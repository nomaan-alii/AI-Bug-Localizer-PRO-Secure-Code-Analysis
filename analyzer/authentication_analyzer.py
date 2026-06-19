# Authentication & Authorization Analyzer
import re
from typing import List, Dict, Any

class AuthenticationAnalyzer:
    """Analyze authentication and authorization implementation"""
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for auth issues"""
        issues = []
        
        issues.extend(self._check_password_strength(code))
        issues.extend(self._check_session_management(code))
        issues.extend(self._check_mfa(code))
        issues.extend(self._check_token_security(code))
        issues.extend(self._check_oauth(code))
        
        return issues
    
    def _check_password_strength(self, code: str) -> List[Dict]:
        issues = []
        
        # Check for weak password validation
        if re.search(r'len\(.*password.*\)\s*<\s*[0-8]', code):
            issues.append({
                'type': 'Weak Password Policy',
                'severity': 'HIGH',
                'line': 0,
                'msg': 'Password minimum length less than 8 characters',
                'score': 0.80,
                'category': 'AUTH',
                'recommendation': 'Enforce minimum 12 character passwords'
            })
        
        # Check for password validation
        if 'password' in code.lower():
            if not any(x in code.lower() for x in ['regex', 'pattern', 'validate', 'check']):
                issues.append({
                    'type': 'No Password Validation',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'No password complexity validation detected',
                    'score': 0.72,
                    'category': 'AUTH',
                    'recommendation': 'Require uppercase, lowercase, numbers, and special chars'
                })
        
        return issues
    
    def _check_session_management(self, code: str) -> List[Dict]:
        issues = []
        
        # Check for session timeout
        if 'session' in code.lower():
            if 'timeout' not in code.lower() and 'expire' not in code.lower():
                issues.append({
                    'type': 'No Session Timeout',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'Session timeout not implemented',
                    'score': 0.70,
                    'category': 'AUTH',
                    'recommendation': 'Implement 15-30 minute session timeout'
                })
        
        # Check for secure cookie flags
        patterns = [
            (r'Set-Cookie.*Secure', True),
            (r'Set-Cookie.*HttpOnly', True),
            (r'Set-Cookie.*SameSite', True),
        ]
        
        if 'cookie' in code.lower():
            for pattern, required in patterns:
                if not re.search(pattern, code):
                    issues.append({
                        'type': 'Insecure Cookie',
                        'severity': 'HIGH',
                        'line': 0,
                        'msg': f'Missing cookie security flag: {pattern}',
                        'score': 0.83,
                        'category': 'AUTH',
                        'recommendation': 'Set Secure, HttpOnly, and SameSite flags'
                    })
        
        return issues
    
    def _check_mfa(self, code: str) -> List[Dict]:
        issues = []
        
        # Check for multi-factor authentication
        if 'login' in code.lower() or 'authenticate' in code.lower():
            if 'mfa' not in code.lower() and 'otp' not in code.lower() and '2fa' not in code.lower():
                issues.append({
                    'type': 'No Multi-Factor Auth',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'Multi-factor authentication not implemented',
                    'score': 0.75,
                    'category': 'AUTH',
                    'recommendation': 'Implement TOTP or SMS-based MFA'
                })
        
        return issues
    
    def _check_token_security(self, code: str) -> List[Dict]:
        issues = []
        
        # Check for JWT security
        if 'jwt' in code.lower() or 'token' in code.lower():
            # Check for algorithm specification
            if 'algorithm' not in code.lower():
                issues.append({
                    'type': 'JWT: No Algorithm Specified',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'JWT without explicit algorithm specification',
                    'score': 0.85,
                    'category': 'AUTH',
                    'recommendation': 'Specify algorithm (RS256, HS256) explicitly'
                })
            
            # Check for token expiration
            if 'exp' not in code.lower() and 'expir' not in code.lower():
                issues.append({
                    'type': 'JWT: No Expiration',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'JWT tokens without expiration time',
                    'score': 0.84,
                    'category': 'AUTH',
                    'recommendation': 'Add exp claim with reasonable TTL'
                })
            
            # Check for secret key strength
            if re.search(r'secret\s*=\s*["\'][^"\']{0,15}["\']', code):
                issues.append({
                    'type': 'Weak JWT Secret',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': 'JWT secret key is too short',
                    'score': 0.90,
                    'category': 'AUTH',
                    'recommendation': 'Use at least 256-bit keys'
                })
        
        return issues
    
    def _check_oauth(self, code: str) -> List[Dict]:
        issues = []
        
        if 'oauth' in code.lower():
            # Check for state parameter
            if 'state' not in code.lower():
                issues.append({
                    'type': 'OAuth: Missing State Parameter',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'OAuth flow missing CSRF protection (state parameter)',
                    'score': 0.88,
                    'category': 'AUTH',
                    'recommendation': 'Implement state parameter for CSRF protection'
                })
            
            # Check for PKCE
            if 'code_challenge' not in code.lower():
                issues.append({
                    'type': 'OAuth: No PKCE',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'OAuth flow without PKCE for native apps',
                    'score': 0.72,
                    'category': 'AUTH',
                    'recommendation': 'Use PKCE for mobile/desktop apps'
                })
        
        return issues
