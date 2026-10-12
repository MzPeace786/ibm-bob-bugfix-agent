"""
LangGraph stateful agent workflow for IBM Bob Automated Bug-Fixing & Testing Agent.
Coordinates Test Runner Agent, Debugging Agent, Human-in-the-Loop Approval Gate,
and Validation Agent with iterative retry limits and loop protection.
"""

import os
import time
import logging
from typing import TypedDict, List, Dict, Any, Optional, Literal
from langgraph.graph import StateGraph, START, END

from backend.git_manager import SafeGitManager
from backend.executor.docker_runner import TestExecutionEngine
from backend.llm.bob_client import IBMBobClient
from backend.agents.test_runner import TestRunnerAgent
from backend.agents.debugger import DebuggingAgent
from backend.agents.validator import ValidationAgent

logger = logging.getLogger("ibm_bob.workflow")


class AgentWorkflowState(TypedDict):
    run_id: str
    workspace_path: str
    original_repo_path: str
    branch_name: str
    project_type: str
    custom_command: Optional[str]
    iteration: int
    max_retries: int
    hitl_enabled: bool
    risk_threshold: float
    status: str
    stage: str
    test_results: Dict[str, Any]
    patch_info: Optional[Dict[str, Any]]
    validation_results: Optional[Dict[str, Any]]
    requires_approval: bool
    approved_by_human: Optional[bool]
    rejection_reason: Optional[str]
    logs: List[Dict[str, Any]]
    error: Optional[str]


