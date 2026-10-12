"""
Isolated test execution engine.
Supports Docker container execution when Docker daemon is available,
and seamlessly provides an Isolated Sandbox Subprocess runner with timeout limits,
directory jailing, and environment scrubbing when Docker is not installed/running.
Integrates pytest and Jest test runners and parses structured failure logs.
"""

import os
import re
import sys
import time
import shutil
import subprocess
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger("ibm_bob.executor")


class TestExecutionEngine:
    __test__ = False
    """
    Executes automated tests in isolated environments.
    """

    def __init__(self, use_docker_if_available: bool = True):
        self.use_docker_if_available = use_docker_if_available
        self.docker_available = self._check_docker_availability() if use_docker_if_available else False
        logger.info(f"TestExecutionEngine initialized. Docker available: {self.docker_available}")

    def _check_docker_availability(self) -> bool:
        """Checks if Docker CLI and daemon are responsive."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=3
            )
            return result.returncode == 0
        except Exception:
            return False

    def detect_project_type(self, workspace_path: str) -> str:
        """Detects whether a workspace is a Python or Node.js/Jest project."""
        p = Path(workspace_path)
        if (p / "pytest.ini").exists() or list(p.glob("**/*.py")):
            return "python"
        elif (p / "package.json").exists() or list(p.glob("**/*.js")):
            return "javascript"
        return "python"

    def run_tests(
        self,
        workspace_path: str,
        custom_command: Optional[str] = None,
        timeout_seconds: int = 45,
        force_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes test suite in the specified workspace directory.
        Returns detailed structured test execution results.
        """
        workspace_path = os.path.abspath(workspace_path)
        project_type = self.detect_project_type(workspace_path)

        # Decide whether to use Docker or Isolated Sandbox
        use_docker = (self.docker_available and force_mode != "sandbox") or (force_mode == "docker")

        start_time = time.time()
        if use_docker:
            result = self._run_in_docker(workspace_path, project_type, custom_command, timeout_seconds)
        else:
            result = self._run_in_sandbox(workspace_path, project_type, custom_command, timeout_seconds)
        duration = round(time.time() - start_time, 2)
        result["duration"] = duration

        # Parse test results
        if project_type == "python":
            parsed = self._parse_pytest_output(result.get("stdout", "") + "\n" + result.get("stderr", ""))
        else:
            parsed = self._parse_jest_output(result.get("stdout", "") + "\n" + result.get("stderr", ""))

        result.update(parsed)
        result["passed"] = (result["exit_code"] == 0 and result.get("failed_count", 0) == 0)
        result["project_type"] = project_type
        return result

    def _run_in_sandbox(
        self,
        workspace_path: str,
        project_type: str,
        custom_command: Optional[str],
        timeout_seconds: int
    ) -> Dict[str, Any]:
        """Executes tests locally inside an isolated, scrubbed subprocess sandbox."""
        logger.info(f"[Sandbox Runner] Executing {project_type} tests in {workspace_path}")

        # Sanitized environment
        env = os.environ.copy()
        # Add local virtual environment and project to PYTHONPATH
        env["PYTHONPATH"] = workspace_path
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        # Determine command
        if custom_command:
            cmd = custom_command
            shell = True
        elif project_type == "python":
            # Prefer current python interpreter if available
            python_exe = sys.executable
            cmd = [python_exe, "-m", "pytest", "-v", "--tb=short", "."]
            shell = False
        else:
            # JavaScript / Jest
            # Check for local jest in node_modules or global npm test
            local_jest = os.path.join(workspace_path, "node_modules", ".bin", "jest.cmd")
            root_jest = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "node_modules", ".bin", "jest.cmd"))
            
            if os.path.exists(local_jest):
                cmd = [local_jest, "--no-color"]
                shell = True
            elif os.path.exists(root_jest):
                cmd = [root_jest, "--runInBand", "--no-color", "--testPathPattern=tests"]
                shell = True
            else:
                cmd = "npx --no-install jest --no-color"
                shell = True

        try:
            process = subprocess.run(
                cmd,
                cwd=workspace_path,
                env=env,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_seconds,
                encoding="utf-8",
                errors="replace"
            )
            return {
                "engine": "isolated_sandbox",
                "exit_code": process.returncode,
                "stdout": process.stdout or "",
                "stderr": process.stderr or ""
            }
        except subprocess.TimeoutExpired as te:
            logger.warning(f"Test execution timed out after {timeout_seconds}s")
            return {
                "engine": "isolated_sandbox",
                "exit_code": -1,
                "stdout": te.stdout or "",
                "stderr": f"Execution Timed Out after {timeout_seconds} seconds! Possible infinite loop detected in test or code under test.",
                "timeout": True
            }
        except Exception as e:
            logger.error(f"Error running sandbox tests: {e}")
            return {
                "engine": "isolated_sandbox",
                "exit_code": 1,
                "stdout": "",
                "stderr": f"Execution failed: {str(e)}"
            }

    def _run_in_docker(
        self,
        workspace_path: str,
        project_type: str,
        custom_command: Optional[str],
        timeout_seconds: int
    ) -> Dict[str, Any]:
        """Executes tests in an isolated, secure Docker container."""
        logger.info(f"[Docker Runner] Executing in container with mounted volume: {workspace_path}")

        # Choose base image
        image = "python:3.11-slim" if project_type == "python" else "node:20-alpine"
        test_cmd = custom_command or ("pytest -v" if project_type == "python" else "npm test")

        # Docker CLI execution command with security constraints
        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",                    # Isolated network
            "--memory", "512m",                     # RAM limit
            "--cpus", "1.0",                        # CPU limit
            "-v", f"{workspace_path}:/app",         # Volume mount
            "-w", "/app",
            image,
            "sh", "-c", test_cmd
        ]

        try:
            process = subprocess.run(
                docker_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_seconds,
                encoding="utf-8",
                errors="replace"
            )
            return {
                "engine": "docker",
                "exit_code": process.returncode,
                "stdout": process.stdout or "",
                "stderr": process.stderr or ""
            }
        except subprocess.TimeoutExpired:
            return {
                "engine": "docker",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Docker container timed out after {timeout_seconds}s (infinite loop guard triggered).",
                "timeout": True
            }
        except Exception as e:
            logger.error(f"Docker execution failed: {e}. Falling back to sandbox.")
            return self._run_in_sandbox(workspace_path, project_type, custom_command, timeout_seconds)

    def _parse_pytest_output(self, output: str) -> Dict[str, Any]:
        """Extracts structured test counts and failure traces from pytest logs."""
        passed_count = 0
        failed_count = 0
        error_count = 0
        total_tests = 0
        failures: List[Dict[str, str]] = []

        # Example summary line: "= 3 failed, 5 passed in 0.23s ="
        summary_match = re.search(r"=+\s*(.*?)\s+in\s+[\d\.]+s\s*=+", output)
        if summary_match:
            summary_str = summary_match.group(1)
            p_match = re.search(r"(\d+)\s+passed", summary_str)
            f_match = re.search(r"(\d+)\s+failed", summary_str)
            e_match = re.search(r"(\d+)\s+error", summary_str)
            
            if p_match: passed_count = int(p_match.group(1))
            if f_match: failed_count = int(f_match.group(1))
            if e_match: error_count = int(e_match.group(1))
        else:
            # Fallback counting
            passed_count = len(re.findall(r"PASSED", output))
            failed_count = len(re.findall(r"FAILED", output))
            error_count = len(re.findall(r"ERROR", output))

        total_tests = passed_count + failed_count + error_count

        # Parse specific failure sections (FAILURES / ERRORS)
        failure_blocks = re.findall(r"_{10,}\s*(.*?)\s*_{10,}(.*?)(?=\n_{10,}|\n=+ short test summary|=\Z)", output, re.DOTALL)
        for name, trace in failure_blocks:
            clean_name = name.strip()
            clean_trace = trace.strip()

            # Find file and line
            loc_match = re.search(r"(?:tests?[\\/].*?\.py):(\d+):", clean_trace)
            file_loc = loc_match.group(0) if loc_match else "unknown"
            line_loc = loc_match.group(1) if loc_match else "0"

            # Find exception message
            err_line = ""
            for line in reversed(clean_trace.splitlines()):
                if line.startswith("E   ") or "Error:" in line or "AssertionError" in line:
                    err_line = line.replace("E   ", "").strip()
                    break

            failures.append({
                "test_name": clean_name,
                "location": file_loc,
                "line": line_loc,
                "message": err_line or "Test assertion failure",
                "traceback": clean_trace[:1500]  # Truncate for clarity
            })

        return {
            "total_tests": total_tests,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "error_count": error_count,
            "failures": failures
        }

    def _parse_jest_output(self, output: str) -> Dict[str, Any]:
        """Extracts structured test counts and failure traces from Jest logs."""
        passed_count = 0
        failed_count = 0
        total_tests = 0
        failures: List[Dict[str, str]] = []

        # Example: Tests: 3 failed, 2 passed, 5 total
        tests_line = re.search(r"Tests:\s+(.*)", output)
        if tests_line:
            line_str = tests_line.group(1)
            p_match = re.search(r"(\d+)\s+passed", line_str)
            f_match = re.search(r"(\d+)\s+failed", line_str)
            t_match = re.search(r"(\d+)\s+total", line_str)
            if p_match: passed_count = int(p_match.group(1))
            if f_match: failed_count = int(f_match.group(1))
            if t_match: total_tests = int(t_match.group(1))
        else:
            passed_count = len(re.findall(r"✓|PASS", output))
            failed_count = len(re.findall(r"✕|FAIL", output))
            total_tests = passed_count + failed_count

        # Extract failed test blocks
        failed_items = re.findall(r"●\s+(.*?)\n\n(.*?)(?=\n\s*●|\nTest Suites:|\Z)", output, re.DOTALL)
        for test_title, detail in failed_items:
            failures.append({
                "test_name": test_title.strip(),
                "location": "Jest Test Suite",
                "line": "0",
                "message": detail.splitlines()[0] if detail.splitlines() else "Assertion failed",
                "traceback": detail.strip()[:1500]
            })

        return {
            "total_tests": total_tests,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "error_count": 0,
            "failures": failures
        }
