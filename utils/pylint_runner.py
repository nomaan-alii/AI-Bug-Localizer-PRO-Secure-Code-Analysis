import subprocess
import sys
import tempfile
import os


def run_pylint(code):
    """
    Safe pylint runner (FIXED: prevents parsing crash noise)
    """

    if not code or not code.strip():
        return "⚠️ No code provided for analysis."

    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        result = subprocess.run(
            [sys.executable, "-m", "pylint", tmp_path,
             "--disable=all",
             "--enable=E,W"],   # safer coverage
            capture_output=True,
            text=True,
            check=False
        )

        output = result.stdout + result.stderr

        # 🔥 CLEAN INVALID PARSE ERROR
        if "E0001" in output:
            return "⚠️ Pylint could not parse code (syntax issue detected). Fix syntax first."

        if not output.strip():
            return "✅ Code quality: Excellent (No issues detected)"

        return output

    except Exception as e:
        return f"⚠️ Pylint error: {str(e)}"

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)