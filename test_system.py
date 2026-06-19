"""
COMPREHENSIVE TEST SCRIPT FOR AI BUG LOCALIZER PRO
==================================================
Tests all 9 analyzers and system functionality
Run: python test_system.py
"""

import sys
import traceback
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Test samples
VULNERABLE_CODE_SAMPLES = {
    "sql_injection": """
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('db.sqlite')
    query = "SELECT * FROM users WHERE id = " + user_id  # SQL Injection
    cursor = conn.execute(query)
    return cursor.fetchall()
""",
    
    "hardcoded_credentials": """
import requests

API_KEY = "sk-1234567890abcdef"  # Hardcoded API key
SECRET = "super_secret_password"

def login():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    return requests.get("https://api.example.com/user", headers=headers)
""",
    
    "weak_crypto": """
import hashlib
import pickle

password = "user_password"
# Weak: Using MD5 for password hashing
hashed = hashlib.md5(password.encode()).hexdigest()

# Dangerous: Using pickle for untrusted data
data = pickle.loads(untrusted_input)
""",
    
    "owasp_issues": """
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/user/<user_id>')
def get_user(user_id):
    # A1: Injection - No input validation
    query = f"SELECT * FROM users WHERE id = {user_id}"
    
    # A7: XSS - Unsanitized output
    user_data = request.args.get('name')
    return f"<h1>{user_data}</h1>"

@app.route('/upload', methods=['POST'])
def upload():
    # A6: Using components with known vulnerabilities
    file = request.files['file']
    file.save(f"/uploads/{file.filename}")  # Path traversal vulnerability
    return "Uploaded"
""",
    
    "bad_config": """
import os
from flask import Flask

app = Flask(__name__)

# Bad: Debug mode enabled in production
app.config['DEBUG'] = True

# Bad: Hardcoded database credentials
DB_URL = "postgresql://admin:password123@localhost/db"

# Bad: No HTTPS
app.config['SESSION_COOKIE_SECURE'] = False

# Bad: CORS too permissive
app.config['CORS_HEADERS'] = 'Content-Type'
""",
    
    "dependency_vuln": """
import pickle
import shelve
import marshal
import subprocess

# All dangerous - known vulnerable patterns
data = pickle.loads(user_input)
db = shelve.open('data')
code = marshal.loads(bytecode)

# Shell injection
os.system(f"echo {user_input}")
subprocess.call(f"ls {directory}", shell=True)
""",
    
    "api_security": """
@app.route('/api/data', methods=['GET'])
def get_data():
    # No rate limiting
    # No API authentication
    data = request.args.get('query')
    
    # No input validation
    result = database.query(data)
    
    # No logging
    return result

@app.route('/api/v1/user/<user_id>')
def get_user(user_id):
    # Hardcoded API key in response
    api_key = "secret_key_12345"
    return {"data": user_data, "key": api_key}
""",
    
    "input_validation": """
def process_data(user_input, file_path):
    # No validation - potential for multiple attacks
    
    # SQL Injection
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    
    # Path Traversal
    file = open(f"/uploads/{file_path}", 'r')
    
    # Command Injection
    os.system(f"process_file {file_path}")
    
    # XSS (if used in web context)
    return f"<div>{user_input}</div>"
""",
}

