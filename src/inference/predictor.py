from src.config import (
    FAKE_THRESHOLD,
    IMAGE_MANIPULATION_WEIGHT,
    SIMILARITY_WEIGHT,
    SUSPICIOUS_THRESHOLD,
    TEXT_SUSPICIOUS_WEIGHT,
)
from src.image.preprocess import analyze_image
from src.inference.explanation import build_reasons
from src.models.clip_model import compute_clip_similarity
from src.text.suspicious_score import analyze_text


def classify_fake_score(fake_score: float) -> str:
    if fake_score >= FAKE_THRESHOLD:
        return "Fake"
    if fake_score >= SUSPICIOUS_THRESHOLD:
        return "Suspicious"
    return "Real"


def predict_fake_news(image_path: str, text: str) -> dict:
    image_result = analyze_image(image_path)
    text_result = analyze_text(text)
    clip_result = compute_clip_similarity(image_path, text_result["translated_text"])

    similarity = clip_result["similarity_score"]
    text_suspicious = text_result["suspicious_score"]
    image_manipulation = image_result["ela_score"]

    fake_score = (
        SIMILARITY_WEIGHT * (1 - similarity)
        + TEXT_SUSPICIOUS_WEIGHT * text_suspicious
        + IMAGE_MANIPULATION_WEIGHT * image_manipulation
    )
    fake_score = round(min(max(fake_score, 0.0), 1.0), 3)

    result = classify_fake_score(fake_score)
    confidence = round(max(fake_score, 1 - fake_score) * 100)

    return {
        "result": result,
        "confidence": confidence,
        "scores": {
            "similarity": round(similarity, 3),
            "text_suspicious": round(text_suspicious, 3),
            "image_manipulation": round(image_manipulation, 3),
            "fake_score": fake_score,
        },
        "reasons": build_reasons(similarity, text_result, image_result),
    }

