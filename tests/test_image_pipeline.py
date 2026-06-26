from PIL import Image

from src.image.preprocess import analyze_image


def test_analyze_image_returns_expected_shape(tmp_path):
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (32, 48), color="blue").save(image_path)

    result = analyze_image(str(image_path))

    assert result["image_valid"] is True
    assert result["image_size"] == [32, 48]
    assert 0 <= result["ela_score"] <= 1

