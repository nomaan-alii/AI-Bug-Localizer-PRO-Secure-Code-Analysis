# ui/components.py
import streamlit as st
from typing import Dict, Any, List

def get_severity_color(score: float) -> tuple:
    """Return severity label, emoji, color and CSS class."""
    if score >= 0.85:
        return "CRITICAL", "🔴", "#ef4444", "critical"
    elif score >= 0.7:
        return "HIGH", "🟠", "#f59e0b", "high"
    elif score >= 0.5:
        return "MEDIUM", "🟡", "#3b82f6", "medium"
    else:
        return "LOW", "🟢", "#10b981", "low"

def get_category_icon(category: str) -> str:
    """Return icon for category."""
    icons = {
        "OWASP": "🛡️",
        "CRYPTO": "🔐",
        "COMPLIANCE": "📋",
        "AUTH": "🔑",
        "BUG": "🐛",
        "PERF": "⚡",
    }
    return icons.get(category, "📌")

def render_issue_card(issue: Dict[str, Any], index: int):
    """Render a professional issue card."""
    score = issue.get("score", 0)
    issue_type = issue.get("type", "unknown")
    line = issue.get("line", "N/A")
    category = issue.get("category", "BUG")
    severity_name, emoji, color, css_class = get_severity_color(score)
    
    # Professional card layout
    col1, col2, col3 = st.columns([0.8, 3, 1.2])
    
    with col1:
        st.markdown(f"<div style='text-align: center; padding: 10px;'>{emoji}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div style='padding: 5px;'><b>{issue_type}</b><br/><small>Line {line} • {get_category_icon(category)} {category}</small></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div style='text-align: right; padding: 5px;'><span class='badge-{css_class}'>{severity_name}</span><br/><small>Risk: {round(score*100)}%</small></div>", unsafe_allow_html=True)
    
    # Expandable details
    with st.expander("📖 Details & Recommendations"):
        col_msg, col_rec = st.columns(2)
        
        with col_msg:
            if "msg" in issue:
                st.info(f"**Issue:**\n{issue['msg']}")
        
        with col_rec:
            if "recommendation" in issue:
                st.success(f"**Fix:**\n{issue['recommendation']}")
        
        # Additional details
        if "var" in issue:
            st.warning(f"**Variable:** `{issue['var']}`")

def render_security_dashboard(security_issues: List[Dict]):
    """Render security analysis dashboard."""
    st.markdown("### 🛡️ Security Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    critical = len([i for i in security_issues if i.get("severity") == "CRITICAL"])
    high = len([i for i in security_issues if i.get("severity") == "HIGH"])
    medium = len([i for i in security_issues if i.get("severity") == "MEDIUM"])
    low = len([i for i in security_issues if i.get("severity") == "LOW"])
    
    with col1:
        st.metric("🔴 Critical", critical, delta=None)
    with col2:
        st.metric("🟠 High", high, delta=None)
    with col3:
        st.metric("🟡 Medium", medium, delta=None)
    with col4:
        st.metric("🟢 Low", low, delta=None)

def render_compliance_checker(compliance_issues: List[Dict]):
    """Render compliance status."""
    st.markdown("### 📋 Compliance Status")
    
    if not compliance_issues:
        st.success("✅ No compliance issues detected!")
        return
    
    standards = {}
    for issue in compliance_issues:
        standard = issue.get("type", "").split(":")[0]
        if standard not in standards:
            standards[standard] = []
        standards[standard].append(issue)
    
    for standard, issues in standards.items():
        with st.expander(f"📌 {standard}"):
            for issue in issues:
                severity_name, emoji, _, _ = get_severity_color(issue.get("score", 0))
                st.markdown(f"{emoji} **{issue.get('msg')}**")
                st.caption(f"Recommendation: {issue.get('recommendation', 'N/A')}")

def render_header():
    """Render professional header."""
    st.markdown("""
    <div class="header-card">
        <h1>🧠 AI Bug Localizer PRO</h1>
        <p>Advanced Code Analysis with Security & Compliance Intelligence</p>
        <small>⚡ Powered by ML • 🛡️ Security Focused • 📋 Compliance Ready</small>
    </div>
    """, unsafe_allow_html=True)


def show_results(issues):
    """
    Display all issues in structured format.
    """

    if not issues:
        st.success("🎉 No major issues found!")
        return

    st.subheader("🔍 Bug Analysis Report")

    for i, issue in enumerate(issues, 1):
        show_issue(issue, i)