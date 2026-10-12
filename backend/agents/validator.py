"""
Validation Agent.
Applies patches in temporary scratch workspaces/branches, reruns automated tests,
and automatically commits successful fixes or immediately rolls back failed changes.
"""

import os
import logging
from typing import Dict, Any
from backend.git_manager import SafeGitManager
from backend.agents.test_runner import TestRunnerAgent

logger = logging.getLogger("ibm_bob.agent.validator")


class ValidationAgent:
    """
    Agent responsible for applying candidate patches, verifying fixes,
    and executing automated git commits or atomic rollbacks.
    """

    def __init__(self, git_manager: SafeGitManager, test_runner: TestRunnerAgent):
        self.git = git_manager
        self.test_runner = test_runner

    def apply_patch_to_file(self, workspace_path: str, target_file: str, fixed_content: str) -> bool:
        """Writes the proposed patch content to the target file in the workspace."""
        full_path = os.path.join(workspace_path, target_file)
        logger.info(f"[Validation Agent] Applying patch to {full_path}")
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
        except Exception as e:
            logger.error(f"Failed to write patch to {full_path}: {e}")
            return False

    def validate_and_finalize(
        self,
        workspace_path: str,
        patch_info: Dict[str, Any],
        run_id: str,
        custom_command: str = None
    ) -> Dict[str, Any]:
        """
        Applies patch, runs test verification suite, and commits or rolls back.
        """
        target_file = patch_info.get("target_file")
        fixed_content = patch_info.get("fixed_content")
        commit_message = patch_info.get("commit_message", "[IBM Bob Auto-Fix] Bug fix")

        # 1. Apply patch
        apply_ok = self.apply_patch_to_file(workspace_path, target_file, fixed_content)
        if not apply_ok:
            return {
                "validated": False,
                "action": "apply_failed",
                "message": f"Could not apply patch to {target_file}"
            }

        # 2. Rerun tests
        logger.info("[Validation Agent] Re-running tests to verify patch effectiveness...")
        test_results = self.test_runner.execute(workspace_path, custom_command=custom_command)

        # 3. Assess results
        if test_results.get("passed", False):
            logger.info("[Validation Agent] All tests passed! Committing fix to git repository...")
            commit_res = self.git.commit_fix(commit_message, run_id=run_id)
            return {
                "validated": True,
                "action": "committed",
                "test_results": test_results,
                "commit_details": commit_res,
                "message": "Patch validated successfully and committed to branch."
            }
        else:
            logger.warning("[Validation Agent] Tests still failing after patch. Initiating atomic rollback...")
            self.git.rollback_changes()
            return {
                "validated": False,
                "action": "rolled_back",
                "test_results": test_results,
                "message": "Tests failed. Changes rolled back to clean working tree."
            }
