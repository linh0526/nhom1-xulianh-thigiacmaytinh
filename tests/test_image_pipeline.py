from pathlib import Path

from PIL import Image

from src.image.ela import calculate_ela_score


SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
DEFAULT_CLIP_IMAGE_SIZE = (224, 224)
ELA_WARNING_THRESHOLD = 0.25


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


def preprocess_image(
    image: Image.Image,
    target_size: tuple[int, int] = DEFAULT_CLIP_IMAGE_SIZE,
) -> Image.Image:
    return image.convert("RGB").resize(
        target_size,
        Image.Resampling.LANCZOS
    )


def analyze_image(image_path: str) -> dict:
    image = load_image(image_path)

    width, height = image.size

    ela_score = calculate_ela_score(image_path)

    image_reasons = []

    if ela_score > ELA_WARNING_THRESHOLD:
        image_reasons.append(
            "Image has unusual compression/manipulation patterns."
        )

    return {
        "image_path": image_path,
        "image_valid": True,
        "image_size": [width, height],
        "ela_score": round(ela_score, 3),
        "ela_image_path": None,
        "image_reasons": image_reasons,
    }