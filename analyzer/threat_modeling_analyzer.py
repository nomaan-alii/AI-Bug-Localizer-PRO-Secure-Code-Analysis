"""
Threat Modeling Analyzer - Identifies potential threat vectors and attack surfaces
Focus: Data flow, trust boundaries, access control, privilege escalation
"""

import re
from typing import List, Dict, Any

class ThreatModelingAnalyzer:
    """Analyze code for threat modeling and attack surfaces"""
    
    def __init__(self):
        self.name = "Threat Modeling"
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for threat vectors"""
        issues = []
        
        issues.extend(self._check_privilege_escalation(code))
        issues.extend(self._check_data_exposure(code))
        issues.extend(self._check_access_control(code))
        issues.extend(self._check_error_handling(code))
        issues.extend(self._check_cryptographic_weaknesses(code))
        
        return issues
    
    def _check_privilege_escalation(self, code: str) -> List[Dict]:
        """Check for privilege escalation risks"""
        issues = []
        
        # Check for use of sudo or elevated privileges
        if 'sudo' in code or 'root' in code.lower():
            if 'os.getuid' not in code and 'os.geteuid' not in code:
                issues.append({
                    'type': 'Potential Privilege Escalation',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'Code uses sudo or root without privilege checks',
                    'score': 0.80,
                    'category': 'THREAT_MODEL',
                    'recommendation': 'Implement privilege validation and least privilege principle'
                })
        
        # Check for unsafe file permissions
        if 'chmod' in code.lower():
            if re.search(r'0o777|0777|chmod.*["\']?777["\']?', code, re.IGNORECASE):
                issues.append({
                    'type': 'Insecure File Permissions',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'Files created with overly permissive permissions (777)',
                    'score': 0.82,
                    'category': 'THREAT_MODEL',
                    'recommendation': 'Use restrictive file permissions (e.g., 0o600 or 0o755)'
                })
        
        return issues
    
    def _check_data_exposure(self, code: str) -> List[Dict]:
        """Check for data exposure risks"""
        issues = []
        
        # Check for unencrypted data storage
        if any(kw in code.lower() for kw in ['database', 'file', 'cache', 'session']):
            if not any(kw in code.lower() for kw in ['encrypt', 'cipher', 'fernet', 'aes']):
                if any(kw in code.lower() for kw in ['password', 'credit', 'ssn', 'personal', 'secret']):
                    issues.append({
                        'type': 'Unencrypted Sensitive Data',
                        'severity': 'CRITICAL',
                        'line': 0,
                        'msg': 'Sensitive data stored without encryption',
                        'score': 0.92,
                        'category': 'THREAT_MODEL',
                        'recommendation': 'Encrypt sensitive data at rest using strong algorithms'
                    })
        
        # Check for data in memory/memory dumps
        if 'password' in code.lower() or 'token' in code.lower():
            if 'clear' not in code.lower() and 'delete' not in code.lower():
                issues.append({
                    'type': 'Data Retention Risk',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'Sensitive data might persist in memory',
                    'score': 0.65,
                    'category': 'THREAT_MODEL',
                    'recommendation': 'Clear sensitive data from memory after use'
                })
        
        return issues
    
    def _check_access_control(self, code: str) -> List[Dict]:
        """Check for access control vulnerabilities"""
        issues = []
        
        # Check for missing authorization checks
        if any(kw in code.lower() for kw in ['@route', '@app', 'def delete_', 'def remove_', 'def update_']):
            if not any(kw in code.lower() for kw in ['auth', 'permission', 'role', 'admin', 'owner']):
                issues.append({
                    'type': 'Missing Authorization Check',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'Resource modification without authorization check',
                    'score': 0.84,
                    'category': 'THREAT_MODEL',
                    'recommendation': 'Implement role-based or attribute-based access control'
                })
        
        # Check for IDOR (Insecure Direct Object Reference)
        if re.search(r'\.get\s*\(\s*id\s*\)|id\s*=\s*request', code, re.IGNORECASE):
            if not any(kw in code.lower() for kw in ['current_user', 'owner', 'permission', 'check_access']):
                issues.append({
                    'type': 'IDOR Vulnerability Risk',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'Direct object reference without ownership verification',
                    'score': 0.86,
                    'category': 'THREAT_MODEL',
                    'recommendation': 'Verify user owns/can access the resource before returning it'
                })
        
        return issues
    
    def _check_error_handling(self, code: str) -> List[Dict]:
        """Check for information disclosure through error handling"""
        issues = []
        
        # Check for bare except
        if re.search(r'except\s*:\s', code):
            issues.append({
                'type': 'Overly Broad Exception Handling',
                'severity': 'MEDIUM',
                'line': 0,
                'msg': 'Bare except clause might hide security issues',
                'score': 0.60,
                'category': 'THREAT_MODEL',
                'recommendation': 'Catch specific exceptions and log them securely'
            })
        
        # Check for information disclosure in error messages
        if 'exception' in code.lower() or 'error' in code.lower():
            if not any(kw in code.lower() for kw in ['sanitize', 'generic', 'hide']):
                if any(kw in code.lower() for kw in ['traceback', 'stack', 'sql']):
                    issues.append({
                        'type': 'Information Disclosure',
                        'severity': 'MEDIUM',
                        'line': 0,
                        'msg': 'Error messages might expose sensitive information',
                        'score': 0.72,
                        'category': 'THREAT_MODEL',
                        'recommendation': 'Show generic errors to users, log details securely'
                    })
        
        return issues
    
    def _check_cryptographic_weaknesses(self, code: str) -> List[Dict]:
        """Check for cryptographic weaknesses"""
        issues = []
        
        # Check for custom crypto implementation
        if any(kw in code.lower() for kw in ['def encrypt', 'def decrypt', 'def hash']):
            if not any(kw in code.lower() for kw in ['cryptography', 'pycryptodome', 'nacl']):
                issues.append({
                    'type': 'Custom Cryptography Implementation',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': 'Custom cryptographic implementation detected',
                    'score': 0.95,
                    'category': 'THREAT_MODEL',
                    'recommendation': 'Use well-tested cryptographic libraries (cryptography, nacl)'
                })
        
        # Check for hardcoded IVs or nonces
        if re.search(r'iv\s*=|nonce\s*=', code, re.IGNORECASE):
            if 'os.urandom' not in code and 'secrets.token' not in code:
                issues.append({
                    'type': 'Static IV/Nonce',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'IV or nonce might be static instead of random',
                    'score': 0.85,
                    'category': 'THREAT_MODEL',
                    'recommendation': 'Use os.urandom() or secrets module for random IV/nonce'
                })
        
        return issues
