"""
Secure Configuration Analyzer - Checks for insecure configurations
Focus: Database security, environment variables, secrets management, debug modes
"""

import re
from typing import List, Dict, Any

class SecureConfigurationAnalyzer:
    """Analyze secure configuration and settings"""
    
    def __init__(self):
        self.name = "Secure Configuration"
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for security configuration issues"""
        issues = []
        
        issues.extend(self._check_debug_mode(code))
        issues.extend(self._check_secret_management(code))
        issues.extend(self._check_database_config(code))
        issues.extend(self._check_logging_config(code))
        issues.extend(self._check_ssl_tls(code))
        issues.extend(self._check_security_headers(code))
        
        return issues
    
    def _check_debug_mode(self, code: str) -> List[Dict]:
        """Check if debug mode is enabled in production"""
        issues = []
        
        patterns = [
            (r'DEBUG\s*=\s*True', 'Flask/Django DEBUG=True'),
            (r'debug\s*=\s*True', 'Debug mode enabled'),
            (r'app\.run\s*\(\s*debug\s*=\s*True', 'app.run with debug=True'),
            (r'DEBUG\s*=\s*True\s*#.*production', 'Debug enabled in production'),
        ]
        
        for pattern, msg in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    'type': 'Debug Mode Enabled',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': msg,
                    'score': 0.90,
                    'category': 'CONFIG_SECURITY',
                    'recommendation': 'Disable DEBUG in production - use environment variables'
                })
        
        return issues
    
    def _check_secret_management(self, code: str) -> List[Dict]:
        """Check for proper secret management"""
        issues = []
        
        # Check for hardcoded secrets
        secret_patterns = [
            (r'PASSWORD\s*=\s*["\'][\w\!@#$%^&*]{8,}["\']', 'Hardcoded password'),
            (r'SECRET_KEY\s*=\s*["\'][\w\-\.]{20,}["\']', 'Hardcoded SECRET_KEY'),
            (r'DATABASE_URL\s*=\s*["\'].*://.*:.*@', 'Hardcoded database credentials'),
            (r'AWS_KEY\s*=\s*["\']', 'Hardcoded AWS key'),
            (r'API_SECRET\s*=\s*["\']', 'Hardcoded API secret'),
        ]
        
        for pattern, msg in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    'type': 'Hardcoded Secret',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': msg,
                    'score': 0.98,
                    'category': 'CONFIG_SECURITY',
                    'recommendation': 'Use environment variables or secret management tools'
                })
        
        # Check if secrets are properly sourced from environment
        if any(kw in code for kw in ['password', 'secret', 'key', 'token']):
            if not any(kw in code.lower() for kw in ['os.environ', 'getenv', 'dotenv', '.env']):
                issues.append({
                    'type': 'Hardcoded Credentials Risk',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'Sensitive data detected but not sourced from environment',
                    'score': 0.85,
                    'category': 'CONFIG_SECURITY',
                    'recommendation': 'Use os.environ or python-dotenv to load secrets'
                })
        
        return issues
    
    def _check_database_config(self, code: str) -> List[Dict]:
        """Check database configuration security"""
        issues = []
        
        # Check for database host settings
        if 'database' in code.lower() or 'db' in code.lower():
            if 'localhost' not in code and '127.0.0.1' not in code:
                if re.search(r'host\s*=\s*["\'][\w\.\-]+["\']', code):
                    if 'env' not in code.lower():
                        issues.append({
                            'type': 'Hardcoded Database Host',
                            'severity': 'MEDIUM',
                            'line': 0,
                            'msg': 'Database host might be hardcoded',
                            'score': 0.65,
                            'category': 'CONFIG_SECURITY',
                            'recommendation': 'Use environment variables for database configuration'
                        })
        
        # Check for default credentials
        if any(cred in code for cred in ['root', 'admin', 'password', '123456', '12345']):
            if 'database' in code.lower() or 'db' in code.lower() or 'sql' in code.lower():
                issues.append({
                    'type': 'Default Database Credentials',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': 'Default or weak database credentials detected',
                    'score': 0.92,
                    'category': 'CONFIG_SECURITY',
                    'recommendation': 'Use strong, unique credentials from secure storage'
                })
        
        return issues
    
    def _check_logging_config(self, code: str) -> List[Dict]:
        """Check logging configuration"""
        issues = []
        
        if 'logging' in code.lower() or 'logger' in code.lower():
            # Check if sensitive data might be logged
            if any(kw in code.lower() for kw in ['password', 'token', 'secret', 'key']):
                if 'password' not in code and 'token' not in code:
                    if not any(kw in code.lower() for kw in ['redact', 'mask', 'sanitize', 'hide']):
                        issues.append({
                            'type': 'Potential Sensitive Data in Logs',
                            'severity': 'HIGH',
                            'line': 0,
                            'msg': 'Sensitive data might be logged without redaction',
                            'score': 0.75,
                            'category': 'CONFIG_SECURITY',
                            'recommendation': 'Redact or mask sensitive data before logging'
                        })
        
        return issues
    
    def _check_ssl_tls(self, code: str) -> List[Dict]:
        """Check SSL/TLS configuration"""
        issues = []
        
        if 'ssl' in code.lower() or 'tls' in code.lower() or 'https' in code.lower():
            # Check for weak SSL protocols
            if any(proto in code.lower() for proto in ['sslv2', 'sslv3', 'tlsv1.0', 'tlsv1']):
                issues.append({
                    'type': 'Weak SSL/TLS Protocol',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'Using weak or deprecated SSL/TLS version',
                    'score': 0.82,
                    'category': 'CONFIG_SECURITY',
                    'recommendation': 'Use TLS 1.2 or higher'
                })
        
        # Check if HTTPS is enforced
        if 'http://' in code and 'api' in code.lower():
            issues.append({
                'type': 'Unencrypted HTTP',
                'severity': 'HIGH',
                'line': 0,
                'msg': 'HTTP protocol used instead of HTTPS',
                'score': 0.85,
                'category': 'CONFIG_SECURITY',
                'recommendation': 'Use HTTPS for all API communications'
            })
        
        return issues
    
    def _check_security_headers(self, code: str) -> List[Dict]:
        """Check security headers configuration"""
        issues = []
        
        if any(kw in code.lower() for kw in ['@app', '@route', 'response', 'header']):
            required_headers = ['x-frame-options', 'x-content-type-options', 'strict-transport-security']
            
            headers_found = sum(1 for h in required_headers if h in code.lower())
            
            if headers_found == 0:
                issues.append({
                    'type': 'Missing Security Headers',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'Security headers not configured',
                    'score': 0.68,
                    'category': 'CONFIG_SECURITY',
                    'recommendation': 'Add security headers (X-Frame-Options, X-Content-Type-Options, etc.)'
                })
        
        return issues
