import json
import logging

# Đã import thư viện mới theo đúng cảnh báo của hệ thống
from ddgs import DDGS
from google import genai

# THAY API KEY CỦA BẠN VÀO ĐÂY NHÉ!
GEMINI_API_KEY = "THAY_API_KEY_CUA_BAN_VAO_DAY" 

def search_web_for_truth(claim: str, max_results: int = 3) -> str:
    """
    Tự động tra cứu Google/DuckDuckGo để tìm các bài báo liên quan đến nội dung.
    """
    print(f"🔍 Đang truy vết thông tin trên mạng: '{claim}'...")
    try:
        results = DDGS().text(claim, max_results=max_results)
        
        # Gom các kết quả tìm kiếm lại thành một đoạn văn bản
        search_context = ""
        for i, r in enumerate(results):
            search_context += f"Nguồn {i+1} ({r.get('title', '')}): {r.get('body', '')}\n"
            
        return search_context
    except Exception as e:
        logging.error(f"Lỗi khi tìm kiếm web: {e}")
        return ""

def verify_claim_with_llm(claim: str) -> dict:
    """
    Dùng Gemini đọc kết quả tìm kiếm và kết luận Thật/Giả.
    """
    # 1. Tìm bằng chứng trên mạng
    evidence = search_web_for_truth(claim)
    if not evidence:
        return {"status": "Unknown", "reason": "Không tìm thấy thông tin trên mạng để xác minh (Hoặc bị chặn tìm kiếm)."}

    # 2. Cấu hình AI Gemini theo chuẩn SDK mới nhất
    print("🤖 Đang phân tích bằng chứng...")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        # 3. Ra lệnh cho AI (Prompt Engineering)
        prompt = f"""
        Bạn là một chuyên gia kiểm chứng tin giả (Fact-checker) tại Việt Nam.
        Nhiệm vụ của bạn là xác minh xem thông tin người dùng đưa ra là THẬT hay GIẢ dựa trên bằng chứng tìm được trên mạng.

        THÔNG TIN CẦN XÁC MINH: "{claim}"
        
        BẰNG CHỨNG TÌM ĐƯỢC TRÊN MẠNG:
        {evidence}

        Hãy phân tích và trả về đúng định dạng JSON sau (KHÔNG chứa markdown, KHÔNG bọc trong ```json):
        {{
            "status": "Real" hoặc "Fake" hoặc "Unverified",
            "reason": "Giải thích ngắn gọn lý do vì sao (dựa trên bằng chứng)"
        }}
        """
        
        # Gọi model thế hệ mới của Google
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Xử lý text để ép về JSON chuẩn
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(raw_text)
        return result
        
    except Exception as e:
        logging.error(f"Lỗi khi AI xử lý: {e}")
        return {"status": "Error", "reason": "AI không thể phân tích vào lúc này (Vui lòng kiểm tra lại API Key)."}
    