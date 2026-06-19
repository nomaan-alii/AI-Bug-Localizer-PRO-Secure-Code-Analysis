from analyzer.code_corrector import apply_basic_fixes


def detect_intent(text):
    text = text.lower()

    if "fix" in text:
        return "fix"

    if "explain" in text or "why" in text:
        return "explain"

    if "security" in text:
        return "security"

    if "complexity" in text:
        return "complexity"

    if "summary" in text:
        return "summary"

    return "general"


def get_top_issue(issues):
    if not issues:
        return None

    return max(issues, key=lambda x: x.get("score", 0))


def copilot_brain_engine(user_input, analysis_data):

    if not analysis_data:
        return "Run code analysis first."

    issues = analysis_data.get("issues", [])
    complexity = analysis_data.get("complexity", {})
    code = analysis_data.get("code", "")

    intent = detect_intent(user_input)

    # ================= FIX =================
    if intent == "fix":
        top = get_top_issue(issues)

        if not top:
            return "No issues found."

        return f"""
🛠️ AI FIX ENGINE

Issue: {top.get('type')}
Score: {top.get('score')}

Fix:
{apply_basic_fixes(code)}
"""

    # ================= EXPLAIN =================
    if intent == "explain":
        top = get_top_issue(issues)

        if not top:
            return "No issues to explain."

        return f"""
🧠 EXPLANATION

Problem: {top.get('type')}

Why it happens:
Bad patterns, unsafe logic, or runtime errors.

Score: {top.get('score')}

Fix:
{apply_basic_fixes(code)}
"""

    # ================= SECURITY =================
    if intent == "security":
        sec = [i for i in issues if i.get("type") == "security_vulnerability"]

        if not sec:
            return "🟢 No security issues found"

        return "\n\n".join(
            [f"{i.get('message')} (score: {i.get('score')})" for i in sec]
        )

    # ================= COMPLEXITY =================
    if intent == "complexity":
        return f"""
📊 COMPLEXITY REPORT

Score: {complexity.get('complexity_score', 0)}
Risk: {complexity.get('risk', 'LOW')}
"""

    # ================= SUMMARY =================
    if intent == "summary":
        return f"""
📋 SUMMARY

Total Issues: {len(issues)}
Complexity: {complexity.get('complexity_score', 0)}
Risk: {complexity.get('risk', 'LOW')}
"""

    # ================= DEFAULT =================
    return """
🤖 Copilot Brain Ready

Try:
• fix
• explain
• security
• complexity
• summary
"""