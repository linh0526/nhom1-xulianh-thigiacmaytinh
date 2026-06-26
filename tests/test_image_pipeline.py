import pytest
from PIL import Image

from src.image.preprocess import analyze_image, load_image, preprocess_image


def create_sample_image(path, image_format="JPEG"):
    image = Image.new("RGB", (640, 480), color="blue")
    image.save(path, format=image_format)


def test_load_image_reads_jpg_and_converts_to_rgb(tmp_path):
    image_path = tmp_path / "sample.jpg"
    create_sample_image(image_path, "JPEG")

    image = load_image(str(image_path))

    assert image.mode == "RGB"
    assert image.size == (640, 480)


def test_load_image_reads_png_and_converts_to_rgb(tmp_path):
    image_path = tmp_path / "sample.png"
    create_sample_image(image_path, "PNG")

    image = load_image(str(image_path))

    assert image.mode == "RGB"
    assert image.size == (640, 480)


def test_preprocess_image_resizes_to_clip_input_size():
    image = Image.new("RGB", (640, 480), color="red")

    processed = preprocess_image(image)

    assert processed.mode == "RGB"
    assert processed.size == (224, 224)


def test_analyze_image_returns_expected_shape(tmp_path):
    image_path = tmp_path / "sample.jpg"
    create_sample_image(image_path, "JPEG")

    result = analyze_image(str(image_path))

    assert result["image_path"] == str(image_path)
    assert result["image_valid"] is True
    assert result["image_size"] == [640, 480]
    assert isinstance(result["ela_score"], float)
    assert result["ela_image_path"] is None
    assert isinstance(result["image_reasons"], list)


def test_load_image_rejects_missing_file():
    with pytest.raises(FileNotFoundError):
        load_image("missing_image.jpg")


def test_load_image_rejects_unsupported_format(tmp_path):
    text_path = tmp_path / "sample.txt"
    text_path.write_text("not an image")

    with pytest.raises(ValueError, match="Unsupported image format"):
        load_image(str(text_path))


def test_analyze_image_uses_ela_score(tmp_path):
    image_path = tmp_path / "checkerboard.png"
    image = Image.new("RGB", (32, 32), color="white")

    for x in range(0, 32, 2):
        for y in range(0, 32, 2):
            image.putpixel((x, y), (0, 0, 0))

    image.save(image_path)

    result = analyze_image(str(image_path))

    assert result["ela_score"] > 0