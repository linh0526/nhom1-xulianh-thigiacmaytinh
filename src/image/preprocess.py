from pathlib import Path

from PIL import Image

from src.image.ela import calculate_ela_score


SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
DEFAULT_CLIP_IMAGE_SIZE = (224, 224)
ELA_WARNING_THRESHOLD = 0.25


