def suggest_fix(issue):
    """
    Improved fix suggestion engine.
    Structured + consistent + extensible.
    """

    issue_type = issue.get("type", "unknown")
    var = issue.get("var", "")
    msg = issue.get("msg", "")
    line = issue.get("line", "unknown")

    # ---------------- SYNTAX ERROR ----------------
    if issue_type == "syntax_error":
        return (
            "🔧 Fix Syntax Error:\n"
            "- Check missing ':' or brackets\n"
            "- Fix indentation at line "
            f"{line}\n"
            f"- Details: {msg}"
        )

    # ---------------- UNDEFINED VARIABLE ----------------
    if issue_type == "undefined_variable":
        return (
            f"🔧 Fix '{var}':\n"
            "- Define variable before using it\n"
            "- Check spelling mistakes\n"
            f"- Example: {var} = 0"
        )

    # ---------------- RUNTIME ERROR ----------------
    if issue_type.startswith("runtime_error"):
        return (
            "🔧 Fix Runtime Error:\n"
            f"- Error: {msg}\n"
            "- Check invalid operations\n"
            "- Check data types\n"
            "- Verify input values"
        )

    # ---------------- SECURITY ISSUES ----------------
    if issue.get("subtype") == "Code Injection":
        return "Avoid eval(). Use ast.literal_eval()"

    if issue.get("subtype") == "Command Injection":
        return "Avoid exec(). Use safer alternatives"

    if issue.get("subtype") == "Weak Hashing":
        return "Use hashlib.sha256() instead of MD5/SHA1"

    if issue.get("subtype") == "Hardcoded Secret":
        return "Move secrets to environment variables"

    # ---------------- FALLBACK ----------------
    return (
        "🔧 General Fix:\n"
        "- Review logic\n"
        "- Check variable usage\n"
        f"- Issue type: {issue_type}"
    )