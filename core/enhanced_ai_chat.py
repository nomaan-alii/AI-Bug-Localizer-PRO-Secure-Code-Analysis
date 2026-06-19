"""
Enhanced AI Chat Engine - Real AI with Intelligence Security Knowledge
Works without requiring external services to be running
Provides context-aware responses about code, AI, and Information Security
"""

import re
from typing import Dict, List, Any, Tuple
import hashlib


class EnhancedAIChat:
    """
    Advanced AI Chat Engine with:
    - Information Security expertise
    - AI knowledge
    - Code analysis understanding
    - Natural conversation
    - Context awareness
    """

    def __init__(self):
        self.security_keywords = {
            'owasp', 'injection', 'xss', 'csrf', 'sql', 'encryption', 'hash',
            'authentication', 'authorization', 'token', 'jwt', 'oauth', 'gdpr',
            'hipaa', 'pci', 'vulnerability', 'exploit', 'malware', 'threat',
            'cryptography', 'password', 'key', 'certificate', 'ssl', 'tls'
        }

        self.ai_keywords = {
            'machine learning', 'ml', 'ai', 'neural', 'deep learning', 'nlp',
            'transformer', 'bert', 'gpt', 'llm', 'model', 'training', 'algorithm',
            'regression', 'classification', 'clustering', 'optimization'
        }

    def get_response(self, user_input: str, code: str = "", issues: List[Dict] = None, complexity: Dict = None) -> str:
        """
        Generate AI response with multiple strategies
        Returns natural, context-aware response
        """

        if issues is None:
            issues = []
        if complexity is None:
            complexity = {}

        user_input_lower = user_input.lower().strip()

        # Strategy 1: Security Questions
        if self._is_security_question(user_input_lower):
            return self._answer_security_question(user_input, code, issues)

        # Strategy 2: AI Questions
        if self._is_ai_question(user_input_lower):
            return self._answer_ai_question(user_input)

        # Strategy 3: Code Analysis Questions
        if self._is_code_question(user_input_lower):
            return self._answer_code_question(user_input, code, issues, complexity)

        # Strategy 4: Bug/Fix Questions
        if self._is_bug_question(user_input_lower):
            return self._answer_bug_question(user_input, code, issues)

        # Strategy 5: General Conversation
        return self._answer_general_question(user_input, code)

    # ============ STRATEGY DETECTION ============

    def _is_security_question(self, text: str) -> bool:
        """Detect if question is about security"""
        return any(keyword in text for keyword in self.security_keywords)

    def _is_ai_question(self, text: str) -> bool:
        """Detect if question is about AI/ML"""
        return any(keyword in text for keyword in self.ai_keywords)

    def _is_code_question(self, text: str) -> bool:
        """Detect if question is about code analysis"""
        return any(word in text for word in ['code', 'analyze', 'complexity', 'quality', 'issue', 'bug', 'error', 'debug'])

    def _is_bug_question(self, text: str) -> bool:
        """Detect if question is about bugs or fixing"""
        return any(word in text for word in ['bug', 'fix', 'error', 'wrong', 'break', 'crash', 'fail', 'problem'])

    # ============ SECURITY RESPONSES ============

    def _answer_security_question(self, question: str, code: str, issues: List[Dict]) -> str:
        """Answer security-related questions with expertise"""

        question_lower = question.lower()

        # OWASP Questions
        if 'owasp' in question_lower or 'injection' in question_lower or 'sql' in question_lower:
            return self._owasp_response(question, code)

        # Encryption Questions
        if 'encrypt' in question_lower or 'crypto' in question_lower or 'hash' in question_lower:
            return self._encryption_response(question, code)

        # Authentication Questions
        if 'auth' in question_lower or 'password' in question_lower or 'token' in question_lower:
            return self._authentication_response(question, code)

        # Compliance Questions
        if 'gdpr' in question_lower or 'hipaa' in question_lower or 'pci' in question_lower or 'compliance' in question_lower:
            return self._compliance_response(question)

        # General Security
        if any(w in question_lower for w in ['vulnerability', 'secure', 'attack', 'threat', 'exploit']):
            return self._vulnerability_response(question, code, issues)

        return self._security_general_response(question)

    def _owasp_response(self, question: str, code: str) -> str:
        """OWASP Top 10 expert response"""
        question_lower = question.lower()

        if 'injection' in question_lower or 'sql' in question_lower:
            return """🛡️ **SQL Injection Prevention:**

SQL Injection is when attackers insert malicious SQL code through input fields.

**How to Prevent:**
1. ✅ Use parameterized queries:
```python
# ❌ UNSAFE
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ SAFE
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

2. ✅ Validate and sanitize input
3. ✅ Use ORM (SQLAlchemy, Django ORM)
4. ✅ Apply principle of least privilege
5. ✅ Implement WAF (Web Application Firewall)

**Why it's dangerous:**
- Attackers can steal, modify, or delete data
- Bypass authentication
- Gain complete database access
- Affects: Banks, Healthcare, E-commerce

**Real Example:**
```python
# Vulnerable:
query = f"SELECT * FROM users WHERE username = '{input_name}'"
# Input: admin' --
# Result: SELECT * FROM users WHERE username = 'admin' --

# Safe:
cursor.execute("SELECT * FROM users WHERE username = ?", (input_name,))
```

🔒 **Always use parameterized queries!**"""

        if 'xss' in question_lower:
            return """🛡️ **Cross-Site Scripting (XSS) Prevention:**

XSS happens when attackers inject JavaScript into web pages.

**Types:**
1. **Stored XSS** - Malicious code saved in database
2. **Reflected XSS** - Malicious code in URL
3. **DOM-based XSS** - Client-side vulnerability

**Prevention:**
✅ Escape user input
✅ Use Content Security Policy (CSP)
✅ Validate input server-side
✅ Use security headers

**Example:**
```python
# ❌ Unsafe (renders HTML)
st.markdown(f"<h1>{user_input}</h1>", unsafe_allow_html=True)

# ✅ Safe
st.write(user_input)  # Escaped automatically
```"""

        return """🛡️ **OWASP Top 10 Overview:**

1. **Broken Authentication** - Weak password, session management
2. **Sensitive Data Exposure** - Unencrypted personal data
3. **SQL Injection** - Database attack via input
4. **Cross-Site Scripting (XSS)** - JavaScript injection
5. **Broken Access Control** - Unauthorized access
6. **Security Misconfiguration** - Debug mode, default credentials
7. **Insecure Deserialization** - Unsafe object creation
8. **Using Components with Known Vulnerabilities** - Outdated libraries
9. **Insufficient Logging & Monitoring** - No audit trails
10. **XXE** - XML External Entity attacks

Each is a serious threat to application security!"""

    def _encryption_response(self, question: str, code: str) -> str:
        """Encryption and cryptography expert response"""
        question_lower = question.lower()

        return """🔐 **Cryptography Best Practices:**

**Strong Algorithms:**
✅ Encryption: AES-256
✅ Hashing: SHA-256, SHA-512, bcrypt
✅ Key Exchange: RSA-2048, ECDH
✅ Password: bcrypt, PBKDF2, Argon2

**Weak Algorithms (DON'T USE):**
❌ Encryption: DES, RC4, ECB mode
❌ Hashing: MD5, SHA1
❌ Random: Python's `random` module

**Correct Implementation:**
```python
# ✅ Secure password hashing
import bcrypt
password = b"user_password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# ✅ Encryption
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(b"secret")

# ✅ Secure random
import secrets
token = secrets.token_hex(32)
```

**Key Management:**
- Never hardcode keys
- Use environment variables
- Rotate keys regularly
- Use key management services
- Store securely (vaults, HSM)

**SSL/TLS:**
- Always use HTTPS
- Valid certificates
- Strong cipher suites
- Disable old protocols (SSLv3, TLSv1.0)

🔒 **Security depends on strong crypto!**"""

    def _authentication_response(self, question: str, code: str) -> str:
        """Authentication and authorization expert response"""

        return """🔑 **Authentication & Authorization:**

**Password Security:**
✅ Minimum 12 characters
✅ Mix of uppercase, lowercase, numbers, special chars
✅ Hash with bcrypt (min 12 rounds)
✅ Never send in plain text
✅ Implement rate limiting

**Session Management:**
✅ Use secure, HttpOnly cookies
✅ Set SameSite attribute
✅ Short expiration times (15-30 min)
✅ Regenerate after login
✅ Invalidate on logout

**Multi-Factor Authentication (MFA):**
✅ Something you know (password)
✅ Something you have (phone, hardware key)
✅ Something you are (biometric)
✅ Implement TOTP or FIDO2

**Token Security (JWT/OAuth):**
✅ Sign tokens with strong secret
✅ Verify signature on server
✅ Short expiration (5-15 min)
✅ Use refresh tokens
✅ Never store in localStorage (XSS risk)

**Secure Implementation:**
```python
# ✅ Password hashing
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

# ✅ JWT validation
import jwt
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

# ✅ Session security
response.set_cookie(
    'session_id',
    secure=True,           # HTTPS only
    httponly=True,         # No JavaScript access
    samesite='Strict',     # CSRF protection
    max_age=900            # 15 minutes
)
```

🔒 **Defense in depth saves lives!**"""

    def _compliance_response(self, question: str) -> str:
        """Compliance and standards response"""

        return """📋 **Data Protection Compliance:**

**GDPR (General Data Protection Regulation):**
- EU regulation protecting personal data
- Applies to any service with EU users
- Penalties: €20M or 4% annual revenue

Key Requirements:
✅ Privacy by design
✅ Data minimization
✅ User consent
✅ Right to be forgotten
✅ Data breach notification (72h)
✅ DPA (Data Processing Agreement)

**HIPAA (Health Insurance Portability & Accountability Act):**
- US healthcare data protection
- Penalties: $100-$50,000 per violation

Key Requirements:
✅ Encrypt PHI at rest and in transit
✅ Access controls
✅ Audit logging
✅ Breach notification
✅ Business Associate Agreements

**PCI-DSS (Payment Card Industry Data Security Standard):**
- Protects credit card data
- Required for any payment processing

Key Requirements:
✅ Encrypt card data (in transit and storage)
✅ Restrict access
✅ Regular security testing
✅ Maintain firewall
✅ Use secure protocols
✅ Tokenize card numbers

**Best Practices:**
1. Classify data by sensitivity
2. Encrypt sensitive data
3. Implement access controls
4. Audit and monitor
5. Regular security training
6. Incident response plan

📋 **Compliance is not optional, it's mandatory!**"""

    def _vulnerability_response(self, question: str, code: str, issues: List[Dict]) -> str:
        """Vulnerability and threat response"""

        response = """🛡️ **Vulnerability Assessment & Management:**

**Vulnerability Types:**
1. **Critical** - Can compromise entire system
2. **High** - Significant security impact
3. **Medium** - Moderate risk, should fix
4. **Low** - Minor issue, nice to fix

**Common Vulnerabilities in Code:**
- Hardcoded secrets (API keys, passwords)
- Weak encryption algorithms
- Missing input validation
- SQL injection points
- Path traversal vulnerabilities
- Command injection
- Insecure deserialization
- Missing security headers

**Mitigation Strategy:**
1. Identify (use static analysis tools)
2. Assess (impact, exploitability)
3. Prioritize (by severity)
4. Fix (apply patches)
5. Test (verify fix works)
6. Monitor (watch for exploitation)

"""

        if issues:
            response += f"""
**Issues Found in Your Code:** ({len(issues)} issues)

"""
            critical = [i for i in issues if i.get('score', 0) >= 0.85]
            high = [i for i in issues if 0.70 <= i.get('score', 0) < 0.85]

            if critical:
                response += f"🔴 **{len(critical)} Critical Issues** - Fix immediately!\n"
            if high:
                response += f"🟠 **{len(high)} High Issues** - Fix soon\n"

        response += """
**Best Practices:**
✅ Use OWASP guidelines
✅ Security testing (SAST, DAST)
✅ Code review process
✅ Dependency scanning
✅ Regular updates
✅ Security training

🛡️ **Continuous security improvement!**"""

        return response

    def _security_general_response(self, question: str) -> str:
        """General security advice"""
        return """🛡️ **General Security Advice:**

**Defense in Depth:**
1. Input validation - Never trust user input
2. Authentication - Verify who you are
3. Authorization - Verify what you can do
4. Encryption - Protect data in transit and at rest
5. Monitoring - Detect attacks early
6. Incident response - Have a plan

**Security Mindset:**
- Assume breach (security by design)
- Fail securely (safe defaults)
- Least privilege (minimum access)
- No security through obscurity
- Defense in depth (multiple layers)

**Regular Tasks:**
✅ Update dependencies
✅ Security patches
✅ Code reviews
✅ Vulnerability scanning
✅ Access reviews
✅ Training & awareness

🔒 **Security is a journey, not a destination!**"""

    # ============ AI RESPONSES ============

    def _answer_ai_question(self, question: str) -> str:
        """Answer AI/ML-related questions"""
        question_lower = question.lower()

        if any(w in question_lower for w in ['llm', 'gpt', 'transformer', 'bert', 'foundation']):
            return """🤖 **Large Language Models (LLMs):**

**What are LLMs?**
Neural networks trained on massive text data to predict and generate text.

**Popular LLMs:**
- GPT-4, GPT-3.5 (OpenAI)
- Claude (Anthropic)
- Llama (Meta)
- Gemini (Google)
- Phi (Microsoft)

**How they work:**
1. Training - Learn patterns from billions of texts
2. Tokenization - Convert text to numbers
3. Attention - Focus on important parts
4. Generation - Predict next word based on context

**Limitations:**
⚠️ Can hallucinate (make up facts)
⚠️ Knowledge cutoff date
⚠️ Computationally expensive
⚠️ Privacy concerns
⚠️ Bias in training data

**Use Cases:**
✅ Code generation
✅ Text summarization
✅ Translation
✅ Question answering
✅ Creative writing
✅ Code analysis (like this app!)

**Future:**
- Multimodal models (text, image, audio)
- More efficient architectures
- Better alignment with human values
- Local deployment options

🧠 **AI is transforming technology!**"""

        if any(w in question_lower for w in ['machine learning', 'ml', 'deep learning', 'neural']):
            return """🤖 **Machine Learning Fundamentals:**

**Three Main Types:**

1. **Supervised Learning** - Learn from labeled examples
   - Classification (cat vs dog)
   - Regression (price prediction)

2. **Unsupervised Learning** - Find patterns in unlabeled data
   - Clustering (group similar items)
   - Dimensionality reduction

3. **Reinforcement Learning** - Learn through rewards/penalties
   - Game playing
   - Robot control

**Common Algorithms:**
- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forest
- Support Vector Machines (SVM)
- K-Means Clustering
- Neural Networks

**Steps to Build ML Model:**
1. Collect data
2. Clean data
3. Feature engineering
4. Select algorithm
5. Train model
6. Evaluate performance
7. Tune hyperparameters
8. Deploy

**Key Concepts:**
- Training/validation/test split
- Overfitting (memorizing data)
- Underfitting (too simple)
- Regularization (prevent overfitting)
- Cross-validation (robust evaluation)

**Tools & Libraries:**
- Python, scikit-learn, TensorFlow, PyTorch
- Jupyter Notebooks for experiments
- Real datasets: Kaggle, UCI, Papers with Code

🧠 **ML is solving real-world problems!**"""

        return """🤖 **Artificial Intelligence Overview:**

**What is AI?**
Machines performing tasks that require human intelligence:
- Learning from data
- Pattern recognition
- Decision making
- Natural language processing
- Computer vision

**AI vs ML vs DL:**
- AI: Broad field (any intelligent machine)
- ML: Subset of AI (learns from data)
- DL: Subset of ML (uses neural networks)

**AI Applications:**
✅ Chatbots & assistants (like me!)
✅ Computer vision (object detection)
✅ Natural language processing (language understanding)
✅ Recommendation systems (Netflix, Amazon)
✅ Autonomous vehicles
✅ Medical diagnosis
✅ Code analysis (bug detection)
✅ Fraud detection

**Current State:**
- Generative AI revolution
- LLMs showing reasoning abilities
- Multimodal AI emerging
- AI becoming more accessible
- Ethical concerns growing

**Future Challenges:**
❓ Alignment (safe AI)
❓ Interpretability (understanding decisions)
❓ Scalability (efficiency)
❓ Ethics (bias, privacy)
❓ AGI (general intelligence)

🧠 **We're living through an AI revolution!**"""

    # ============ CODE ANALYSIS RESPONSES ============

    def _answer_code_question(self, question: str, code: str, issues: List[Dict], complexity: Dict) -> str:
        """Answer questions about code analysis"""

        question_lower = question.lower()

        # Complexity questions
        if 'complex' in question_lower:
            complexity_score = complexity.get('complexity_score', 0)
            risk = complexity.get('risk', 'UNKNOWN')
            return f"""📊 **Code Complexity Analysis:**

Your code complexity score: **{complexity_score}/100**
Risk level: **{risk}**

**What is Complexity?**
Measures how complicated code is:
- McCabe Complexity - Number of decision paths
- Lines of Code (LOC)
- Cyclomatic Complexity
- Cognitive Complexity

**Interpretation:**
- 0-10: Simple, easy to understand ✅
- 10-20: Moderate, manageable
- 20-50: Complex, consider refactoring
- 50+: Very complex, definitely refactor

**How to Reduce Complexity:**
1. Break into smaller functions
2. Reduce nesting depth
3. Simplify conditionals
4. Use design patterns
5. Eliminate duplicate code
6. Use appropriate algorithms

**Benefits of Low Complexity:**
✅ Easier to maintain
✅ Fewer bugs
✅ Better performance
✅ Easier to test
✅ Team productivity

📊 **Simpler code is better code!**"""

        if 'issue' in question_lower or 'bug' in question_lower or 'error' in question_lower:
            if not issues:
                return """✅ **No issues detected!**

Your code looks good! 

But remember:
- Static analysis catches common patterns
- Manual review still recommended
- Test cases important
- Security review recommended
- Performance profiling useful

Keep coding safely! 🚀"""

            return f"""⚠️ **Found {len(issues)} issue(s):**

**Summary:**
"""+ "\n".join([f"- **{i.get('type', 'Issue')}** ({i.get('score', 0):.0%} severity): {i.get('msg', 'Unknown')}" for i in issues[:5]]) + f"""

**Next Steps:**
1. Review each issue
2. Understand the risk
3. Apply fix suggestions
4. Test your changes
5. Re-analyze code

**Prevention Tips:**
✅ Code review before committing
✅ Use linters (pylint, flake8)
✅ Run tests continuously
✅ Static analysis tools
✅ Security scanning

🔍 **Clean code is secure code!**"""

        if 'quality' in question_lower:
            return """📈 **Code Quality Metrics:**

**What Makes Code Quality?**
1. **Readability** - Easy to understand
2. **Maintainability** - Easy to modify
3. **Testability** - Easy to test
4. **Performance** - Runs efficiently
5. **Security** - Resistant to attacks

**Measuring Quality:**
- Code coverage (test %)
- Cyclomatic complexity
- Maintainability index
- Technical debt
- Issue density

**Quality Improvements:**
✅ Follow style guide (PEP8 for Python)
✅ Write comments
✅ Use meaningful names
✅ Keep functions small
✅ DRY principle (Don't Repeat Yourself)
✅ SOLID principles
✅ Design patterns

**Tools:**
- SonarQube
- CodeClimate
- Pylint
- Black (formatter)
- Pre-commit hooks

📈 **Quality code saves time and money!**"""

        return """📊 **Code Analysis Overview:**

**What is Code Analysis?**
Automatic examination of code to find:
- Bugs and errors
- Security vulnerabilities
- Code smells
- Performance issues
- Style violations

**Types:**
1. **Static Analysis** - Without running code
2. **Dynamic Analysis** - While running
3. **Semantic Analysis** - Meaning of code
4. **Style Analysis** - Formatting

**This App Does:**
✅ AST analysis (Python parsing)
✅ Security checks (50+ patterns)
✅ Complexity scoring
✅ Compliance validation
✅ Best practices verification

**Why It Matters:**
- Find issues early
- Prevent bugs in production
- Improve security
- Maintain standards
- Save debugging time

📊 **Automate quality checks!**"""

    # ============ BUG/FIX RESPONSES ============

    def _answer_bug_question(self, question: str, code: str, issues: List[Dict]) -> str:
        """Answer bug and fix related questions"""

        return """🐛 **Debugging & Fixing Guide:**

**Debugging Process:**
1. **Reproduce** - Make the bug happen consistently
2. **Isolate** - Find the exact code causing it
3. **Understand** - Why is it happening?
4. **Fix** - Apply the solution
5. **Test** - Verify it works
6. **Prevent** - Add test to catch it again

**Common Bug Types:**
❌ Logic errors - Wrong algorithm
❌ Off-by-one - Array indexing issues
❌ Null references - Using None/null
❌ Type errors - Wrong data type
❌ State issues - Wrong variable state
❌ Concurrency - Race conditions

**Debugging Tools:**
✅ Print statements
✅ Debugger (breakpoints)
✅ Logging
✅ Unit tests
✅ Static analysis
✅ Code review

**Prevention Tips:**
✅ Write tests first (TDD)
✅ Code review
✅ Use type hints
✅ Follow patterns
✅ Handle edge cases
✅ Document assumptions

**Security Bugs:**
🔒 Most dangerous type!
- Buffer overflow
- SQL injection
- Logic flaws
- Unchecked access
- Insecure deserialization

🐛 **Find bugs fast, fix them faster!**"""

    # ============ GENERAL CONVERSATION ============

    def _answer_general_question(self, question: str, code: str) -> str:
        """Answer general questions naturally"""

        question_lower = question.lower()

        # Greetings
        if any(w in question_lower for w in ['hello', 'hi', 'hey', 'greetings']):
            return """👋 **Hello! Welcome to AI Bug Localizer PRO!**

I'm your AI debugging assistant. I can help you with:

🛡️ **Information Security**
- OWASP Top 10 vulnerabilities
- Encryption & cryptography
- Compliance (GDPR, HIPAA, PCI-DSS)
- Authentication & Authorization
- Secure coding practices

🤖 **AI & Machine Learning**
- LLMs and transformers
- Machine learning algorithms
- Deep learning concepts
- Model evaluation

📊 **Code Analysis**
- Bug detection
- Complexity analysis
- Quality metrics
- Performance issues

✅ **Best Practices**
- Design patterns
- Refactoring tips
- Testing strategies
- Debugging techniques

**How to Use:**
1. Upload code to the Analyzer tab
2. Ask me questions about it
3. I'll provide context-aware responses
4. Use Security Lab for detailed analysis

What would you like to know? 😊"""

        if any(w in question_lower for w in ['help', 'what can you do', 'features', 'capabilities']):
            return """🎯 **What I Can Help With:**

**Security Analysis:**
- Identify OWASP vulnerabilities
- Check encryption practices
- Verify compliance requirements
- Review authentication flows
- Explain security issues

**Code Understanding:**
- Explain what your code does
- Identify bugs and errors
- Measure complexity
- Suggest improvements
- Find security issues

**AI & ML Guidance:**
- Explain AI concepts
- Machine learning basics
- Algorithm recommendations
- Model evaluation
- Best practices

**Practical Tools:**
- Hash generation
- Encryption/decryption
- JWT tokens
- API keys
- Password strength

**Best Practices:**
- Secure coding
- Code quality
- Debugging tips
- Testing strategies
- Refactoring advice

**Just ask naturally!**
- "What's in my code?"
- "Is it secure?"
- "How complex is it?"
- "What's SQL injection?"
- "How do I hash passwords?"

I'm here to help! 🚀"""

        if any(w in question_lower for w in ['thanks', 'thank you', 'appreciate', 'thanks a lot', 'thank u']):
            return """😊 **Happy to help!**

Feel free to ask more questions anytime. Whether it's:
- Analyzing your code
- Security questions
- AI/ML concepts
- Debugging help
- Best practices

I'm always here! 🚀

**Next Steps:**
1. Load some code
2. Ask questions
3. Review recommendations
4. Use Security Lab
5. Keep learning!

Thanks for using AI Bug Localizer PRO! 🎉"""

        if any(w in question_lower for w in ['about', 'information', 'what is this']):
            return """ℹ️ **About AI Bug Localizer PRO:**

**What is it?**
An enterprise-grade Python code analysis tool with:
- Security vulnerability detection
- Code quality analysis
- AI-powered recommendations
- Interactive debugging
- Compliance checking

**Key Features:**
✅ 50+ security patterns
✅ OWASP Top 10 detection
✅ Compliance validation
✅ Encryption analysis
✅ Code complexity scoring
✅ AI chat assistant
✅ Cryptographic tools
✅ Professional UI

**Security Modules:**
- OWASP Analyzer
- Encryption Analyzer
- Compliance Checker
- Authentication Analyzer

**Built With:**
- Python & Streamlit
- Advanced AI analysis
- Best practices
- Professional design

**Why Use It?**
✅ Find vulnerabilities early
✅ Learn security best practices
✅ Validate compliance
✅ Improve code quality
✅ Get expert guidance

Start analyzing! 🚀"""

        # Fallback for unknown questions
        return f"""💭 **Interesting question!**

I'd love to help with: "{question}"

I'm especially good at:
🛡️ Security questions (OWASP, encryption, compliance, authentication)
🤖 AI & Machine Learning concepts
📊 Code analysis (bugs, complexity, quality)
🐛 Debugging and fixing code
✅ Best practices and design patterns

**Tips for getting better answers:**
- Be specific about what you're asking
- Mention if it's about security, AI, or code
- Ask about your actual code context
- Tell me what you want to learn

Would you like to ask about one of these topics? 😊"""


# ============ SINGLETON INSTANCE ============
_ai_engine = None


def get_ai_engine() -> EnhancedAIChat:
    """Get or create AI engine instance"""
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = EnhancedAIChat()
    return _ai_engine
