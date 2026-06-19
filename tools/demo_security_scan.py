import json
from analyzer.owasp_analyzer import OWASPAnalyzer
from analyzer.encryption_analyzer import EncryptionAnalyzer
from analyzer.compliance_checker import ComplianceChecker
from analyzer.authentication_analyzer import AuthenticationAnalyzer

sample_code = '''
# Vulnerable sample for demonstration
import sqlite3
import hashlib
import yaml

# SQL injection (string formatting)
def get_user(conn, user_input):
    q = "SELECT * FROM users WHERE username = '%s'" % user_input
    cur = conn.execute(q)
    return cur.fetchall()

# Hardcoded secret
API_KEY = "12345-SECRET-KEY"
PASSWORD = "password123"

# Weak hashing
def wrong_hash(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

# Unsafe deserialization
def load_config(raw):
    return yaml.load(raw)

# Eval usage (dangerous)
def run(cmd):
    return eval(cmd)

# Insecure JWT secret example
JWT_SECRET = "secret"

# Debug mode left on
DEBUG = True
'''

# Instantiate analyzers
owasp = OWASPAnalyzer()
enc = EncryptionAnalyzer()
comp = ComplianceChecker()
auth = AuthenticationAnalyzer()

# Run analyses
owasp_issues = owasp.analyze(sample_code)
crypto_issues = enc.analyze(sample_code)
compliance_issues = comp.analyze(sample_code)
auth_issues = auth.analyze(sample_code)

results = {
    'owasp_issues': owasp_issues if isinstance(owasp_issues, list) else [owasp_issues],
    'crypto_issues': crypto_issues if isinstance(crypto_issues, list) else [crypto_issues],
    'compliance_issues': compliance_issues if isinstance(compliance_issues, list) else [compliance_issues],
    'auth_issues': auth_issues if isinstance(auth_issues, list) else [auth_issues],
}

print(json.dumps(results, indent=2))
