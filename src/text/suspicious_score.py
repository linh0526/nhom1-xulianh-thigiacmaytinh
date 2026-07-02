import re
from src.text.preprocess import clean_text
from src.text.translate import translate_to_english

SUSPICIOUS_KEYWORDS = [
    "soc", "sốc", "khan cap", "khẩn cấp", "chia se ngay", "chia sẻ ngay",
    "su that bi che giau", "sự thật bị che giấu", "khong ai noi cho ban",
    "không ai nói cho bạn", "100% su that", "100% sự thật", "canh bao",
    "cảnh báo", "dung bo qua", "đừng bỏ qua",
]

VIOLENT_KEYWORDS = [
    "giet", "giết", "danh dam", "đánh đấm", "dam mau", "đẫm máu", 
    "hanh hung", "hành hung", "cat co", "cắt cổ", "bao hanh", "bạo hành", 
    "chem", "chém", "dan ap", "đàn áp", "tham sat", "thảm sát"
]

INCITING_KEYWORDS = [
    "bieu tinh", "biểu tình", "bạo loạn", "bao loan", "chong pha", "chống phá",
    "lat do", "lật đổ", "noi loang", "nổi loạn", "tay chay", "tẩy chay",
    "dap pha", "đập phá", "dao chinh", "đảo chính", "xuong duong", "xuống đường"
]

def _find_keywords(text: str, keywords: list) -> list:
    """Hàm hỗ trợ tìm kiếm từ khóa chính xác bằng Regex"""
    matched = []
    for kw in keywords:
        # Dùng \b để đánh dấu ranh giới từ, tránh lỗi "soc" bắt nhầm trong "socola"
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
            matched.append(kw)
    return matched

def calculate_suspicious_score(text: str) -> dict:
    normalized = clean_text(text).lower()
    reasons = []
    score = 0.0
    tags = []

    # Giật tít
    matched_suspicious = _find_keywords(normalized, SUSPICIOUS_KEYWORDS)
    if matched_suspicious:
        score += min(0.6, 0.15 * len(matched_suspicious))
        reasons.append("Văn bản có chứa từ khóa giật tít hoặc cảnh báo mạnh.")
        tags.append("Giật tít") # Đã bổ sung Tag bị thiếu

    # Bạo lực
    matched_violent = _find_keywords(normalized, VIOLENT_KEYWORDS)
    if matched_violent:
        score += min(0.8, 0.2 * len(matched_violent))
        reasons.append("Văn bản chứa ngôn từ bạo lực, nguy hiểm.")
        tags.append("Bạo lực")

    # Kích động
    matched_inciting = _find_keywords(normalized, INCITING_KEYWORDS)
    if matched_inciting:
        score += min(0.8, 0.2 * len(matched_inciting))
        reasons.append("Văn bản có dấu hiệu kích động, bạo loạn.")
        tags.append("Kích động")

    exclamation_count = normalized.count("!")
    if exclamation_count >= 2:
        score += min(0.2, exclamation_count * 0.05)
        reasons.append("Văn bản sử dụng quá nhiều dấu chấm than.")

    if len(normalized) < 20:
        score += 0.1
        reasons.append("Văn bản quá ngắn, thiếu ngữ cảnh xác thực.")

    return {
        "suspicious_score": round(min(score, 1.0), 3),
        "suspicious_reasons": reasons,
        "tags": tags
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
        "tags": suspicious["tags"]
    }