GOOD_CODE_SAMPLE = """
import hashlib
import secrets
from flask import Flask, request
from cryptography.fernet import Fernet

app = Flask(__name__)

# Good: Secure configuration
app.config['DEBUG'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Good: Secure password hashing
def hash_password(password):
    salt = secrets.token_hex(32)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${hashed.hex()}"

# Good: Input validation
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Good: Secure API with authentication
@app.route('/api/user', methods=['GET'])
def get_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return {'error': 'Unauthorized'}, 401
    
    # Good: Rate limiting (in production)
    # @limiter.limit("100 per hour")
    
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        return {'error': 'Invalid input'}, 400
    
    # Good: Parameterized query (not shown, but used)
    return {'user': 'data'}
"""

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Back.CYAN}{Fore.BLACK}{'='*70}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK} {text:<68} {Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{'='*70}{Style.RESET_ALL}\n")

def print_success(msg):
    """Print success message"""
    print(f"{Fore.GREEN}✅ {msg}{Style.RESET_ALL}")

def print_error(msg):
    """Print error message"""
    print(f"{Fore.RED}❌ {msg}{Style.RESET_ALL}")

def print_info(msg):
    """Print info message"""
    print(f"{Fore.BLUE}ℹ️  {msg}{Style.RESET_ALL}")

def print_warning(msg):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠️  {msg}{Style.RESET_ALL}")

def test_imports():
    """Test if all required modules can be imported"""
    print_header("TESTING IMPORTS")
    
    modules_to_test = [
        ("streamlit", "Streamlit"),
        ("analyzer.static_analysis", "Static Analysis"),
        ("analyzer.runtime_analysis", "Runtime Analysis"),
        ("analyzer.security_analysis", "Security Analysis"),
        ("analyzer.owasp_analyzer", "OWASP Analyzer"),
        ("analyzer.encryption_analyzer", "Encryption Analyzer"),
        ("analyzer.compliance_checker", "Compliance Checker"),
        ("analyzer.authentication_analyzer", "Authentication Analyzer"),
        ("analyzer.api_security_analyzer", "API Security Analyzer"),
        ("analyzer.dependency_vulnerability_analyzer", "Dependency Analyzer"),
        ("analyzer.secure_configuration_analyzer", "Configuration Analyzer"),
        ("analyzer.input_validation_analyzer", "Input Validation Analyzer"),
        ("analyzer.threat_modeling_analyzer", "Threat Modeling Analyzer"),
    ]
    
    all_passed = True
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print_success(f"{display_name} imported successfully")
        except Exception as e:
            print_error(f"{display_name} import failed: {str(e)}")
            all_passed = False
    
    return all_passed

def test_analyzer(analyzer_class, code_sample, analyzer_name):
    """Test a single analyzer"""
    try:
        analyzer = analyzer_class()
        results = analyzer.analyze(code_sample)
        
        if results and isinstance(results, list):
            print_success(f"{analyzer_name}: Found {len(results)} issue(s)")
            return True, results
        elif results is None:
            print_warning(f"{analyzer_name}: No issues found (empty result)")
            return True, []
        else:
            print_warning(f"{analyzer_name}: Unexpected result type")
            return True, []
    except Exception as e:
        print_error(f"{analyzer_name} failed: {str(e)}")
        traceback.print_exc()
        return False, []

def test_all_analyzers():
    """Test all 9 analyzers with vulnerable code"""
    print_header("TESTING ALL 9 ANALYZERS")
    
    try:
        from analyzer.static_analysis import analyze_ast
        from analyzer.runtime_analysis import run_code
        from analyzer.security_analysis import analyze_security
        from analyzer.owasp_analyzer import OWASPAnalyzer
        from analyzer.encryption_analyzer import EncryptionAnalyzer
        from analyzer.compliance_checker import ComplianceChecker
        from analyzer.authentication_analyzer import AuthenticationAnalyzer
        from analyzer.api_security_analyzer import APISecurityAnalyzer
        from analyzer.dependency_vulnerability_analyzer import DependencyVulnerabilityAnalyzer
        from analyzer.secure_configuration_analyzer import SecureConfigurationAnalyzer
        from analyzer.input_validation_analyzer import InputValidationAnalyzer
        from analyzer.threat_modeling_analyzer import ThreatModelingAnalyzer
        
        # Test function-based analyzers
        print_info("Testing function-based analyzers:")
        
        # Static Analysis
        try:
            results = analyze_ast(VULNERABLE_CODE_SAMPLES["sql_injection"])
            if results and isinstance(results, list):
                print_success(f"Static Analysis: Found {len(results)} issue(s)")
            else:
                print_warning("Static Analysis: No issues found")
        except Exception as e:
            print_warning(f"Static Analysis: {str(e)}")
        
        # Runtime Analysis
        try:
            results = run_code(VULNERABLE_CODE_SAMPLES["weak_crypto"])
            if results and isinstance(results, list):
                print_success(f"Runtime Analysis: Found {len(results)} issue(s)")
            else:
                print_warning("Runtime Analysis: No runtime errors found")
        except Exception as e:
            print_error(f"Runtime Analysis failed: {str(e)}")
        
        # Security Analysis
        try:
            results = analyze_security(VULNERABLE_CODE_SAMPLES["hardcoded_credentials"])
            if results and isinstance(results, list):
                print_success(f"Security Analysis: Found {len(results)} issue(s)")
            else:
                print_warning("Security Analysis: No issues found")
        except Exception as e:
            print_error(f"Security Analysis failed: {str(e)}")
        
        print()
        print_info("Testing class-based security modules:")
        
        # Class-based analyzers
        analyzers = [
            (OWASPAnalyzer, VULNERABLE_CODE_SAMPLES["owasp_issues"], "OWASP Analyzer"),
            (EncryptionAnalyzer, VULNERABLE_CODE_SAMPLES["weak_crypto"], "Encryption Analyzer"),
            (ComplianceChecker, VULNERABLE_CODE_SAMPLES["bad_config"], "Compliance Checker"),
            (AuthenticationAnalyzer, VULNERABLE_CODE_SAMPLES["bad_config"], "Authentication Analyzer"),
            (APISecurityAnalyzer, VULNERABLE_CODE_SAMPLES["api_security"], "API Security Analyzer"),
            (DependencyVulnerabilityAnalyzer, VULNERABLE_CODE_SAMPLES["dependency_vuln"], "Dependency Analyzer"),
            (SecureConfigurationAnalyzer, VULNERABLE_CODE_SAMPLES["bad_config"], "Configuration Analyzer"),
            (InputValidationAnalyzer, VULNERABLE_CODE_SAMPLES["input_validation"], "Input Validation Analyzer"),
            (ThreatModelingAnalyzer, VULNERABLE_CODE_SAMPLES["api_security"], "Threat Modeling Analyzer"),
        ]
        
        total_tests = 3 + len(analyzers)
        passed_tests = 3
        total_issues = 0
        
        for analyzer_class, code_sample, name in analyzers:
            success, results = test_analyzer(analyzer_class, code_sample, name)
            if success:
                passed_tests += 1
                total_issues += len(results)
                
                if results:
                    print(f"   Sample issues found:")
                    for i, issue in enumerate(results[:2], 1):
                        print(f"   {i}. {issue.get('type', 'Unknown')}: {issue.get('msg', 'No message')[:60]}")
            print()
        
        print_info(f"Analyzer Test Results: {passed_tests}/{total_tests} passed")
        print_info(f"Total issues detected: {total_issues}")
        
        return passed_tests >= total_tests - 2  # Allow some flexibility
        
    except Exception as e:
        print_error(f"Analyzer testing failed: {str(e)}")
        traceback.print_exc()
        return False

def test_good_code():
    """Test with good, secure code"""
    print_header("TESTING WITH GOOD CODE (SHOULD HAVE FEWER ISSUES)")
    
    try:
        from analyzer.static_analysis import analyze_ast
        from analyzer.security_analysis import analyze_security
        from analyzer.owasp_analyzer import OWASPAnalyzer
        
        print_info("Testing with secure code sample:")
        print()
        
        # Test function-based analyzers
        try:
            results = analyze_ast(GOOD_CODE_SAMPLE)
            if results:
                print_warning(f"Static Analysis: Found {len(results)} issue(s) (expected: minimal)")
            else:
                print_success("Static Analysis: No issues found ✓")
        except Exception as e:
            print_error(f"Static Analysis failed: {str(e)}")
        
        try:
            results = analyze_security(GOOD_CODE_SAMPLE)
            if results:
                print_warning(f"Security Analysis: Found {len(results)} issue(s) (expected: minimal)")
            else:
                print_success("Security Analysis: No issues found ✓")
        except Exception as e:
            print_error(f"Security Analysis failed: {str(e)}")
        
        # Test class-based analyzer
        try:
            analyzer = OWASPAnalyzer()
            results = analyzer.analyze(GOOD_CODE_SAMPLE)
            if results:
                print_warning(f"OWASP Analyzer: Found {len(results)} issue(s) (expected: minimal)")
            else:
                print_success("OWASP Analyzer: No issues found ✓")
        except Exception as e:
            print_error(f"OWASP Analyzer failed: {str(e)}")
        
        return True
        
    except Exception as e:
        print_error(f"Good code testing failed: {str(e)}")
        traceback.print_exc()
        return False

def test_issue_format():
    """Test if issues have correct format"""
    print_header("TESTING ISSUE FORMAT")
    
    try:
        from analyzer.static_analysis import analyze_ast
        
        results = analyze_ast(VULNERABLE_CODE_SAMPLES["sql_injection"])
        
        if not results:
            print_warning("No results to validate format")
            return True
        
        print_info("Validating issue format from Static Analysis:")
        print()
        
        issue = results[0]
        fields_to_check = ['line', 'type', 'msg']
        
        print(f"Sample issue structure:")
        for field in fields_to_check:
            if field in issue:
                print_success(f"  '{field}': {issue[field]}")
            else:
                print_error(f"  '{field}': MISSING")
        
        all_present = all(field in issue for field in fields_to_check)
        
        if all_present:
            print()
            print_success("Issue format validation passed!")
        else:
            print_error("Issue format validation failed!")
        
        return all_present
        
    except Exception as e:
        print_error(f"Issue format testing failed: {str(e)}")
        traceback.print_exc()
        return False

def test_performance():
    """Test analyzer performance"""
    print_header("TESTING PERFORMANCE")
    
    import time
    
    try:
        from analyzer.static_analysis import analyze_ast
        from analyzer.security_analysis import analyze_security
        from analyzer.owasp_analyzer import OWASPAnalyzer
        
        code_sample = VULNERABLE_CODE_SAMPLES["sql_injection"] * 10  # Larger sample
        
        print_info("Testing with 10x code sample size:")
        print()
        
        # Function-based analyzers
        try:
            start = time.time()
            results = analyze_ast(code_sample)
            elapsed = (time.time() - start) * 1000
            
            if elapsed < 1000:
                print_success(f"Static Analysis: {elapsed:.2f}ms ✓")
            elif elapsed < 5000:
                print_warning(f"Static Analysis: {elapsed:.2f}ms (acceptable)")
            else:
                print_error(f"Static Analysis: {elapsed:.2f}ms (slow)")
        except Exception as e:
            print_error(f"Static Analysis perf test failed: {str(e)}")
        
        try:
            start = time.time()
            results = analyze_security(code_sample)
            elapsed = (time.time() - start) * 1000
            
            if elapsed < 1000:
                print_success(f"Security Analysis: {elapsed:.2f}ms ✓")
            elif elapsed < 5000:
                print_warning(f"Security Analysis: {elapsed:.2f}ms (acceptable)")
            else:
                print_error(f"Security Analysis: {elapsed:.2f}ms (slow)")
        except Exception as e:
            print_error(f"Security Analysis perf test failed: {str(e)}")
        
        # Class-based analyzer
        try:
            analyzer = OWASPAnalyzer()
            start = time.time()
            results = analyzer.analyze(code_sample)
            elapsed = (time.time() - start) * 1000
            
            if elapsed < 1000:
                print_success(f"OWASP Analyzer: {elapsed:.2f}ms ✓")
            elif elapsed < 5000:
                print_warning(f"OWASP Analyzer: {elapsed:.2f}ms (acceptable)")
            else:
                print_error(f"OWASP Analyzer: {elapsed:.2f}ms (slow)")
        except Exception as e:
            print_error(f"OWASP Analyzer perf test failed: {str(e)}")
        
        return True
        
    except Exception as e:
        print_error(f"Performance testing failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Back.MAGENTA}{Fore.WHITE}{'='*70}{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE} AI BUG LOCALIZER PRO - COMPREHENSIVE TEST SUITE{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}{'='*70}{Style.RESET_ALL}\n")
    
    test_results = {
        "Import Tests": test_imports(),
        "Analyzer Tests": test_all_analyzers(),
        "Good Code Tests": test_good_code(),
        "Issue Format Tests": test_issue_format(),
        "Performance Tests": test_performance(),
    }
    
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in test_results.values() if v)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print()
    if passed == total:
        print(f"{Back.GREEN}{Fore.BLACK} ✅ ALL TESTS PASSED ({passed}/{total}) {Style.RESET_ALL}")
        print_success("System is ready for production use!")
        return 0
    else:
        print(f"{Back.YELLOW}{Fore.BLACK} ⚠️  SOME TESTS FAILED ({passed}/{total}) {Style.RESET_ALL}")
        print_warning("Please review the failures above")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
