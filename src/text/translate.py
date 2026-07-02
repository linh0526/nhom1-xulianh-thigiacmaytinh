import logging
from deep_translator import GoogleTranslator

def translate_to_english(text: str) -> str:
    """
    Dịch văn bản Tiếng Việt sang Tiếng Anh để đưa vào mô hình CLIP.
    Sử dụng deep_translator để đảm bảo ổn định.
    """
    try:
        if not text or not text.strip():
            return ""
            
        # Dịch từ vi (Việt) sang en (Anh)
        translated = GoogleTranslator(source='vi', target='en').translate(text)
        return translated
        
    except Exception as e:
        logging.error(f"Lỗi dịch thuật: {e}")
        # Nếu mất mạng hoặc lỗi, trả về nguyên gốc tiếng Việt để không bị crash hệ thống
        return text