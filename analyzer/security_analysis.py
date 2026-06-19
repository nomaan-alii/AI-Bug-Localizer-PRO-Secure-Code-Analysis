def analyze_security(code):
    issues = []

    code_lower = code.lower()

    # 🔴 Code Injection
    if "eval(" in code:
        issues.append({
            "type": "security_vulnerability",
            "subtype": "Code Injection",
            "message": "Use of eval() is dangerous",
            "score": 0.95
        })

    # 🔴 Command Injection
    if "exec(" in code:
        issues.append({
            "type": "security_vulnerability",
            "subtype": "Command Injection",
            "message": "Use of exec() is unsafe",
            "score": 0.96
        })

    # 🔴 Hardcoded secrets
    if "password" in code_lower or "api_key" in code_lower:
        issues.append({
            "type": "security_vulnerability",
            "subtype": "Hardcoded Secret",
            "message": "Possible hardcoded credential detected",
            "score": 0.98
        })

    # 🟡 Weak hashing
    if "md5" in code_lower:
        issues.append({
            "type": "security_vulnerability",
            "subtype": "Weak Hashing",
            "message": "MD5 is insecure, use SHA-256",
            "score": 0.9
        })

    if "sha1" in code_lower:
        issues.append({
            "type": "security_vulnerability",
            "subtype": "Weak Hashing",
            "message": "SHA1 is deprecated",
            "score": 0.85
        })

    # 🟡 Unsafe randomness
    if "random.random" in code:
        issues.append({
            "type": "security_vulnerability",
            "subtype": "Weak Randomness",
            "message": "Use secrets module instead of random",
            "score": 0.8
        })

    return issues