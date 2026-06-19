"""
API Security Analyzer - Detects API vulnerabilities and misconfigurations
Focus: Rate limiting, API key management, CORS, input validation, versioning
"""

import re
from typing import List, Dict, Any

class APISecurityAnalyzer:
    """Analyze API security vulnerabilities"""
    
    def __init__(self):
        self.name = "API Security"
        self.severity_levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for API security issues"""
        issues = []
        
        issues.extend(self._check_rate_limiting(code))
        issues.extend(self._check_api_keys(code))
        issues.extend(self._check_api_versioning(code))
        issues.extend(self._check_cors(code))
        issues.extend(self._check_api_input_validation(code))
        issues.extend(self._check_api_authentication(code))
        issues.extend(self._check_api_logging(code))
        
        return issues
    
    def _check_rate_limiting(self, code: str) -> List[Dict]:
        """Check for rate limiting implementation"""
        issues = []
        
        if any(kw in code.lower() for kw in ['api', 'endpoint', 'route', '@app', '@bp', '@router']):
            if not any(kw in code.lower() for kw in ['rate_limit', 'throttle', 'limiter', 'ratelimit']):
                issues.append({
                    'type': 'Missing Rate Limiting',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'No rate limiting detected on API endpoints',
                    'score': 0.78,
                    'category': 'API_SECURITY',
                    'recommendation': 'Implement rate limiting using Flask-Limiter, python-ratelimit, or similar'
                })
        
        return issues
    
    def _check_api_keys(self, code: str) -> List[Dict]:
        """Check for exposed API keys"""
        issues = []
        
        patterns = [
            (r'api_key\s*=\s*["\'][\w\-]{20,}["\']', 'API key hardcoded'),
            (r'apikey\s*=\s*["\'][\w\-]{20,}["\']', 'API key hardcoded'),
            (r'bearer\s+[\w\-\.]{20,}', 'Bearer token exposed'),
            (r'authorization\s*:\s*["\']Bearer\s+[\w\-\.]{20,}', 'Authorization header hardcoded')
        ]
        
        for pattern, msg in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    'type': 'Hardcoded API Credentials',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': msg,
                    'score': 0.95,
                    'category': 'API_SECURITY',
                    'recommendation': 'Store API keys in environment variables or secure vaults'
                })
        
        return issues
    
    def _check_api_versioning(self, code: str) -> List[Dict]:
        """Check for API versioning"""
        issues = []
        
        if 'api' in code.lower() and ('@app' in code or '@router' in code or '@bp' in code):
            if not any(kw in code.lower() for kw in ['/v1', '/v2', 'api_version', 'version']):
                issues.append({
                    'type': 'Missing API Versioning',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'API does not use versioning (e.g., /v1, /v2)',
                    'score': 0.55,
                    'category': 'API_SECURITY',
                    'recommendation': 'Implement API versioning to manage breaking changes safely'
                })
        
        return issues
    
    def _check_cors(self, code: str) -> List[Dict]:
        """Check CORS configuration"""
        issues = []
        
        if 'cors' in code.lower():
            if 'allow_origins' in code and '*' in code:
                issues.append({
                    'type': 'Overly Permissive CORS',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'CORS allows all origins (*) - potential security risk',
                    'score': 0.82,
                    'category': 'API_SECURITY',
                    'recommendation': 'Restrict CORS to specific trusted domains instead of "*"'
                })
        elif 'allow_origin' in code and '*' in code:
            issues.append({
                'type': 'Overly Permissive CORS',
                'severity': 'HIGH',
                'line': 0,
                'msg': 'CORS allows all origins - restrict to specific domains',
                'score': 0.82,
                'category': 'API_SECURITY',
                'recommendation': 'Use specific domain whitelist for CORS'
            })
        
        return issues
    
    def _check_api_input_validation(self, code: str) -> List[Dict]:
        """Check API input validation"""
        issues = []
        
        patterns = [
            (r'request\.args\.get\(\w+\)', 'Query parameter used without validation'),
            (r'request\.form\.get\(\w+\)', 'Form data used without validation'),
            (r'request\.json\.get\(\w+\)', 'JSON input used without validation')
        ]
        
        for pattern, msg in patterns:
            if re.search(pattern, code):
                if not any(kw in code.lower() for kw in ['validate', 'sanitize', 'schema', 'pydantic']):
                    issues.append({
                        'type': 'Missing Input Validation',
                        'severity': 'HIGH',
                        'line': 0,
                        'msg': msg,
                        'score': 0.85,
                        'category': 'API_SECURITY',
                        'recommendation': 'Use validation libraries like Pydantic or marshmallow'
                    })
                    break
        
        return issues
    
    def _check_api_authentication(self, code: str) -> List[Dict]:
        """Check API authentication"""
        issues = []
        
        if any(kw in code.lower() for kw in ['@route', '@app.route', '@bp.route', '@api']):
            if not any(kw in code.lower() for kw in ['auth', 'token', 'jwt', 'require_login', '@login_required']):
                issues.append({
                    'type': 'Unauthenticated API Endpoint',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': 'API endpoint appears to lack authentication',
                    'score': 0.90,
                    'category': 'API_SECURITY',
                    'recommendation': 'Add authentication (JWT, OAuth, API Key) to all endpoints'
                })
        
        return issues
    
    def _check_api_logging(self, code: str) -> List[Dict]:
        """Check API logging and monitoring"""
        issues = []
        
        if any(kw in code.lower() for kw in ['@route', '@app.route', '@bp.route', 'api']):
            if 'log' not in code.lower():
                issues.append({
                    'type': 'Missing API Logging',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'No logging detected for API endpoints',
                    'score': 0.65,
                    'category': 'API_SECURITY',
                    'recommendation': 'Implement comprehensive logging for audit trails and monitoring'
                })
        
        return issues
