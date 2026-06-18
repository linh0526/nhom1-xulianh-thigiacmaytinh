from src.text.preprocess import clean_text
from src.text.translate import translate_to_english


SUSPICIOUS_KEYWORDS = [
    "soc",
    "sốc",
    "khan cap",
    "khẩn cấp",
    "chia se ngay",
    "chia sẻ ngay",
    "su that bi che giau",
    "sự thật bị che giấu",
    "khong ai noi cho ban",
    "không ai nói cho bạn",
    "100% su that",
    "100% sự thật",
    "canh bao",
    "cảnh báo",
    "dung bo qua",
    "đừng bỏ qua",
]


def calculate_suspicious_score(text: str) -> dict:
    normalized = clean_text(text).lower()
    reasons = []
    score = 0.0

    matched_keywords = [keyword for keyword in SUSPICIOUS_KEYWORDS if keyword in normalized]
    if matched_keywords:
        score += min(0.6, 0.15 * len(matched_keywords))
        reasons.append("Van ban co tu khoa giat tit hoac canh bao manh.")

    exclamation_count = normalized.count("!")
    if exclamation_count >= 2:
        score += min(0.2, exclamation_count * 0.05)
        reasons.append("Van ban dung nhieu dau cham than.")

    if len(normalized) < 20:
        score += 0.1
        reasons.append("Van ban qua ngan de xac minh ngu canh.")

    return {
        "suspicious_score": round(min(score, 1.0), 3),
        "suspicious_reasons": reasons,
    }


def analyze_text(text: str) -> dict:
    clean = clean_text(text)
    suspicious = calculate_suspicious_score(clean)

    return {
        "original_text": text,
        "clean_text": clean,
        "translated_text": translate_to_english(clean),
        "suspicious_score": suspicious["suspicious_score"],
        "suspicious_reasons": suspicious["suspicious_reasons"],
    }

