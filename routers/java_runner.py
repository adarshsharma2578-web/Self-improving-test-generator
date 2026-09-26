import subprocess
import tempfile
import os


def run_java_tests(source_code, test_code):

    with tempfile.TemporaryDirectory() as temp_dir:

        source_path = os.path.join(temp_dir, "Calculator.java")
        test_path = os.path.join(temp_dir, "CalculatorTest.java")

        with open(source_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_code)

        try:

            compile_result = subprocess.run(
                ["javac", source_path, test_path],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            if compile_result.returncode != 0:

                return {
                    "success": False,
                    "output": compile_result.stderr
                }

            return {
                "success": True,
                "output": "Java files compiled successfully."
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "output": "Java test execution timed out."
            }