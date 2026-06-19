import ast

BUILTINS = set(dir(__builtins__))


def analyze_ast(code):
    """
    Improved AST analyzer (clean + pipeline-ready)

    Detects:
    - Syntax errors
    - Undefined variables (basic level)
    """

    issues = []
    defined = set()
    seen = set()

    # ---------------- SYNTAX CHECK ----------------
    try:
        tree = ast.parse(code)

    except SyntaxError as e:
        return [{
            "line": e.lineno or 0,
            "type": "syntax_error",
            "msg": e.msg,
            "var": None,
            "score": 0.95
        }]

    # ---------------- AST TRAVERSAL ----------------
    for node in ast.walk(tree):

        if isinstance(node, ast.Name):
            name = node.id
            line = getattr(node, "lineno", 0)

            # ignore built-ins
            if name in BUILTINS:
                continue

            # variable assignment
            if isinstance(node.ctx, ast.Store):
                defined.add(name)

            # variable usage
            elif isinstance(node.ctx, ast.Load):

                # undefined variable detection
                if name not in defined:

                    key = (name, line)

                    if key not in seen:
                        seen.add(key)

                        issues.append({
                            "line": line,
                            "type": "undefined_variable",
                            "msg": f"Variable '{name}' used before assignment",
                            "var": name,
                            "score": 0.85
                        })

    return issues