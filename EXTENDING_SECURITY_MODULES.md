# Extending Information Security Modules

## 📚 Architecture Overview

The Information Security analysis is modular and easily extensible. Here's how the system works and how you can add new modules.

### Current Modules

```
analyzer/
├── owasp_analyzer.py              # A1-A10 vulnerabilities
├── encryption_analyzer.py         # Cryptography analysis
├── compliance_checker.py          # GDPR/HIPAA/PCI-DSS
├── authentication_analyzer.py     # Auth/AuthZ
├── security_analysis.py          # Basic security checks
├── static_analysis.py            # AST-based analysis
├── runtime_analysis.py           # Execution analysis
└── [YOUR NEW MODULE].py          # Add here!
```

### Module Structure

Each security analyzer module follows this pattern:

```python
class [AnalyzerName]:
    """Description of what this analyzer does"""
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Main analysis method - required"""
        issues = []
        issues.extend(self._check_first_thing(code))
        issues.extend(self._check_second_thing(code))
        return issues
    
    def _check_first_thing(self, code: str) -> List[Dict]:
        """Helper method to check for specific issues"""
        issues = []
        # Implementation here
        return issues
```

### Issue Dictionary Format

Each issue must follow this structure:

```python
{
    'type': 'Issue Type Name',           # Required: Category name
    'severity': 'CRITICAL|HIGH|MEDIUM',  # Required: Severity level
    'line': 1,                           # Required: Line number (0 if global)
    'msg': 'What was found',             # Required: Clear description
    'score': 0.85,                       # Required: 0.0-1.0 risk score
    'category': 'MODULE_NAME',           # Required: Module category
    'recommendation': 'How to fix',      # Optional but recommended
    'var': 'variable_name'               # Optional: Affected variable
}
```

## 🆕 Creating a New Security Module

### Example: API Security Analyzer

Here's how to create a new module:

```python
# analyzer/api_security_analyzer.py

import re
from typing import List, Dict, Any

class APISecurityAnalyzer:
    """Analyze API security vulnerabilities"""
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for API security issues"""
        issues = []
        
        issues.extend(self._check_rate_limiting(code))
        issues.extend(self._check_api_keys(code))
        issues.extend(self._check_api_versioning(code))
        issues.extend(self._check_cors(code))
        issues.extend(self._check_input_validation(code))
        
        return issues
    
    def _check_rate_limiting(self, code: str) -> List[Dict]:
        """Check for rate limiting implementation"""
        issues = []
        
        if 'api' in code.lower() or 'endpoint' in code.lower():
            if 'rate_limit' not in code.lower() and 'throttle' not in code.lower():
                issues.append({
                    'type': 'Missing Rate Limiting',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'No rate limiting detected on API endpoints',
                    'score': 0.78,
                    'category': 'API',
                    'recommendation': 'Implement rate limiting using libraries like Flask-Limiter'
                })
        
        return issues
    
    def _check_api_keys(self, code: str) -> List[Dict]:
        """Check for hardcoded API keys"""
        issues = []
        
        patterns = [
            r'api_key\s*=\s*["\'][^"\']{10,}["\']',
            r'API_KEY\s*=\s*["\'][^"\']{10,}["\']',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'Hardcoded API Key',
                        'severity': 'CRITICAL',
                        'line': i,
                        'msg': 'API key hardcoded in source',
                        'score': 0.96,
                        'category': 'API',
                        'recommendation': 'Use environment variables or secret management'
                    })
        
        return issues
    
    def _check_api_versioning(self, code: str) -> List[Dict]:
        """Check for API versioning"""
        issues = []
        
        if 'api' in code.lower():
            if '/v1' not in code and '/v2' not in code:
                issues.append({
                    'type': 'No API Versioning',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'API endpoints without versioning detected',
                    'score': 0.65,
                    'category': 'API',
                    'recommendation': 'Implement API versioning (/v1, /v2)'
                })
        
        return issues
    
    def _check_cors(self, code: str) -> List[Dict]:
        """Check CORS configuration"""
        issues = []
        
        patterns = [
            r'Access-Control-Allow-Origin.*\*',
            r'CORS.*allow.*all',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'Overly Permissive CORS',
                        'severity': 'HIGH',
                        'line': i,
                        'msg': 'CORS allows all origins (*)',
                        'score': 0.82,
                        'category': 'API',
                        'recommendation': 'Restrict CORS to specific trusted domains'
                    })
        
        return issues
    
    def _check_input_validation(self, code: str) -> List[Dict]:
        """Check for input validation"""
        issues = []
        
        if 'request' in code.lower() or 'input' in code.lower():
            if 'validate' not in code.lower() and 'schema' not in code.lower():
                issues.append({
                    'type': 'No Input Validation',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'No input validation on API endpoints',
                    'score': 0.80,
                    'category': 'API',
                    'recommendation': 'Use Pydantic or JSON Schema for validation'
                })
        
        return issues
```

### Step 2: Integrate into app.py

