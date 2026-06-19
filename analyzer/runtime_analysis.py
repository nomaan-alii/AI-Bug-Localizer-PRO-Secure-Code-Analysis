import traceback
import builtins
import sys
import io


def run_code(code):
    """
    Safe runtime analyzer.

    Detects:
    - runtime errors
    - execution line
    - error type + message
    """

    issues = []

    try:
        # safer execution environment
        safe_globals = {
            "__builtins__": builtins
        }

        safe_locals = {}

        # ---------------- EXECUTION ----------------
        exec(code, safe_globals, safe_locals)

    except Exception as e:

        tb = traceback.extract_tb(e.__traceback__)

        # get most relevant line
        line = tb[-1].lineno if tb else 0

        error_type = type(e).__name__

        issues.append({
            "line": line,
            "type": "runtime_error_" + error_type.lower(),
            "msg": str(e),
            "var": None,
            "score": 0.90
        })

    return issues