# Cryptography & Encryption Analysis
import re
from typing import List, Dict, Any

class EncryptionAnalyzer:
    """Analyze encryption and cryptography practices in code"""
    
    WEAK_ALGORITHMS = ['DES', 'MD5', 'SHA1', 'RC4']
    STRONG_ALGORITHMS = ['AES', 'RSA-2048', 'SHA-256', 'SHA-512', 'bcrypt', 'PBKDF2']
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for cryptography issues"""
        issues = []
        
        issues.extend(self._check_weak_encryption(code))
        issues.extend(self._check_weak_hashing(code))
        issues.extend(self._check_ssl_tls(code))
        issues.extend(self._check_random_generation(code))
        issues.extend(self._check_key_management(code))
        
        return issues
    
    def _check_weak_encryption(self, code: str) -> List[Dict]:
        issues = []
        
        # Check for weak cipher modes
        weak_patterns = [
            (r'DES\(', 'DES is deprecated'),
            (r'Cipher\.new.*DES', 'DES is deprecated'),
            (r'RC4', 'RC4 is broken'),
            (r'ECB\(', 'ECB mode is insecure'),
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern, msg in weak_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'Weak Encryption Algorithm',
                        'severity': 'CRITICAL',
                        'line': i,
                        'msg': msg,
                        'score': 0.93,
                        'category': 'CRYPTO',
                        'recommendation': 'Use AES with CBC or GCM mode'
                    })
        
        return issues
    
    def _check_weak_hashing(self, code: str) -> List[Dict]:
        issues = []
        weak_hashes = [
            (r'md5\(', 'MD5 is cryptographically broken'),
            (r'hashlib\.md5', 'MD5 is cryptographically broken'),
            (r'sha1\(', 'SHA1 is weak'),
            (r'hashlib\.sha1', 'SHA1 is weak'),
            (r'hash\(.*plain', 'Plain hashing without salt'),
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern, msg in weak_hashes:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'Weak Hashing Algorithm',
                        'severity': 'HIGH',
                        'line': i,
                        'msg': msg,
                        'score': 0.87,
                        'category': 'CRYPTO',
                        'recommendation': 'Use SHA-256 or bcrypt for passwords'
                    })
        
        # Check for unsalted hashing
        if 'hash(' in code and 'salt' not in code.lower():
            issues.append({
                'type': 'Unsalted Hash',
                'severity': 'HIGH',
                'line': 0,
                'msg': 'Password hashing without salt detected',
                'score': 0.85,
                'category': 'CRYPTO',
                'recommendation': 'Always use salt for password hashing'
            })
        
        return issues
    
    def _check_ssl_tls(self, code: str) -> List[Dict]:
        issues = []
        
        patterns = [
            (r'verify\s*=\s*False', 'SSL verification disabled'),
            (r'ssl\.CERT_NONE', 'SSL certificate validation disabled'),
            (r'http://', 'Unencrypted HTTP connection'),
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern, msg in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'SSL/TLS Issue',
                        'severity': 'HIGH' if 'http://' in pattern else 'CRITICAL',
                        'line': i,
                        'msg': msg,
                        'score': 0.89,
                        'category': 'CRYPTO',
                        'recommendation': 'Use HTTPS and verify certificates'
                    })
        
        return issues
    
    def _check_random_generation(self, code: str) -> List[Dict]:
        issues = []
        
        patterns = [
            (r'random\.randint', 'Using random instead of secrets'),
            (r'random\.choice', 'Using random instead of secrets'),
            (r'random\.shuffle', 'Using random instead of secrets'),
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern, msg in patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'Weak Random Generation',
                        'severity': 'MEDIUM',
                        'line': i,
                        'msg': msg,
                        'score': 0.75,
                        'category': 'CRYPTO',
                        'recommendation': 'Use secrets module for cryptographic operations'
                    })
        
        return issues
    
    def _check_key_management(self, code: str) -> List[Dict]:
        issues = []
        
        if 'key' in code.lower():
            if re.search(r'key\s*=\s*["\'][^"\']*["\']', code):
                issues.append({
                    'type': 'Hardcoded Cryptographic Key',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': 'Cryptographic keys hardcoded in source',
                    'score': 0.96,
                    'category': 'CRYPTO',
                    'recommendation': 'Store keys in secure key management system'
                })
        
        return issues
