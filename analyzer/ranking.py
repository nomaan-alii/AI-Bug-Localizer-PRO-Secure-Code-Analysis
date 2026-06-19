from ml.scoring import rank_issues as ml_rank_issues


def rank_issues(issues):
    """
    Wrapper only (no logic here)
    Keeps compatibility with app.py
    """

    return ml_rank_issues(issues)