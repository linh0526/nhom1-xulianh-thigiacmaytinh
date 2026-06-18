from src.text.suspicious_score import analyze_text


def test_analyze_text_returns_expected_shape():
    result = analyze_text("Khan cap! Chia se ngay!")

    assert "clean_text" in result
    assert "translated_text" in result
    assert 0 <= result["suspicious_score"] <= 1
    assert isinstance(result["suspicious_reasons"], list)

