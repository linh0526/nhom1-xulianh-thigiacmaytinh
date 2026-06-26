def build_reasons(similarity_score: float, text_result: dict, image_result: dict) -> list[str]:
    reasons = []

    if similarity_score < 0.25:
        reasons.append("Nội dung văn bản và hình ảnh có độ tương đồng rất thấp (không liên quan).")

    reasons.extend(text_result.get("suspicious_reasons", []))
    reasons.extend(image_result.get("image_reasons", []))

    if image_result.get("ela_score", 0.0) > 0.6:
        reasons.append("Ảnh có dấu hiệu bất thường về nền hoặc có thể đã bị chỉnh sửa cắt ghép.")

    if not reasons:
        reasons.append("Không phát hiện dấu hiệu bất thường rõ ràng.")

    return reasons
