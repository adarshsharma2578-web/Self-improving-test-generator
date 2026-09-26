from routers.python_runner import run_python_tests
from routers.javascript_runner import run_javascript_tests
from routers.java_runner import run_java_tests


def run_tests(source_code, test_code, language):
    """
    Select the correct test runner according to
    the programming language.
    """

    language = language.strip().lower()

    if language == "python":
        return run_python_tests(
            source_code,
            test_code
        )

    elif language in ["javascript", "js"]:
        return run_javascript_tests(
            source_code,
            test_code
        )

    elif language == "java":
        return run_java_tests(
            source_code,
            test_code
        )

    else:
        return {
            "success": False,
            "output": (
                f"Unsupported language: {language}. "
                "Supported languages: Python, JavaScript, Java."
            ),
            "return_code": -1
        }


if __name__ == "__main__":
    print("Test Runner Router")
    print("------------------")
    print("Python      → Pytest")
    print("JavaScript  → Jest")
    print("Java        → JUnit")