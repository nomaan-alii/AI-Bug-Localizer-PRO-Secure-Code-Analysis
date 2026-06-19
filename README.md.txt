🧠 AI Bug Localizer PRO

An AI-powered Python debugging, analysis, and auto-fix system built with Streamlit, ML ranking, AST analysis, and runtime inspection.

It detects bugs, ranks issues, estimates complexity, suggests fixes, and provides an interactive dashboard for developers.

🚀 Features
🧪 Code Analysis Engine
AST-based static analysis
Runtime error detection
ML-based issue ranking
Automatic issue prioritization
🧠 AI Intelligence
Complexity scoring system
Risk classification (LOW / MEDIUM / HIGH)
Smart fix suggestions
Copilot-style auto code fixer
📊 Interactive Dashboard
Pie & bar charts for issue distribution
Trend analysis over multiple runs
Real-time bug explorer
🛠️ Auto Fix Engine
Syntax correction
PEP8-style cleanup
Basic structural improvements
Safe code rewriting (non-destructive)
💬 AI Debug Assistant
Ask questions about your code
Get explanations of errors
Get top fix recommendations


🏗️ Project Structure
ai_bug_localizer/
│
├── app.py                         # 🎯 Streamlit UI entry point
│
├── analyzer/                      # 🧠 Core analysis engine
│   ├── static_analysis.py
│   ├── runtime_analysis.py
│   ├── explanation.py
│   ├── fix_suggester.py
│   ├── complexity.py
│   ├── code_corrector.py
│   └── ranking.py                # (fine ranking module)
│
├── core/                          # ⚙️ AI engine layer
│   ├── __init__.py
│   ├── ai_engine.py              # unified analysis pipeline
│   ├── quality_engine.py         # code scoring system
│   ├── report_engine.py          # report generator
│
├── ml/
│   └── scoring.py                # ML-based issue ranking
│
├── utils/
│   └── pylint_runner.py
│
├── components/                   # 🎨 UI components (optional refactor)
│   ├── __init__.py
│   └── ui.py
│
├── tests/                        # 🧪 Test layer
│   ├── test_analyzer.py
│   └── test_engine.py
│
├── assets/
│   └── styles.css
│
├── requirements.txt
└── README.md


⚙️ Installation
1. Clone the repository
git clone https://github.com/your-username/ai-bug-localizer.git
cd ai-bug-localizer

2. Create virtual environment
python -m venv test_env
test_env\Scripts\activate   # Windows

3. Install dependencies
pip install -r requirements.txt

▶️ Run the Application
streamlit run app.py

Then open:

http://localhost:8501

🧪 Run Tests
python -m pytest tests/

🧠 Core Workflow
User Code
   ↓
AST Analysis + Runtime Check
   ↓
ML Issue Ranking
   ↓
Complexity Engine
   ↓
AI Fix Suggestion Engine
   ↓
Streamlit Dashboard


📊 Output Insights
🔴 High Risk Issues
🟠 Medium Risk Issues
🟢 Low Risk Issues
🧠 Complexity Score
📈 Trend History
🛠 Auto Fixed Code
🛠 Tech Stack


Python 3.10+
Streamlit
Plotly
AST (Abstract Syntax Tree)
Machine Learning Ranking Model
Pytest


📌 Future Improvements
GPT-based explanation engine
Docker deployment
GitHub Actions CI/CD
Multi-language support
Live collaborative debugging


👨‍💻 Author

Built by AI Engineering Project (Student System)
Focus: Intelligent Debugging + Code Quality Automation

📄 License

This project is for educational and research purposes.