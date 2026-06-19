def explain(issue):
    """
    Clean + consistent explanation engine.
    Works with all analyzer outputs.
    """

    issue_type = issue.get("type", "unknown")
    msg = issue.get("msg", "")
    var = issue.get("var", "")
    line = issue.get("line", "unknown")

    # ---------------- SYNTAX ERROR ----------------
    if issue_type == "syntax_error":
        return (
            f"❌ Syntax Error at line {line}\n\n"
            f"{msg}\n\n"
            "Common causes:\n"
            "- Missing colon (:)\n"
            "- Wrong indentation\n"
            "- Missing brackets () [] {}\n"
        )

    # ---------------- UNDEFINED VARIABLE ----------------
    if issue_type == "undefined_variable":
        return (
            f"⚠️ Undefined Variable '{var}' at line {line}\n\n"
            "This variable is used before assignment.\n"
            "Fix:\n"
            "- Define it before use\n"
            "- Check spelling\n"
            "- Ensure correct scope"
        )

    # ---------------- RUNTIME ERROR ----------------
    if issue_type.startswith("runtime_error"):
        return (
            f"💥 Runtime Error at line {line}\n\n"
            f"{msg}\n\n"
            "This error occurs during execution.\n"
            "Common causes:\n"
            "- Invalid operations\n"
            "- Type mismatch\n"
            "- Division by zero\n"
            "- Missing values"
        )

    # ---------------- FALLBACK ----------------
    return (
        f"ℹ️ Issue at line {line}\n"
        f"Type: {issue_type}\n"
        f"Details: {msg}"
    )