class BugFixWorkflow:
    """
    Encapsulates the LangGraph execution graph and agent dependencies.
    """

    def __init__(
        self,
        git_manager: SafeGitManager,
        execution_engine: TestExecutionEngine,
        bob_client: IBMBobClient
    ):
        self.git = git_manager
        self.engine = execution_engine
        self.bob = bob_client

        self.test_runner_agent = TestRunnerAgent(self.engine)
        self.debugging_agent = DebuggingAgent(self.bob)
        self.validation_agent = ValidationAgent(self.git, self.test_runner_agent)

        self.graph = self._build_graph()

    def _log_event(self, state: AgentWorkflowState, level: str, message: str):
        """Helper to append structured log events."""
        event = {
            "timestamp": time.strftime("%H:%M:%S"),
            "level": level,
            "stage": state.get("stage", "AGENT"),
            "iteration": state.get("iteration", 1),
            "message": message
        }
        state["logs"].append(event)
        logger.info(f"[{level}] {message}")

    # --- GRAPH NODES ---

    def node_run_tests(self, state: AgentWorkflowState) -> AgentWorkflowState:
        """Test Runner Node: Executes tests and collects failure logs."""
        state["stage"] = "TEST_RUNNER"
        self._log_event(state, "INFO", f"Test Runner Agent started in workspace: {state['workspace_path']}")

        results = self.test_runner_agent.execute(
            state["workspace_path"],
            custom_command=state.get("custom_command")
        )
        state["test_results"] = results
        state["project_type"] = results.get("project_type", "python")

        if results.get("passed", False):
            state["status"] = "ALL_TESTS_PASSED"
            state["stage"] = "COMPLETED"
            self._log_event(state, "SUCCESS", "All test cases passed cleanly! No debugging required.")
        else:
            state["status"] = "TESTS_FAILED"
            self._log_event(
                state, "WARNING",
                f"Test suite failed with {results.get('failed_count', 0)} failing test(s). Handing over to Debugging Agent."
            )

        return state

    def node_debug(self, state: AgentWorkflowState) -> AgentWorkflowState:
        """Debugging Node: Uses IBM Bob to analyze failures and propose code patch."""
        state["stage"] = "DEBUGGING"
        self._log_event(
            state, "INFO",
            f"Debugging Agent (IBM Bob) active. Iteration #{state['iteration']}/{state['max_retries']}."
        )

        patch_info = self.debugging_agent.analyze_and_patch(
            state["workspace_path"],
            state["test_results"],
            iteration=state["iteration"]
        )
        state["patch_info"] = patch_info

        if patch_info.get("status") == "error":
            state["status"] = "DEBUGGING_ERROR"
            state["stage"] = "FAILED"
            self._log_event(state, "ERROR", patch_info.get("error", "Debugging failed."))
            return state

        # Check for loop / duplicate patch
        if patch_info.get("is_duplicate_patch"):
            self._log_event(state, "WARNING", "Loop detection warning: Proposed patch matches previous attempt.")

        # Risk assessment
        risk_score = patch_info.get("risk_score", 0.3)
        risk_level = patch_info.get("risk_level", "Low")
        self._log_event(
            state, "AGENT",
            f"Root Cause identified: {patch_info.get('bug_category')}. Modification Risk: {risk_level} ({risk_score})."
        )

        # Check if Human-in-the-Loop is required
        needs_approval = state["hitl_enabled"] and (risk_score >= state["risk_threshold"])
        state["requires_approval"] = needs_approval

        if needs_approval and state.get("approved_by_human") is None:
            state["status"] = "AWAITING_APPROVAL"
            state["stage"] = "HUMAN_APPROVAL"
            self._log_event(state, "PROMPT", "Human Approval required before patch application due to risk threshold.")
        else:
            state["status"] = "READY_FOR_VALIDATION"

        return state

    def node_human_gate(self, state: AgentWorkflowState) -> AgentWorkflowState:
        """Human-in-the-loop Gate: Waits for or handles manual user approval/rejection."""
        state["stage"] = "HUMAN_APPROVAL"
        if state.get("approved_by_human") is True:
            self._log_event(state, "SUCCESS", "Patch approved by human reviewer. Proceeding to validation.")
            state["status"] = "READY_FOR_VALIDATION"
        elif state.get("approved_by_human") is False:
            self._log_event(state, "WARNING", f"Patch rejected by human reviewer. Reason: {state.get('rejection_reason', 'None')}")
            state["status"] = "PATCH_REJECTED"
        return state

    def node_validate(self, state: AgentWorkflowState) -> AgentWorkflowState:
        """Validation Node: Applies patch, reruns tests, auto-commits or rolls back."""
        state["stage"] = "VALIDATION"
        self._log_event(state, "INFO", "Validation Agent applying proposed patch in isolated workspace...")

        val_result = self.validation_agent.validate_and_finalize(
            state["workspace_path"],
            state["patch_info"],
            run_id=state["run_id"],
            custom_command=state.get("custom_command")
        )
        state["validation_results"] = val_result

        if val_result.get("validated", False):
            state["status"] = "SUCCESS"
            state["stage"] = "COMPLETED"
            self._log_event(state, "SUCCESS", f"Patch verified! Auto-committed fix with hash: {val_result.get('commit_details', {}).get('commit_short', 'HEAD')}")
        else:
            self._log_event(state, "ERROR", "Validation failed: tests still failing after patch. Rolled back changes.")
            if state["iteration"] < state["max_retries"]:
                state["iteration"] += 1
                state["status"] = "RETRY"
                self._log_event(state, "INFO", f"Incrementing retry counter. Starting iteration {state['iteration']}/{state['max_retries']}...")
            else:
                state["status"] = "MAX_RETRIES_EXCEEDED"
                state["stage"] = "FAILED"
                self._log_event(state, "ERROR", f"Max retries ({state['max_retries']}) reached without passing tests. Halting to avoid infinite loop.")

        return state

    # --- CONDITIONAL ROUTING ---

    def _route_after_test_runner(self, state: AgentWorkflowState) -> Literal["end", "node_debug"]:
        if state["status"] == "ALL_TESTS_PASSED":
            return "end"
        return "node_debug"

    def _route_after_debugger(self, state: AgentWorkflowState) -> Literal["node_human_gate", "node_validate", "end"]:
        if state["status"] == "DEBUGGING_ERROR":
            return "end"
        if state.get("requires_approval") and state.get("approved_by_human") is None:
            return "node_human_gate"
        return "node_validate"

    def _route_after_human_gate(self, state: AgentWorkflowState) -> Literal["node_validate", "end"]:
        if state.get("approved_by_human") is True:
            return "node_validate"
        return "end"

    def _route_after_validator(self, state: AgentWorkflowState) -> Literal["end", "node_debug"]:
        if state["status"] in ("SUCCESS", "MAX_RETRIES_EXCEEDED", "FAILED"):
            return "end"
        if state["status"] == "RETRY":
            return "node_debug"
        return "end"

    def _build_graph(self):
        """Constructs and compiles the LangGraph StateGraph."""
        builder = StateGraph(AgentWorkflowState)

        builder.add_node("node_run_tests", self.node_run_tests)
        builder.add_node("node_debug", self.node_debug)
        builder.add_node("node_human_gate", self.node_human_gate)
        builder.add_node("node_validate", self.node_validate)

        builder.add_edge(START, "node_run_tests")

        builder.add_conditional_edges(
            "node_run_tests",
            self._route_after_test_runner,
            {
                "end": END,
                "node_debug": "node_debug"
            }
        )

        builder.add_conditional_edges(
            "node_debug",
            self._route_after_debugger,
            {
                "node_human_gate": "node_human_gate",
                "node_validate": "node_validate",
                "end": END
            }
        )

        builder.add_conditional_edges(
            "node_human_gate",
            self._route_after_human_gate,
            {
                "node_validate": "node_validate",
                "end": END
            }
        )

        builder.add_conditional_edges(
            "node_validate",
            self._route_after_validator,
            {
                "node_debug": "node_debug",
                "end": END
            }
        )

        return builder.compile()

    def run(self, initial_state: AgentWorkflowState) -> AgentWorkflowState:
        """Executes the compiled LangGraph workflow."""
        return self.graph.invoke(initial_state)
