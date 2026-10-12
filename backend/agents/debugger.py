"""
Debugging Agent.
Analyzes stack traces, examines project source code, identifies root causes,
assesses risk score, and generates targeted code patches and unified diffs.
Integrates IBM Bob reasoning and loop protection.
"""

import os
import difflib
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from backend.llm.bob_client import IBMBobClient

logger = logging.getLogger("ibm_bob.agent.debugger")


class DebuggingAgent:
    """
    Agent responsible for root cause analysis and patch generation.
    """

    def __init__(self, bob_client: IBMBobClient):
        self.bob = bob_client
        self.attempted_patches: List[str] = []

    def _read_source_files(self, workspace_path: str, project_type: str) -> Dict[str, str]:
        """Reads source code files (excluding tests, venv, git, node_modules) for context."""
        files = {}
        extensions = [".py"] if project_type == "python" else [".js", ".ts"]
        base = Path(workspace_path)

        for root, dirs, filenames in os.walk(workspace_path):
            # Exclude non-source directories
            dirs[:] = [
                d for d in dirs
                if d not in {".git", "node_modules", "venv", ".venv", "__pycache__", ".pytest_cache", "tests", "test"}
            ]
            for file in filenames:
                if any(file.endswith(ext) for ext in extensions):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, workspace_path)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                            files[rel_path] = f.read()
                    except Exception as e:
                        logger.warning(f"Could not read file {rel_path}: {e}")

        return files

    def _generate_unified_diff(self, file_path: str, original_code: str, modified_code: str) -> str:
        """Generates a standard unified diff string."""
        diff_lines = list(difflib.unified_diff(
            original_code.splitlines(keepends=True),
            modified_code.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            n=3
        ))
        return "".join(diff_lines)

    def analyze_and_patch(
        self,
        workspace_path: str,
        test_results: Dict[str, Any],
        iteration: int = 1
    ) -> Dict[str, Any]:
        """
        Runs root-cause analysis on failing tests and generates code patch.
        """
        project_type = test_results.get("project_type", "python")
        failure_logs = test_results.get("stderr", "") + "\n" + test_results.get("stdout", "")
        structured_failures = test_results.get("failures", [])

        source_files = self._read_source_files(workspace_path, project_type)
        if not source_files:
            return {
                "error": "No source files found in workspace to analyze.",
                "status": "error"
            }

        # Query IBM Bob
        bob_response = self.bob.analyze_and_generate_patch(
            project_type=project_type,
            files_content=source_files,
            failure_logs=failure_logs,
            structured_failures=structured_failures,
            iteration=iteration
        )

        target_file = bob_response.get("target_file", list(source_files.keys())[0])
        fixed_content = bob_response.get("fixed_content", "")
        original_content = source_files.get(target_file, "")

        # Compute diff
        patch_diff = self._generate_unified_diff(target_file, original_content, fixed_content)

        # Infinite loop / cycle protection check
        diff_signature = patch_diff.strip()
        if diff_signature in self.attempted_patches:
            logger.warning("Duplicate patch detected! Agent proposed an identical patch previously tried.")
            is_duplicate = True
        else:
            self.attempted_patches.append(diff_signature)
            is_duplicate = False

        # Calculate risk evaluation
        risk_score = bob_response.get("risk_score", 0.3)
        # Escalate risk if large changes or duplicate
        lines_changed = len([line for line in patch_diff.splitlines() if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))])
        if lines_changed > 15:
            risk_score = min(1.0, risk_score + 0.25)
        if is_duplicate:
            risk_score = 1.0

        risk_level = "High" if risk_score >= 0.6 else ("Medium" if risk_score >= 0.35 else "Low")

        return {
            "root_cause_analysis": bob_response.get("root_cause_analysis", "Analyzed failing test diagnostics."),
            "bug_category": bob_response.get("bug_category", "LogicError"),
            "target_file": target_file,
            "original_content": original_content,
            "fixed_content": fixed_content,
            "patch_diff": patch_diff,
            "explanation": bob_response.get("explanation", "Patch generated by IBM Bob."),
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "commit_message": bob_response.get("commit_message", f"fix({target_file}): automated bug fix"),
            "is_duplicate_patch": is_duplicate,
            "lines_changed": lines_changed
        }