```python
# In app.py imports:
from analyzer.api_security_analyzer import APISecurityAnalyzer

# In cached_analysis function:
api_analyzer = APISecurityAnalyzer()
api_issues = api_analyzer.analyze(code) or []

# Add to all_issues:
all_issues = ast_issues + runtime_issues + security_issues + owasp_issues + crypto_issues + compliance_issues + auth_issues + api_issues

# Add to return dictionary:
return {
    # ... existing returns ...
    "api_issues": api_issues
}
```

### Step 3: Add to Security Lab

```python
# In app.py, Security Lab section:

api_tab = st.tabs([..., "🌐 API Security"])

with api_tab:
    st.markdown("### 🌐 API Security Analysis")
    
    if data and data.get("code"):
        api_issues = data.get("api_issues", [])
        
        if api_issues:
            for idx, issue in enumerate(api_issues, 1):
                render_issue_card(issue, idx)
        else:
            st.success("✅ No API security issues detected!")
    else:
        st.info("💡 Analyze code to check API security")
```

## 🧩 Other Module Ideas

### 1. **Database Security Analyzer**
```python
class DatabaseSecurityAnalyzer:
    - SQL injection detection
    - Connection security
    - Query logging
    - Backup procedures
```

### 2. **Cloud Security Analyzer**
```python
class CloudSecurityAnalyzer:
    - AWS security best practices
    - Azure security best practices
    - GCP security best practices
    - IAM configuration
```

### 3. **Dependency Security Analyzer**
```python
class DependencySecurityAnalyzer:
    - Known vulnerabilities in dependencies
    - Version checking
    - License compliance
    - Outdated packages
```

### 4. **Container Security Analyzer**
```python
class ContainerSecurityAnalyzer:
    - Dockerfile best practices
    - Container registry security
    - Image scanning
    - Runtime security
```

### 5. **Infrastructure Security Analyzer**
```python
class InfrastructureSecurityAnalyzer:
    - Terraform/CloudFormation security
    - Network security
    - Firewall rules
    - Load balancer configuration
```

### 6. **Mobile Security Analyzer**
```python
class MobileSecurityAnalyzer:
    - Certificate pinning
    - Secure storage
    - Input validation
    - Code obfuscation
```

### 7. **Supply Chain Security Analyzer**
```python
class SupplyChainAnalyzer:
    - Artifact signing
    - Dependency verification
    - SoftwareBOM (SBOM)
    - Provenance tracking
```

### 8. **Privacy & Data Protection Analyzer**
```python
class PrivacyAnalyzer:
    - Data minimization
    - Consent management
    - Data retention
    - Privacy by design
```

## 📊 Testing Your Module

```python
# test_your_analyzer.py

from analyzer.your_analyzer import YourAnalyzer

def test_your_analyzer():
    analyzer = YourAnalyzer()
    
    test_code = """
    # Your test code here
    hardcoded_secret = 'my_secret_key'
    """
    
    issues = analyzer.analyze(test_code)
    
    assert len(issues) > 0
    assert issues[0]['severity'] == 'CRITICAL'
    print("✅ Tests passed!")

if __name__ == "__main__":
    test_your_analyzer()
```

## 🔄 Module Integration Checklist

- [ ] Create analyzer class with `analyze()` method
- [ ] Return list of dictionaries with required fields
- [ ] Add unit tests
- [ ] Import in app.py
- [ ] Add to `cached_analysis()` function
- [ ] Create tab in Security Lab
- [ ] Update documentation
- [ ] Add to issue counter/dashboard
- [ ] Test end-to-end flow
- [ ] Update SECURITY_FEATURES.md

## 💡 Best Practices for New Modules

### 1. **Clear Naming**
```python
# Good
class SQLSecurityAnalyzer
class DatabaseConnectionAnalyzer

# Avoid
class Analyzer1
class SecCheck
```

### 2. **Focused Scope**
- One module = one security domain
- Don't mix authentication with encryption

### 3. **Comprehensive Coverage**
- Check multiple patterns within domain
- Use regular expressions for code patterns

### 4. **Accurate Scoring**
- 0.95+ = Critical vulnerability
- 0.75-0.94 = High priority
- 0.5-0.74 = Medium priority
- <0.5 = Low priority or best practice

### 5. **Actionable Recommendations**
```python
# Good
'recommendation': 'Use bcrypt.hashpw() for password hashing'

# Avoid
'recommendation': 'Fix security issue'
```

### 6. **Clear Messages**
```python
# Good
'msg': 'Password hashing without salt detected - use bcrypt'

# Avoid
'msg': 'Bad security'
```

## 🚀 Performance Considerations

- Keep regex patterns efficient
- Cache compiled patterns
- Avoid nested loops
- Use generator expressions where possible
- Profile with large codebases

## 📞 Questions?

- Review existing modules for patterns
- Check OWASP standards for guidance
- Test with real-world code samples
- Document edge cases

---

**Happy coding! 🛡️**
