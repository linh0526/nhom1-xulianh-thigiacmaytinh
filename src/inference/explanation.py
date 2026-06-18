def build_reasons(similarity_score: float, text_result: dict, image_result: dict) -> list[str]:
    reasons = []

    if similarity_score < 0.25:
        reasons.append("Noi dung van ban va hinh anh co do tuong dong thap.")

    reasons.extend(text_result.get("suspicious_reasons", []))
    reasons.extend(image_result.get("image_reasons", []))

    if image_result.get("ela_score", 0.0) > 0.6:
        reasons.append("Anh co dau hieu bat thuong ve nen hoac chinh sua.")

    if not reasons:
        reasons.append("Khong phat hien dau hieu bat thuong ro rang.")

    return reasons

