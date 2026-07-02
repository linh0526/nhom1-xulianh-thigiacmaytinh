import os
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def calculate_ela_score(image_path: str, quality: int = 90) -> float:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Tạo file tạm và đóng luồng (file descriptor) ngay lập tức để tránh lỗi Permission trên Windows
    fd, temp_path_str = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    temp_path = Path(temp_path_str)

    try:
        # Sử dụng context manager (with) cho cả ảnh gốc và ảnh nén để tránh rò rỉ bộ nhớ
        with Image.open(path) as image:
            original = image.convert("RGB")
            original.save(temp_path, "JPEG", quality=quality)

        with Image.open(temp_path) as compressed_img:
            compressed = compressed_img.convert("RGB")
            
            diff = ImageChops.difference(original, compressed)
            stat = ImageStat.Stat(diff)

            mean_diff = sum(stat.mean) / len(stat.mean)
            return round(mean_diff / 255, 6)
    finally:
        # Đảm bảo xóa file tạm an toàn
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)