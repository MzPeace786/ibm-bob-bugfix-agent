"""
Git repository manager using GitPython.
Provides safe branch isolation, staging, diff extraction, automatic commits,
and atomic rollbacks to guarantee that the original repository is never modified without authorization.
"""

import os
import shutil
import tempfile
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# Ensure GitPython finds git on Windows
GIT_CANDIDATE_PATHS = [
    r"C:\Users\amank\AppData\Local\GitHubDesktop\app-3.6.4\resources\app\git\cmd\git.exe",
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
]

for candidate in GIT_CANDIDATE_PATHS:
    if os.path.exists(candidate):
        os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = candidate
        break

os.environ["GIT_PYTHON_REFRESH"] = "quiet"

import git
from git import Repo, GitCommandError

logger = logging.getLogger("ibm_bob.git_manager")


class SafeGitManager:
    """
    Manages safe repository interactions.
    Creates isolated scratch workspaces or branches to prevent modifying
    original repos directly without explicit authorization.
    """

    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        if not os.path.isdir(self.repo_path):
            raise FileNotFoundError(f"Repository directory does not exist: {self.repo_path}")

        try:
            self.repo = Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            logger.info(f"Initializing new git repository at {self.repo_path}")
            self.repo = Repo.init(self.repo_path)
            self._configure_default_user()
            # Initial commit if empty
            if not self.repo.heads:
                self.repo.git.add(A=True)
                self.repo.index.commit("Initial repository commit")

        self._configure_default_user()
        self.initial_branch = self.repo.active_branch.name if self.repo.heads else "main"
        self.active_fix_branch: Optional[str] = None
        self.temporary_clone_dir: Optional[str] = None

    def _configure_default_user(self):
        """Ensure git user name and email are configured for automated commits."""
        with self.repo.config_writer() as config:
            if not config.has_section("user"):
                config.add_section("user")
            if not config.has_option("user", "name"):
                config.set_value("user", "name", "IBM Bob Automated Agent")
            if not config.has_option("user", "email"):
                config.set_value("user", "email", "bob-agent@ibm.com")

    def create_isolated_fix_branch(self, run_id: str) -> str:
        """
        Creates a dedicated isolation branch for automated bug fixing.
        Format: ibm-bob-fix-<run_id>
        """
        branch_name = f"ibm-bob-fix-{run_id}"
        logger.info(f"Creating isolated branch '{branch_name}' from '{self.initial_branch}'")
        
        # If branch already exists, switch to it, else create new
        if branch_name in [h.name for h in self.repo.heads]:
            self.repo.git.checkout(branch_name)
        else:
            self.repo.git.checkout("-b", branch_name)

        self.active_fix_branch = branch_name
        return branch_name

    def create_isolated_scratch_clone(self) -> str:
        """
        Creates a completely isolated disk copy (scratch workspace) of the repo.
        All agent edits occur in this temporary clone until validated.
        """
        temp_dir = tempfile.mkdtemp(prefix="ibm_bob_workspace_")
        logger.info(f"Creating isolated scratch clone at {temp_dir}")
        shutil.copytree(self.repo_path, temp_dir, dirs_exist_ok=True)
        self.temporary_clone_dir = temp_dir
        return temp_dir

    def cleanup_scratch_clone(self):
        """Removes the temporary scratch workspace."""
        if self.temporary_clone_dir and os.path.exists(self.temporary_clone_dir):
            try:
                shutil.rmtree(self.temporary_clone_dir, ignore_errors=True)
                logger.info(f"Cleaned up scratch clone at {self.temporary_clone_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanly delete scratch workspace: {e}")
            self.temporary_clone_dir = None

    def get_diff(self) -> str:
        """Returns the current git diff of unstaged and staged changes."""
        try:
            diff_text = self.repo.git.diff("HEAD")
            if not diff_text:
                # Also check staged changes
                diff_text = self.repo.git.diff("--staged")
            return diff_text
        except GitCommandError:
            return ""

    def get_status_summary(self) -> Dict[str, Any]:
        """Returns a structured summary of git status."""
        try:
            untracked = self.repo.untracked_files
            modified = [item.a_path for item in self.repo.index.diff(None)]
            staged = [item.a_path for item in self.repo.index.diff("HEAD")]
            return {
                "active_branch": self.repo.active_branch.name,
                "clean": not (untracked or modified or staged),
                "untracked": untracked,
                "modified": modified,
                "staged": staged,
                "head_commit": str(self.repo.head.commit.hexsha[:8]) if self.repo.heads else "none"
            }
        except Exception as e:
            return {"error": str(e), "clean": False}

    def commit_fix(self, message: str, run_id: str, author_name: str = "IBM Bob Bug-Fixing Agent") -> Dict[str, Any]:
        """
        Stages all validated fixes and creates a standardized commit.
        """
        logger.info(f"Committing fix for run {run_id}: {message}")
        try:
            self.repo.git.add(A=True)
            commit = self.repo.index.commit(
                message,
                author=git.Actor(author_name, "bob-agent@ibm.com"),
                committer=git.Actor("IBM Bob System", "bob-system@ibm.com")
            )
            return {
                "status": "success",
                "commit_hash": commit.hexsha,
                "commit_short": commit.hexsha[:8],
                "message": message,
                "branch": self.repo.active_branch.name
            }
        except Exception as e:
            logger.error(f"Failed to commit fix: {e}")
            return {"status": "error", "error": str(e)}

    def rollback_changes(self) -> bool:
        """
        Performs an atomic rollback of all working tree and index changes.
        """
        logger.warning("Rolling back all uncommitted changes...")
        try:
            # Discard staged and unstaged modifications
            self.repo.git.reset("--hard", "HEAD")
            # Remove untracked files and directories
            self.repo.git.clean("-fd")
            logger.info("Rollback successful. Working tree is clean.")
            return True
        except Exception as e:
            logger.error(f"Failed to rollback working tree: {e}")
            return False

    def restore_initial_branch(self) -> bool:
        """Switches back to the initial starting branch."""
        try:
            if self.initial_branch and self.initial_branch in [h.name for h in self.repo.heads]:
                self.repo.git.checkout(self.initial_branch)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to restore initial branch: {e}")
            return False
