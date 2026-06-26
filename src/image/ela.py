from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image, ImageChops, ImageStat


def calculate_ela_score(image_path: str, quality: int = 90) -> float:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with Image.open(path) as image:
        original = image.convert("RGB")

        with NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            temp_path = Path(tmp.name)

        try:
            original.save(temp_path, "JPEG", quality=quality)
            compressed = Image.open(temp_path).convert("RGB")

            diff = ImageChops.difference(original, compressed)
            stat = ImageStat.Stat(diff)

            mean_diff = sum(stat.mean) / len(stat.mean)
            return round(mean_diff / 255, 6)
        finally:
            temp_path.unlink(missing_ok=True)