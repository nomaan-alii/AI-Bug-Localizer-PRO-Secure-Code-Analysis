from analyzer.static_analysis import analyze_ast
from analyzer.runtime_analysis import run_code
from analyzer.complexity import compute_complexity

def test_ast_analysis():
    code = "print('hello')"
    result = analyze_ast(code)
    assert isinstance(result, list)

def test_runtime_analysis():
    code = "print(x)"  # undefined variable
    result = run_code(code)
    assert isinstance(result, list)

def test_complexity():
    code = "for i in range(10): print(i)"
    result = compute_complexity(code)
    assert "complexity_score" in result