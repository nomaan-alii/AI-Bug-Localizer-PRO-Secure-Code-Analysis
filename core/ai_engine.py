from analyzer.static_analysis import analyze_ast
from analyzer.runtime_analysis import run_code
from analyzer.complexity import compute_complexity
from ml.scoring import rank_issues
from analyzer.code_corrector import apply_basic_fixes


def analyze_code(code):
    """
    Central AI pipeline (used for testing + orchestration)
    Enhanced version: safer + AI-ready + extensible
    """

    # ================= SAFETY CHECK =================
    if not code or not code.strip():
        return {
            "code": "",
            "issues": [],
            "complexity": {
                "complexity_score": 0,
                "risk": "LOW",
                "security_flag": False
            },
            "meta": {
                "status": "empty_input",
                "issue_count": 0
            }
        }

    try:

        # ================= COMPLEXITY =================
        complexity = compute_complexity(code) or {}

        # ================= STATIC + RUNTIME ANALYSIS =================
        ast_issues = analyze_ast(code) or []
        runtime_issues = run_code(code) or []

        # ================= ISSUE MERGING (SAFE) =================
        all_issues = []

        if isinstance(ast_issues, list):
            all_issues.extend(ast_issues)

        if isinstance(runtime_issues, list):
            all_issues.extend(runtime_issues)

        # ================= ML RANKING =================
        issues = rank_issues(all_issues, top_k=None) if all_issues else []

        # ================= SECURITY FLAG (AI READY HOOK) =================
        security_flag = any(
            i.get("type") == "security_vulnerability"
            for i in issues
        )

        # attach severity normalization (future AI use)
        for issue in issues:
            score = issue.get("score", 0)

            issue["severity"] = (
                "critical" if score >= 0.85
                else "high" if score >= 0.6
                else "low"
            )

        # ================= AUTO FIX ENGINE =================
        fixed_code = apply_basic_fixes(code) if issues else code

        # ================= COMPLEXITY ENRICHMENT =================
        complexity["security_flag"] = security_flag

        risk_score = complexity.get("complexity_score", 0)

        complexity["risk"] = (
            "HIGH" if security_flag or risk_score >= 70
            else "MEDIUM" if risk_score >= 40
            else "LOW"
        )

        # ================= FINAL OUTPUT =================
        return {
            "code": code,
            "issues": issues,
            "fixed": fixed_code,
            "complexity": complexity,

            # ================= AI EXTENSION LAYER =================
            "meta": {
                "issue_count": len(issues),
                "security_issues": sum(
                    1 for i in issues
                    if i.get("type") == "security_vulnerability"
                ),
                "runtime_issues": sum(
                    1 for i in issues
                    if i.get("type") == "runtime_error"
                ),
                "ast_issues": len(ast_issues),
                "status": "analyzed_successfully"
            }
        }

    except Exception as e:

        # ================= FAILSAFE =================
        return {
            "code": code,
            "issues": [],
            "complexity": {
                "complexity_score": 0,
                "risk": "UNKNOWN",
                "security_flag": False
            },
            "fixed": code,
            "meta": {
                "status": "error",
                "error": str(e)
            }
        }