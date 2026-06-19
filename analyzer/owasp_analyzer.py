# OWASP Top 10 Vulnerability Analyzer
import re
from typing import List, Dict, Any

class OWASPAnalyzer:
    """Detect OWASP Top 10 vulnerabilities in code"""
    
    def __init__(self):
        self.vulnerabilities = []
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for OWASP vulnerabilities"""
        issues = []
        
        # A1: Injection (SQL, Command)
        issues.extend(self._check_sql_injection(code))
        issues.extend(self._check_command_injection(code))
        
        # A2: Broken Authentication
        issues.extend(self._check_weak_auth(code))
        
        # A3: Sensitive Data Exposure
        issues.extend(self._check_hardcoded_secrets(code))
        
        # A4: XML External Entity (XXE)
        issues.extend(self._check_xxe(code))
        
        # A5: Broken Access Control
        issues.extend(self._check_access_control(code))
        
        # A6: Security Misconfiguration
        issues.extend(self._check_misconfig(code))
        
        # A7: Cross-Site Scripting (XSS)
        issues.extend(self._check_xss(code))
        
        # A8: Insecure Deserialization
        issues.extend(self._check_deserialization(code))
        
        # A9: Using Components with Known Vulnerabilities
        issues.extend(self._check_known_vulns(code))
        
        # A10: Insufficient Logging & Monitoring
        issues.extend(self._check_logging(code))
        
        return issues
    
    def _check_sql_injection(self, code: str) -> List[Dict]:
        issues = []
        patterns = [
            r'execute\s*\(\s*["\'].*\{\}.*["\']',
            r'query\s*\(\s*["\'].*\+',
            r'sql\s*=\s*["\'].*\+.*["\']',
            r'f["\'].*SELECT.*\{',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'SQL Injection',
                        'severity': 'CRITICAL',
                        'line': i,
                        'msg': 'Potential SQL injection vulnerability - use parameterized queries',
                        'score': 0.95,
                        'category': 'OWASP',
                        'recommendation': 'Use prepared statements or ORM frameworks'
                    })
        
        return issues
    
    def _check_command_injection(self, code: str) -> List[Dict]:
        issues = []
        patterns = [
            r'os\.system\s*\(',
            r'subprocess\.Popen\s*\(',
            r'exec\s*\(',
            r'eval\s*\(',
            r'shell\s*=\s*True'
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'Command Injection',
                        'severity': 'CRITICAL',
                        'line': i,
                        'msg': 'Dangerous command execution - vulnerable to injection',
                        'score': 0.92,
                        'category': 'OWASP',
                        'recommendation': 'Use parameterized calls instead of shell=True'
                    })
        
        return issues
    
    def _check_weak_auth(self, code: str) -> List[Dict]:
        issues = []
        patterns = [
            r'password\s*==\s*["\']',
            r'if\s+.*pass',
            r'hardcoded.*auth',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            if 'password' in line.lower() and ('==' in line or '=' in line):
                if any(char in line for char in ['"', "'"]):
                    issues.append({
                        'type': 'Weak Authentication',
                        'severity': 'HIGH',
                        'line': i,
                        'msg': 'Hardcoded credentials detected',
                        'score': 0.88,
                        'category': 'OWASP',
                        'recommendation': 'Use environment variables or secure credential storage'
                    })
        
        return issues
    
    def _check_hardcoded_secrets(self, code: str) -> List[Dict]:
        issues = []
        secret_patterns = [
            r'api_?key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'Hardcoded Secrets',
                        'severity': 'CRITICAL',
                        'line': i,
                        'msg': 'Sensitive data hardcoded in source',
                        'score': 0.96,
                        'category': 'OWASP',
                        'recommendation': 'Move to .env file or secret management system'
                    })
        
        return issues
    
    def _check_xxe(self, code: str) -> List[Dict]:
        issues = []
        xxe_patterns = [
            r'xml\.etree\.ElementTree',
            r'lxml\.etree',
            r'minidom\.parse',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in xxe_patterns:
                if re.search(pattern, line):
                    if 'defusedxml' not in code:
                        issues.append({
                            'type': 'XXE Vulnerability',
                            'severity': 'HIGH',
                            'line': i,
                            'msg': 'XML parsing without XXE protection',
                            'score': 0.85,
                            'category': 'OWASP',
                            'recommendation': 'Use defusedxml library'
                        })
        
        return issues
    
    def _check_access_control(self, code: str) -> List[Dict]:
        issues = []
        
        if 'permission' not in code.lower() and 'role' not in code.lower():
            # No access control checks visible
            if any(x in code.lower() for x in ['def handle', 'def process', '@app.route']):
                issues.append({
                    'type': 'Broken Access Control',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'No access control/authorization checks detected',
                    'score': 0.80,
                    'category': 'OWASP',
                    'recommendation': 'Implement role-based access control'
                })
        
        return issues
    
    def _check_misconfig(self, code: str) -> List[Dict]:
        issues = []
        
        patterns = [
            r'debug\s*=\s*True',
            r'SECRET_KEY.*=.*["\'].*["\']',
            r'ALLOWED_HOSTS\s*=\s*\[.*\*',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'Security Misconfiguration',
                        'severity': 'HIGH',
                        'line': i,
                        'msg': 'Insecure configuration detected',
                        'score': 0.78,
                        'category': 'OWASP',
                        'recommendation': 'Use environment-specific secure configs'
                    })
        
        return issues
    
    def _check_xss(self, code: str) -> List[Dict]:
        issues = []
        xss_patterns = [
            r'render_template_string\(',
            r'\.format\(',
            r'eval\(',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in xss_patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'XSS Vulnerability',
                        'severity': 'HIGH',
                        'line': i,
                        'msg': 'Potential XSS vulnerability - user input not escaped',
                        'score': 0.82,
                        'category': 'OWASP',
                        'recommendation': 'Escape output or use auto-escaping templates'
                    })
        
        return issues
    
    def _check_deserialization(self, code: str) -> List[Dict]:
        issues = []
        patterns = [
            r'pickle\.loads',
            r'yaml\.load',
            r'json\.loads.*user',
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'Insecure Deserialization',
                        'severity': 'HIGH',
                        'line': i,
                        'msg': 'Unsafe deserialization of untrusted data',
                        'score': 0.88,
                        'category': 'OWASP',
                        'recommendation': 'Use safe deserialization methods'
                    })
        
        return issues
    
    def _check_known_vulns(self, code: str) -> List[Dict]:
        # This would require a vulnerability database
        return []
    
    def _check_logging(self, code: str) -> List[Dict]:
        issues = []
        
        if 'logging' not in code and 'log' not in code.lower():
            issues.append({
                'type': 'Insufficient Logging',
                'severity': 'MEDIUM',
                'line': 0,
                'msg': 'No logging or monitoring detected',
                'score': 0.65,
                'category': 'OWASP',
                'recommendation': 'Implement comprehensive logging'
            })
        
        return issues
