import ast


def check_syntax(code):
    """
    Detect syntax errors safely
    """
    try:
        ast.parse(code)
        return {"status": "OK", "error": None}
    except SyntaxError as e:
        return {
            "status": "ERROR",
            "error": f"{e.msg} (line {e.lineno})"
        }


def calculate_code_rating(issues, syntax_ok=True):
    """
    Convert issues into 0–10 rating
    """

    if not syntax_ok:
        return 3.0  # heavy penalty for syntax error

    base = 10.0

    for issue in issues:
        score = issue.get("score", 0)

        # penalty system
        if score >= 0.85:
            base -= 2.0
        elif score >= 0.6:
            base -= 1.0
        else:
            base -= 0.3

    return round(max(0, min(base, 10)), 2)


def build_quality_report(code, issues):
    """
    Final structured report
    """

    syntax = check_syntax(code)
    rating = calculate_code_rating(
        issues,
        syntax_ok=(syntax["status"] == "OK")
    )

    risk = "LOW"

    if rating < 4:
        risk = "HIGH"
    elif rating < 7:
        risk = "MEDIUM"

    return {
        "syntax_status": syntax["status"],
        "syntax_error": syntax["error"],
        "rating": rating,
        "risk": risk
    }