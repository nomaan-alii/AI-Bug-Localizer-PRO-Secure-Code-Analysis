# Compliance & Standards Checker (GDPR, HIPAA, PCI-DSS)
import re
from typing import List, Dict, Any

class ComplianceChecker:
    """Check code compliance with security standards"""
    
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for compliance issues"""
        issues = []
        
        issues.extend(self._check_gdpr(code))
        issues.extend(self._check_hipaa(code))
        issues.extend(self._check_pci_dss(code))
        issues.extend(self._check_data_protection(code))
        
        return issues
    
    def _check_gdpr(self, code: str) -> List[Dict]:
        """Check GDPR compliance (EU data protection)"""
        issues = []
        
        # Check for personal data handling
        patterns = [
            r'email',
            r'phone',
            r'ssn',
            r'personal_id',
            r'credit_card',
        ]
        
        has_pii = any(re.search(pattern, code, re.IGNORECASE) for pattern in patterns)
        
        if has_pii:
            # Check for encryption
            if 'encrypt' not in code.lower():
                issues.append({
                    'type': 'GDPR: Unencrypted PII',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'Personal data detected without encryption',
                    'score': 0.88,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Encrypt all personal data at rest and in transit'
                })
            
            # Check for consent management
            if 'consent' not in code.lower():
                issues.append({
                    'type': 'GDPR: Missing Consent',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'No consent management for PII collection',
                    'score': 0.85,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Implement explicit user consent mechanism'
                })
            
            # Check for data retention policy
            if 'delete' not in code.lower() and 'purge' not in code.lower():
                issues.append({
                    'type': 'GDPR: No Data Retention',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'No data deletion/retention policy detected',
                    'score': 0.70,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Implement automated data deletion after retention period'
                })
        
        return issues
    
    def _check_hipaa(self, code: str) -> List[Dict]:
        """Check HIPAA compliance (Healthcare data)"""
        issues = []
        
        # Check for health-related data
        health_keywords = [
            r'medical',
            r'patient',
            r'diagnosis',
            r'treatment',
            r'healthcare',
            r'health_record',
        ]
        
        has_health_data = any(re.search(kw, code, re.IGNORECASE) for kw in health_keywords)
        
        if has_health_data:
            # Check for encryption
            if 'encrypt' not in code.lower():
                issues.append({
                    'type': 'HIPAA: Unencrypted PHI',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': 'Protected Health Information without encryption',
                    'score': 0.94,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Encrypt PHI using NIST-approved algorithms'
                })
            
            # Check for audit logging
            if 'audit' not in code.lower() and 'log' not in code.lower():
                issues.append({
                    'type': 'HIPAA: No Audit Trail',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'No audit logging for PHI access',
                    'score': 0.87,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Implement comprehensive audit logging'
                })
            
            # Check for access controls
            if 'permission' not in code.lower() and 'role' not in code.lower():
                issues.append({
                    'type': 'HIPAA: No Access Control',
                    'severity': 'HIGH',
                    'line': 0,
                    'msg': 'No role-based access control for PHI',
                    'score': 0.85,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Implement RBAC for PHI access'
                })
        
        return issues
    
    def _check_pci_dss(self, code: str) -> List[Dict]:
        """Check PCI-DSS compliance (Payment card data)"""
        issues = []
        
        # Check for credit card data
        cc_patterns = [
            r'card_number',
            r'cvv',
            r'expiry',
            r'credit_card',
            r'cc_data',
        ]
        
        has_cc_data = any(re.search(pattern, code, re.IGNORECASE) for pattern in cc_patterns)
        
        if has_cc_data:
            # Check for encryption
            if 'encrypt' not in code.lower():
                issues.append({
                    'type': 'PCI-DSS: Unencrypted CC Data',
                    'severity': 'CRITICAL',
                    'line': 0,
                    'msg': 'Credit card data without encryption',
                    'score': 0.96,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Use tokenization and PCI-compliant encryption'
                })
            
            # Check for hardcoded values
            for i, line in enumerate(code.split('\n'), 1):
                if re.search(r'\d{13,19}', line):  # Potential CC number
                    issues.append({
                        'type': 'PCI-DSS: Hardcoded Card Data',
                        'severity': 'CRITICAL',
                        'line': i,
                        'msg': 'Credit card number in source code',
                        'score': 0.98,
                        'category': 'COMPLIANCE',
                        'recommendation': 'Use tokenization services (Stripe, etc.)'
                    })
        
        return issues
    
    def _check_data_protection(self, code: str) -> List[Dict]:
        """General data protection checks"""
        issues = []
        
        # Check for proper error handling of sensitive data
        for i, line in enumerate(code.split('\n'), 1):
            if 'except' in line and 'password' in line.lower():
                issues.append({
                    'type': 'Data Protection: Exposed in Error',
                    'severity': 'HIGH',
                    'line': i,
                    'msg': 'Sensitive data may be exposed in error messages',
                    'score': 0.82,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Sanitize error messages before display'
                })
        
        # Check for database security
        if 'database' in code.lower() or 'db' in code.lower():
            if 'password' not in code.lower():
                issues.append({
                    'type': 'Data Protection: DB Security',
                    'severity': 'MEDIUM',
                    'line': 0,
                    'msg': 'Database connection without visible authentication',
                    'score': 0.70,
                    'category': 'COMPLIANCE',
                    'recommendation': 'Use connection pooling and secure credentials'
                })
        
        return issues
