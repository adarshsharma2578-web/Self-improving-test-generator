import subprocess
import sys
import tempfile
import os


def run_python_tests(source_code, test_code):

    with tempfile.TemporaryDirectory() as temp_dir:

        source_path = os.path.join(temp_dir, "solution.py")
        test_path = os.path.join(temp_dir, "test_solution.py")

        with open(source_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_code)

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    test_path,
                    "-v"
                ],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout + result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "Python test execution timed out."
            }