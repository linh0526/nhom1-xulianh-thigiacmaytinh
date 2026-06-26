from PIL import Image


def load_image(image_path: str) -> Image.Image:
    image = Image.open(image_path)
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

