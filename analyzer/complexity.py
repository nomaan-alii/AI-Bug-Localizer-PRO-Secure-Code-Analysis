import ast

def compute_complexity(code):
    """
    Simple code complexity checker.
    """

    try:
        tree = ast.parse(code)
    except:
        return {
            "complexity_score": 0,
            "risk": "unknown"
        }

    complexity = 1

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
            complexity += 1

    if complexity > 10:
        risk = "high"
    elif complexity > 5:
        risk = "medium"
    else:
        risk = "low"

    return {
        "complexity_score": complexity,
        "risk": risk
    }