from pathlib import Path
import tempfile

import numpy as np
from PIL import Image, ImageChops, ImageEnhance


def create_ela_image(image_path: str, quality: int = 90) -> Image.Image:
    original = Image.open(image_path).convert("RGB")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        compressed_path = tmp.name

    original.save(compressed_path, "JPEG", quality=quality)
    compressed = Image.open(compressed_path).convert("RGB")
    diff = ImageChops.difference(original, compressed)

    extrema = diff.getextrema()
    max_diff = max(channel[1] for channel in extrema)
    scale = 255.0 / max_diff if max_diff else 1.0

    Path(compressed_path).unlink(missing_ok=True)
    return ImageEnhance.Brightness(diff).enhance(scale)


def calculate_ela_score(image_path: str) -> float:
    ela_image = create_ela_image(image_path)
    arr = np.asarray(ela_image).astype("float32") / 255.0
    return float(np.clip(arr.mean(), 0.0, 1.0))

