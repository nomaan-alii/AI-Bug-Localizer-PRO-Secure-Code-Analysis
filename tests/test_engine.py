from core.ai_engine import analyze_code

def test_ai_pipeline():
    code = "print('hello world')"

    result = analyze_code(code)

    assert "issues" in result
    assert "complexity" in result
    assert isinstance(result["issues"], list)
    assert isinstance(result["complexity"], dict)