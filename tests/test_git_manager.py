"""
Unit tests for SafeGitManager repository operations.
"""

import os
import sys
import shutil
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.git_manager import SafeGitManager


def test_safe_git_isolation_and_rollback():
    temp_dir = tempfile.mkdtemp(prefix="git_test_")
    try:
        # Create a sample file
        test_file = os.path.join(temp_dir, "sample.txt")
        with open(test_file, "w") as f:
            f.write("Initial content\n")

        gm = SafeGitManager(temp_dir)
        initial_branch = gm.initial_branch

        # Create isolated branch
        fix_branch = gm.create_isolated_fix_branch("test-branch-1")
        assert fix_branch == "ibm-bob-fix-test-branch-1"

        # Modify file
        with open(test_file, "w") as f:
            f.write("Modified buggy content\n")

        diff = gm.get_diff()
        assert "Modified buggy content" in diff

        # Test rollback
        rollback_ok = gm.rollback_changes()
        assert rollback_ok is True

        # Verify content reverted
        with open(test_file, "r") as f:
            assert f.read() == "Initial content\n"

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
