def compute_score(issue):
    """
    Advanced scoring system (normalized + severity-aware)
    """

    base_scores = {
        "syntax_error": 1.0,
        "runtime_error": 0.92,
        "undefined_variable": 0.87,
        "used_before_assignment": 0.89,
        "name_error": 0.83,
        "type_error": 0.78,
        "import_error": 0.75,
        "warning": 0.45
    }

    issue_type = issue.get("type", "warning")
    score = base_scores.get(issue_type, 0.4)

    # ================= BOOST LOGIC =================

    # runtime error boost (context-aware)
    if issue_type == "runtime_error":
        if issue.get("msg"):
            score += 0.03
        if issue.get("line"):
            score += 0.01

    # undefined variable stronger penalty
    if issue_type == "undefined_variable":
        if issue.get("var"):
            score += 0.04

    # syntax errors = always max priority
    if issue_type == "syntax_error":
        score = 1.0

    # name error boost if frequent
    if issue_type == "name_error":
        if issue.get("count", 1) > 1:
            score += 0.02

    # ================= NORMALIZATION =================
    score = max(0.0, min(score, 1.0))

    return round(score, 3)


def rank_issues(issues, top_k=None):
    """
    Advanced ranking system:
    - keeps full sorted list (for dashboard)
    - optional top_k for AI chat only
    """

    if not issues:
        return []

    # assign scores
    for issue in issues:
        issue["score"] = compute_score(issue)

        # severity mapping (FIX YOUR "UNKNOWN RISK" ISSUE)
        if issue["score"] >= 0.85:
            issue["severity"] = "HIGH"
        elif issue["score"] >= 0.6:
            issue["severity"] = "MEDIUM"
        else:
            issue["severity"] = "LOW"

    # sort by score
    sorted_issues = sorted(
        issues,
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    # IMPORTANT FIX:
    # If top_k is None → return full list (for dashboard)
    if top_k is None:
        return sorted_issues

    return sorted_issues[:top_k]