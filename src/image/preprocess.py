from pathlib import Path

from PIL import Image


SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def load_image(image_path: str) -> Image.Image:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format: {path.suffix}. "
            "Supported formats are .jpg, .jpeg, .png."
        )

    with Image.open(path) as image:
        return image.convert("RGB")


def analyze_image(image_path: str) -> dict:
    image = load_image(image_path)
    width, height = image.size

    return {
        "image_path": image_path,
        "image_valid": True,
        "image_size": [width, height],
        "ela_score": 0.0,
        "ela_image_path": None,
        "image_reasons": [],
    }