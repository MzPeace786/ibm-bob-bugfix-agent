"""
Unit tests for TestExecutionEngine.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.executor.docker_runner import TestExecutionEngine


def test_test_execution_engine_sandbox():
    engine = TestExecutionEngine()
    calc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_repos", "python_calculator"))
    
    res = engine.run_tests(calc_path, force_mode="sandbox")
    assert "total_tests" in res
    assert "failures" in res
    assert res["project_type"] == "python"
    assert res["engine"] == "isolated_sandbox"
