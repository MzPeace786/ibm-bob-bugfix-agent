"""
Test Runner Agent.
Executes test suites (pytest/Jest) in an isolated workspace/container,
captures raw stdout/stderr, evaluates exit codes, and returns structured failure diagnostics.
"""

import logging
from typing import Dict, Any
from backend.executor.docker_runner import TestExecutionEngine

logger = logging.getLogger("ibm_bob.agent.test_runner")


class TestRunnerAgent:
    __test__ = False
    """
    Agent responsible for running tests and collecting test failure telemetry.
    """

    def __init__(self, execution_engine: TestExecutionEngine):
        self.engine = execution_engine

    def execute(self, workspace_path: str, custom_command: str = None) -> Dict[str, Any]:
        """
        Runs the test suite and returns comprehensive test metrics and error logs.
        """
        logger.info(f"[Test Runner Agent] Initiating test run in: {workspace_path}")
        results = self.engine.run_tests(workspace_path, custom_command=custom_command)

        summary = {
            "passed": results.get("passed", False),
            "exit_code": results.get("exit_code", 1),
            "total_tests": results.get("total_tests", 0),
            "passed_count": results.get("passed_count", 0),
            "failed_count": results.get("failed_count", 0),
            "error_count": results.get("error_count", 0),
            "duration": results.get("duration", 0.0),
            "failures": results.get("failures", []),
            "stdout": results.get("stdout", ""),
            "stderr": results.get("stderr", ""),
            "engine": results.get("engine", "isolated_sandbox"),
            "project_type": results.get("project_type", "python")
        }

        logger.info(
            f"[Test Runner Agent] Run complete: {summary['passed_count']} passed, "
            f"{summary['failed_count']} failed out of {summary['total_tests']} tests."
        )
        return summary
