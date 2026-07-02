import logging

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

# 🚀 IMPORT MODULE FACT-CHECKER MỚI
from src.inference.fact_checker import verify_claim_with_llm


def classify_fake_score(fake_score: float) -> str:
    if fake_score >= FAKE_THRESHOLD:
        return "Fake"
    if fake_score >= SUSPICIOUS_THRESHOLD:
        return "Suspicious"
    return "Real"


def predict_fake_news(image_path: str, text: str) -> dict:
    try:
        image_result = analyze_image(image_path)
        text_result = analyze_text(text)
        clip_result = compute_clip_similarity(image_path, text_result["translated_text"])
        
        # 🚀 GỌI AI LÊN MẠNG XÁC MINH SỰ THẬT
        logging.info("Đang tra cứu Internet...")
        fact_check_result = verify_claim_with_llm(text_result["clean_text"])
        
    except Exception as e:
        logging.error(f"Lỗi trong quá trình phân tích: {e}")
        raise ValueError(f"Không thể phân tích dữ liệu đầu vào: {str(e)}")

    raw_similarity = clip_result["similarity_score"]
    text_suspicious = text_result["suspicious_score"]
    image_manipulation = image_result["ela_score"]

    # ==========================================
    # 1. TÍNH ĐIỂM CƠ BẢN (Với công thức chuẩn hóa)
    # ==========================================
    MIN_SIM = 0.14
    MAX_SIM = 0.25
    normalized_similarity = (raw_similarity - MIN_SIM) / (MAX_SIM - MIN_SIM)
    normalized_similarity = max(0.0, min(normalized_similarity, 1.0))

    base_fake_score = (
        SIMILARITY_WEIGHT * (1 - normalized_similarity)
        + TEXT_SUSPICIOUS_WEIGHT * text_suspicious
        + IMAGE_MANIPULATION_WEIGHT * image_manipulation
    )
    
    # ==========================================
    # 2. ĐIỀU CHỈNH ĐIỂM BẰNG KẾT QUẢ TÌM KIẾM WEB
    # ==========================================
    llm_adjustment = 0.0
    if fact_check_result.get("status") == "Fake":
        llm_adjustment = 0.35  # Phạt thật nặng nếu mạng Internet xác nhận là tin giả
    elif fact_check_result.get("status") == "Real":
        llm_adjustment = -0.35 # Giảm điểm Fake (Thưởng) nếu báo chí chính thống xác nhận là sự kiện thật
    elif fact_check_result.get("status") == "Unverified":
        llm_adjustment = 0.20  # THÊM DÒNG NÀY: Phạt điểm cộng dồn nếu không có báo chí đưa tin
        
    fake_score = base_fake_score + llm_adjustment
    
    # Đảm bảo điểm cuối cùng không bị âm hoặc vượt quá 1.0
    fake_score = round(min(max(fake_score, 0.0), 1.0), 3)

    # ==========================================
    # 3. CẬP NHẬT LÝ DO VÀ TRẢ KẾT QUẢ
    # ==========================================
    reasons = build_reasons(raw_similarity, text_result, image_result)
    if raw_similarity >= 0.2:
        reasons = [r for r in reasons if "tương đồng rất thấp" not in r]
        
    # Thêm lý do thu thập được từ Internet vào danh sách
    if fact_check_result.get("status") not in ["Error", "Unknown"]:
        reasons.append(f"🔍 Kết quả tra cứu Internet: {fact_check_result.get('reason')}")

    result = classify_fake_score(fake_score)
    confidence = round(max(fake_score, 1 - fake_score) * 100)

    return {
        "result": result,
        "confidence": confidence,
        "tags": text_result.get("tags", []),
        "scores": {
            "similarity": round(raw_similarity, 3), 
            "text_suspicious": round(text_suspicious, 3),
            "image_manipulation": round(image_manipulation, 3),
            "fact_check_adjustment": llm_adjustment,
            "fake_score": fake_score,
        },
        "fact_check_status": fact_check_result.get("status"),
        "reasons": reasons,
    }