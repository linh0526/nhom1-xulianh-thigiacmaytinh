from pathlib import Path

from PIL import Image

from src.inference.predictor import predict_fake_news


def test_predictor_returns_expected_shape(tmp_path):
    image_path = tmp_path / "sample.jpg"
    Image.new("RGB", (64, 64), color="white").save(image_path)

    result = predict_fake_news(str(image_path), "Noi dung bai viet binh thuong")

    assert result["result"] in {"Real", "Fake", "Suspicious"}
    assert 0 <= result["confidence"] <= 100
    assert "scores" in result
    assert isinstance(result["reasons"], list)

