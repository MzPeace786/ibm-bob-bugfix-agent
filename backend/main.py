"""
FastAPI Server for AI-Powered Automated Bug-Fixing & Testing Agent (IBM Bob).
Provides REST endpoints, WebSocket streaming, and serves the Web Dashboard.
"""

import os
import sys
import uuid
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

# Ensure root directory is on PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure Git executable is configured
GIT_CANDIDATE_PATHS = [
    r"C:\Users\amank\AppData\Local\GitHubDesktop\app-3.6.4\resources\app\git\cmd\git.exe",
    r"C:\Program Files\Git\cmd\git.exe",
]
for candidate in GIT_CANDIDATE_PATHS:
    if os.path.exists(candidate):
        os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = candidate
        break

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from backend.git_manager import SafeGitManager
from backend.executor.docker_runner import TestExecutionEngine
from backend.llm.bob_client import IBMBobClient
from backend.graph import BugFixWorkflow, AgentWorkflowState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger("ibm_bob.server")

app = FastAPI(
    title="IBM Bob AI Bug-Fixing Agent",
    description="Autonomous testing, debugging, and validation pipeline powered by IBM Bob & LangGraph",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State Storage
active_runs: Dict[str, Dict[str, Any]] = {}
active_workflows: Dict[str, BugFixWorkflow] = {}
fix_history: List[Dict[str, Any]] = []
connected_websockets: List[WebSocket] = []

# Global Execution Engine and Bob Client
execution_engine = TestExecutionEngine()
bob_client = IBMBobClient()


# --- Models ---
class RunRequest(BaseModel):
    repo_path: Optional[str] = None
    repo_key: Optional[str] = "python_calculator"
    max_retries: Optional[int] = 3
    hitl_enabled: Optional[bool] = False
    risk_threshold: Optional[float] = 0.5
    custom_command: Optional[str] = None
    model_id: Optional[str] = "ibm/granite-3-8b-instruct"
    use_docker: Optional[bool] = False


class ApprovalRequest(BaseModel):
    run_id: str
    approved: bool
    rejection_reason: Optional[str] = None


class RollbackRequest(BaseModel):
    repo_path: Optional[str] = None
    repo_key: Optional[str] = "python_calculator"


# --- Helpers ---
def get_sample_repos() -> Dict[str, str]:
    sample_dir = ROOT_DIR / "sample_repos"
    return {
        "python_calculator": str(sample_dir / "python_calculator"),
        "js_string_utils": str(sample_dir / "js_string_utils")
    }


async def broadcast_state(data: Dict[str, Any]):
    """Broadcasts state updates to all connected WebSockets."""
    for ws in list(connected_websockets):
        try:
            await ws.send_json(data)
        except Exception:
            if ws in connected_websockets:
                connected_websockets.remove(ws)


# --- REST Endpoints ---

@app.get("/api/status")
def get_status():
    """Returns engine health, docker status, and available models."""
    return {
        "status": "online",
        "ibm_bob_engine": "IBM Bob / Granite Agentic Architecture",
        "cloud_mode": bob_client.is_live_cloud_enabled(),
        "docker_available": execution_engine.docker_available,
        "active_runs_count": len(active_runs),
        "total_fixes": len(fix_history),
        "default_repos": list(get_sample_repos().keys())
    }


@app.get("/api/repos")
def list_repositories():
    """Lists available sample repositories and metadata."""
    sample_repos = get_sample_repos()
    repos_info = []

    for key, path in sample_repos.items():
        if os.path.exists(path):
            try:
                gm = SafeGitManager(path)
                status = gm.get_status_summary()
                project_type = execution_engine.detect_project_type(path)
                repos_info.append({
                    "key": key,
                    "name": key.replace("_", " ").title(),
                    "path": path,
                    "type": project_type,
                    "status": status
                })
            except Exception as e:
                repos_info.append({
                    "key": key,
                    "name": key.replace("_", " ").title(),
                    "path": path,
                    "type": "unknown",
                    "error": str(e)
                })

    return {"repositories": repos_info}


@app.post("/api/run")
async def trigger_run(req: RunRequest, background_tasks: BackgroundTasks):
    """Triggers a new automated bug fixing and testing agent workflow."""
    repos = get_sample_repos()
    target_path = req.repo_path or repos.get(req.repo_key)

    if not target_path or not os.path.isdir(target_path):
        raise HTTPException(status_code=400, detail=f"Invalid repository path: {target_path}")

    run_id = str(uuid.uuid4())[:8]

    # Initialize Git Manager
    git_manager = SafeGitManager(target_path)
    # Create isolated fix branch
    branch_name = git_manager.create_isolated_fix_branch(run_id)

    # Initialize Workflow
    workflow = BugFixWorkflow(
        git_manager=git_manager,
        execution_engine=execution_engine,
        bob_client=bob_client
    )
    active_workflows[run_id] = workflow

    initial_state: AgentWorkflowState = {
        "run_id": run_id,
        "workspace_path": target_path,
        "original_repo_path": target_path,
        "branch_name": branch_name,
        "project_type": execution_engine.detect_project_type(target_path),
        "custom_command": req.custom_command,
        "iteration": 1,
        "max_retries": req.max_retries or 3,
        "hitl_enabled": req.hitl_enabled or False,
        "risk_threshold": req.risk_threshold or 0.5,
        "status": "STARTING",
        "stage": "INITIALIZATION",
        "test_results": {},
        "patch_info": None,
        "validation_results": None,
        "requires_approval": False,
        "approved_by_human": None,
        "rejection_reason": None,
        "logs": [{
            "timestamp": "00:00:00",
            "level": "INFO",
            "stage": "INIT",
            "iteration": 1,
            "message": f"Run {run_id} initiated on branch '{branch_name}'. Mode: {'Docker' if req.use_docker else 'Isolated Sandbox'}."
        }],
        "error": None
    }

    active_runs[run_id] = initial_state

    # Launch workflow in background task
    background_tasks.add_task(execute_workflow_task, run_id, workflow, initial_state)

    return {
        "status": "started",
        "run_id": run_id,
        "branch": branch_name,
        "workspace": target_path
    }


async def execute_workflow_task(run_id: str, workflow: BugFixWorkflow, state: AgentWorkflowState):
    """Asynchronous background worker executing LangGraph state machine."""
    logger.info(f"Starting LangGraph execution task for run {run_id}")

    try:
        # Step 1: Run tests
        state = workflow.node_run_tests(state)
        active_runs[run_id] = state
        await broadcast_state({"type": "state_update", "run_id": run_id, "state": state})

        if state["status"] == "ALL_TESTS_PASSED":
            return

        # Loop until success, max retries, or awaiting approval
        while state["status"] not in ("SUCCESS", "ALL_TESTS_PASSED", "MAX_RETRIES_EXCEEDED", "PATCH_REJECTED", "FAILED", "DEBUGGING_ERROR"):
            # Debugging Node
            state = workflow.node_debug(state)
            active_runs[run_id] = state
            await broadcast_state({"type": "state_update", "run_id": run_id, "state": state})

            # Check if paused for Human Approval
            if state.get("requires_approval") and state.get("approved_by_human") is None:
                logger.info(f"Run {run_id} paused for Human Approval.")
                return  # Halts here until /api/approve is called

            # If user previously rejected in HITL
            if state.get("approved_by_human") is False:
                state["status"] = "PATCH_REJECTED"
                state["stage"] = "FAILED"
                await broadcast_state({"type": "state_update", "run_id": run_id, "state": state})
                break

            # Validation Node
            state = workflow.node_validate(state)
            active_runs[run_id] = state
            await broadcast_state({"type": "state_update", "run_id": run_id, "state": state})

            if state["status"] == "SUCCESS":
                # Record to fix history
                fix_entry = {
                    "run_id": run_id,
                    "target_file": state.get("patch_info", {}).get("target_file", "unknown"),
                    "bug_category": state.get("patch_info", {}).get("bug_category", "LogicError"),
                    "commit": state.get("validation_results", {}).get("commit_details", {}),
                    "iterations": state.get("iteration", 1),
                    "branch": state.get("branch_name"),
                    "timestamp": state.get("logs", [{}])[-1].get("timestamp", "00:00:00")
                }
                fix_history.insert(0, fix_entry)
                break

    except Exception as e:
        logger.error(f"Error executing run {run_id}: {e}", exc_info=True)
        state["status"] = "FAILED"
        state["error"] = str(e)
        active_runs[run_id] = state
        await broadcast_state({"type": "state_update", "run_id": run_id, "state": state})


@app.post("/api/approve")
async def approve_patch(req: ApprovalRequest, background_tasks: BackgroundTasks):
    """Resume execution after human approval or rejection."""
    if req.run_id not in active_runs:
        raise HTTPException(status_code=404, detail="Run not found.")

    state = active_runs[req.run_id]
    workflow = active_workflows.get(req.run_id)

    if not workflow:
        raise HTTPException(status_code=400, detail="Workflow instance no longer active.")

    state["approved_by_human"] = req.approved
    state["rejection_reason"] = req.rejection_reason
    state["requires_approval"] = False

    state = workflow.node_human_gate(state)
    active_runs[req.run_id] = state
    await broadcast_state({"type": "state_update", "run_id": req.run_id, "state": state})

    if req.approved:
        # Continue validation in background
        background_tasks.add_task(continue_workflow_after_approval, req.run_id, workflow, state)
    else:
        # Revert/rollback
        workflow.git.rollback_changes()

    return {"status": "decision_recorded", "approved": req.approved}


async def continue_workflow_after_approval(run_id: str, workflow: BugFixWorkflow, state: AgentWorkflowState):
    """Executes validation after human reviewer approves the candidate patch."""
    state = workflow.node_validate(state)
    active_runs[run_id] = state
    await broadcast_state({"type": "state_update", "run_id": run_id, "state": state})

    if state["status"] == "SUCCESS":
        fix_entry = {
            "run_id": run_id,
            "target_file": state.get("patch_info", {}).get("target_file", "unknown"),
            "bug_category": state.get("patch_info", {}).get("bug_category", "LogicError"),
            "commit": state.get("validation_results", {}).get("commit_details", {}),
            "iterations": state.get("iteration", 1),
            "branch": state.get("branch_name"),
            "timestamp": state.get("logs", [{}])[-1].get("timestamp", "00:00:00")
        }
        fix_history.insert(0, fix_entry)


@app.post("/api/rollback")
def trigger_rollback(req: RollbackRequest):
    """Performs immediate rollback of working tree changes in the specified repo."""
    repos = get_sample_repos()
    target_path = req.repo_path or repos.get(req.repo_key)
    if not target_path:
        raise HTTPException(status_code=400, detail="Invalid repository target.")

    try:
        gm = SafeGitManager(target_path)
        gm.rollback_changes()
        gm.restore_initial_branch()
        return {"status": "success", "message": "Working tree rolled back to clean initial state."}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/api/run/{run_id}")
def get_run(run_id: str):
    """Returns details for a specific run."""
    if run_id not in active_runs:
        raise HTTPException(status_code=404, detail="Run not found.")
    return active_runs[run_id]


@app.get("/api/diff")
def get_current_diff(repo_key: str = "python_calculator", repo_path: Optional[str] = None):
    """Returns current working tree diff for a repository."""
    repos = get_sample_repos()
    target_path = repo_path or repos.get(repo_key)
    if not target_path or not os.path.isdir(target_path):
        return {"diff": ""}

    gm = SafeGitManager(target_path)
    return {"diff": gm.get_diff(), "status": gm.get_status_summary()}


@app.get("/api/history")
def get_history():
    """Returns historical automated fixes."""
    return {"history": fix_history}


# --- WebSocket Endpoint ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)
    logger.info("WebSocket client connected.")
    try:
        while True:
            # Keepalive listener
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected.")
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)
    except Exception as e:
        logger.warning(f"WebSocket error: {e}")
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)


# --- Static Files / Frontend Serving ---

frontend_dir = ROOT_DIR / "frontend"
docs_dir = ROOT_DIR / "docs"

if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(str(frontend_dir / "index.html"))

    @app.get("/report")
    def serve_report():
        report_html = docs_dir / "PROJECT_REPORT.html"
        if report_html.exists():
            return FileResponse(str(report_html))
        return FileResponse(str(docs_dir / "PROJECT_REPORT.md"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
