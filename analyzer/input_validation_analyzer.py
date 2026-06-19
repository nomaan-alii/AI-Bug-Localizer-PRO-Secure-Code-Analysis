"""
Input Validation Analyzer - Checks for proper input validation and sanitization
Focus: SQL injection, XSS, command injection, path traversal, XXE
"""

import re
from typing import List, Dict, Any

class InputValidationAnalyzer:
    """Analyze input validation vulnerabilities"""
    
    def __init__(self):
        self.name = "Input Validation"
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for input validation issues"""
        issues = []
        
        issues.extend(self._check_sql_injection(code))
        issues.extend(self._check_xss_vulnerability(code))
        issues.extend(self._check_path_traversal(code))
        issues.extend(self._check_command_injection(code))
        issues.extend(self._check_xxe_vulnerability(code))
        issues.extend(self._check_input_sanitization(code))
        
        return issues
    
    def _check_sql_injection(self, code: str) -> List[Dict]:
        """Check for SQL injection vulnerabilities"""
        issues = []
        
        # String concatenation in SQL queries
        patterns = [
            (r'query\s*=\s*["\']SELECT.*["\']\s*\+', 'SQL query concatenation'),
            (r'execute\s*\(\s*["\']SELECT.*["\']\s*\.format', 'SQL format string'),
            (r'execute\s*\(\s*f["\']SELECT.*{', 'SQL f-string formatting'),
        ]
        
        for pattern, msg in patterns:
            if re.search(pattern, code, re.IGNORECASE | re.DOTALL):
                issues.append({
                    'type': 'SQL Injection Risk',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': msg + ' - vulnerable to SQL injection',
                    'score': 0.95,
                    'category': 'INPUT_VALIDATION',
                    'recommendation': 'Use parameterized queries or ORM'
                })
        
        # Direct query concatenation
        if re.search(r'query\s*=\s*["\']SELECT\s+\*\s+FROM.*WHERE.*=\s*["\']\s*\+\s*\w+', code):
            issues.append({
                'type': 'SQL Injection',
                'severity': 'CRITICAL',
                'line': 0,
                'msg': 'Direct variable concatenation in SQL query',
                'score': 0.98,
                'category': 'INPUT_VALIDATION',
                'recommendation': 'Use prepared statements with placeholders'
            })
        
        return issues
    
    def _check_xss_vulnerability(self, code: str) -> List[Dict]:
        """Check for Cross-Site Scripting (XSS) vulnerabilities"""
        issues = []
        
        # Unescaped output
        patterns = [
            (r'render_template_string\s*\(\s*[\w\.]+\s*\)', 'Template string with user input'),
            (r'html\.escape', None),  # If present, XSS might be handled
        ]
        
        # Check if user input is rendered without escaping
        if any(kw in code for kw in ['user_input', 'get_param', 'request.args', 'request.form']):
            if re.search(r'render_template\s*\(\s*["\'].*\.html["\'].*user_input', code):
                issues.append({
                    'type': 'Stored XSS Risk',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'User input rendered in template without escaping',
                    'score': 0.85,
                    'category': 'INPUT_VALIDATION',
                    'recommendation': 'Use template auto-escaping or html.escape()'
                })
        
        # Check for innerHTML or innerHTML-like patterns
        if 'innerhtml' in code.lower() or 'insertadjacenthtml' in code.lower():
            if not any(kw in code.lower() for kw in ['dompurify', 'sanitize', 'escape']):
                issues.append({
                    'type': 'DOM-based XSS Risk',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'innerHTML usage without sanitization',
                    'score': 0.88,
                    'category': 'INPUT_VALIDATION',
                    'recommendation': 'Use textContent or DOMPurify for HTML sanitization'
                })
        
        return issues
    
    def _check_path_traversal(self, code: str) -> List[Dict]:
        """Check for path traversal vulnerabilities"""
        issues = []
        
        # Path construction with user input
        patterns = [
            (r'open\s*\(\s*user\w+', 'File open with user input'),
            (r'Path\s*\(\s*\w*input', 'Path construction with input'),
            (r'os\.path\.join\s*\(\s*base.*user', 'Path join with user variable'),
        ]
        
        for pattern, msg in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                if '..' not in code or 'isabs' not in code:
                    issues.append({
                        'type': 'Path Traversal Risk',
                        'severity': 'HIGH',
                        'line': 0,
                        'msg': msg,
                        'score': 0.82,
                        'category': 'INPUT_VALIDATION',
                        'recommendation': 'Validate and sanitize file paths, use pathlib'
                    })
        
        return issues
    
    def _check_command_injection(self, code: str) -> List[Dict]:
        """Check for command injection vulnerabilities"""
        issues = []
        
        # Shell command execution with user input
        patterns = [
            (r'subprocess\.(call|run|Popen)\s*\(\s*f["\'].*{', 'subprocess f-string'),
            (r'os\.system\s*\(\s*[\w\.]+', 'os.system with variable'),
            (r'shell\s*=\s*True', 'subprocess with shell=True'),
        ]
        
        for pattern, msg in patterns:
            if re.search(pattern, code):
                issues.append({
                    'type': 'Command Injection Risk',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': msg,
                    'score': 0.93,
                    'category': 'INPUT_VALIDATION',
                    'recommendation': 'Use subprocess with list arguments, never shell=True'
                })
        
        return issues
    
    def _check_xxe_vulnerability(self, code: str) -> List[Dict]:
        """Check for XML External Entity (XXE) vulnerabilities"""
        issues = []
        
        if any(kw in code.lower() for kw in ['xml', 'etree', 'dom', 'lxml']):
            if 'defusedxml' not in code and 'defused' not in code:
                if re.search(r'ElementTree|parse\s*\(|minidom|pulldom', code):
                    issues.append({
                        'type': 'XXE Vulnerability Risk',
                        'severity': 'HIGH',
                        'line': 0,
                        'msg': 'XML parsing without XXE protection',
                        'score': 0.84,
                        'category': 'INPUT_VALIDATION',
                        'recommendation': 'Use defusedxml library for secure XML parsing'
                    })
        
        return issues
    
    def _check_input_sanitization(self, code: str) -> List[Dict]:
        """Check for proper input sanitization"""
        issues = []
        
        # Check if validation is missing
        if any(kw in code.lower() for kw in ['request.args', 'request.form', 'request.json']):
            if not any(kw in code.lower() for kw in ['validate', 'sanitize', 'strip', 'filter', 'schema']):
                issues.append({
                    'type': 'Missing Input Sanitization',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'User input used without sanitization',
                    'score': 0.70,
                    'category': 'INPUT_VALIDATION',
                    'recommendation': 'Implement input validation using Pydantic, Marshmallow, or similar'
                })
        
        return issues
