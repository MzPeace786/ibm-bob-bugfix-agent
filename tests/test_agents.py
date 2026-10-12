"""
Automated unit tests for IBM Bob AI agents and workflows.
"""

import os
import sys
import shutil
import tempfile
import pytest

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.executor.docker_runner import TestExecutionEngine
from backend.git_manager import SafeGitManager
from backend.llm.bob_client import IBMBobClient
from backend.agents.test_runner import TestRunnerAgent
from backend.agents.debugger import DebuggingAgent
from backend.agents.validator import ValidationAgent


@pytest.fixture
def temp_repo():
    """Creates a temporary isolated test repository."""
    temp_dir = tempfile.mkdtemp(prefix="test_repo_")
    src_calc = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_repos", "python_calculator"))
    shutil.copytree(src_calc, temp_dir, dirs_exist_ok=True)
    
    # Initialize git in temp repo
    gm = SafeGitManager(temp_dir)
    yield temp_dir, gm
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_test_runner_agent(temp_repo):
    repo_path, gm = temp_repo
    engine = TestExecutionEngine()
    runner = TestRunnerAgent(engine)
    
    # Initial run should fail due to intentional bugs
    results = runner.execute(repo_path)
    assert results["passed"] is False
    assert results["failed_count"] > 0
    assert len(results["failures"]) > 0


def test_debugging_agent_generates_patch(temp_repo):
    repo_path, gm = temp_repo
    engine = TestExecutionEngine()
    runner = TestRunnerAgent(engine)
    results = runner.execute(repo_path)
    
    bob = IBMBobClient()
    debugger = DebuggingAgent(bob)
    patch_info = debugger.analyze_and_patch(repo_path, results, iteration=1)
    
    assert "patch_diff" in patch_info
    assert patch_info["target_file"] == "calculator.py"
    assert "fixed_content" in patch_info
    assert patch_info["risk_score"] > 0.0


def test_validation_agent_applies_and_commits(temp_repo):
    repo_path, gm = temp_repo
    engine = TestExecutionEngine()
    runner = TestRunnerAgent(engine)
    results = runner.execute(repo_path)
    
    bob = IBMBobClient()
    debugger = DebuggingAgent(bob)
    patch_info = debugger.analyze_and_patch(repo_path, results, iteration=1)
    
    validator = ValidationAgent(gm, runner)
    val_res = validator.validate_and_finalize(repo_path, patch_info, run_id="unit-test-1")
    
    # After patch, tests must pass and commit must be created
    assert val_res["validated"] is True
    assert val_res["action"] == "committed"
    assert "commit_hash" in val_res["commit_details"]
