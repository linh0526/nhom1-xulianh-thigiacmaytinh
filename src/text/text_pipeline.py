import re

class TextPipeline:
    def __init__(self):
        # Danh sách từ dừng (Stopwords) tiếng Việt cơ bản
        # Giúp loại bỏ những từ đệm vô nghĩa khi trích xuất từ khóa cốt lõi
        self.stopwords = [
            "và", "của", "được", "tại", "với", "trong", "cho", "là", "các", "những", 
            "thì", "mà", "đến", "theo", "đã", "đang", "sẽ", "vừa", "ra", "vào",
            "ở", "như", "này", "đó", "bị", "bởi", "do", "về", "để", "lại"
        ]

    def clean_text(self, text):
        """
        Bước 1: Làm sạch văn bản thô
        - Chuyển về chữ thường để đồng bộ văn bản
        - Xóa toàn bộ liên kết URL (tin giả mạng xã hội rất hay chèn link)
        - Xóa các ký tự đặc biệt, icon và dấu câu
        - Xóa các khoảng trắng thừa
        """
        if not text:
            return ""
        
        # 1. Chuyển về chữ thường
        text = text.lower()
        
        # 2. Xóa các URL (định dạng http://, https:// hoặc www.)
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # 3. Xóa ký tự đặc biệt, icon (chỉ giữ lại chữ cái, số và khoảng trắng)
        text = re.sub(r'[^\w\s]', '', text)
        
        # 4. Xóa khoảng trắng thừa và ký tự xuống dòng (\n)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def extract_keywords(self, text, top_n=5):
        """
        Bước 2: Lọc từ khóa quan trọng từ bài báo
        - Làm sạch văn bản thông qua hàm clean_text()
        - Tách câu thành danh sách các từ đơn lẻ
        - Loại bỏ các từ dừng và từ nhiễu quá ngắn (1 ký tự)
        - Loại bỏ từ trùng lặp để giữ lại các từ khóa độc nhất
        """
        cleaned_text = self.clean_text(text)
        
        # Tách văn bản thành danh sách các từ dựa trên khoảng trắng
        words = cleaned_text.split()
        
        # Lọc từ: Bỏ từ thuộc danh sách stopwords và từ viết tắt/icon thừa (độ dài <= 1)
        filtered_words = [word for word in words if word not in self.stopwords and len(word) > 1]
        
        # Sử dụng set() để loại bỏ hoàn toàn các từ trùng lặp
        unique_keywords = list(set(filtered_words))
        
        # Trả về số lượng top_n từ khóa đầu tiên theo yêu cầu
        return unique_keywords[:top_n]


# ==============================================================================
# ĐOẠN CODE CHẠY KIỂM TRA THỬ NGHIỆM TRỰC TIẾP (MÔI TRƯỜNG LOCAL)
# ==============================================================================
if __name__ == "__main__":
    # Khởi tạo đối tượng xử lý văn bản
    pipeline = TextPipeline()
    
    # Đoạn tin tức mẫu (vừa chứa chữ hoa, ký tự đặc biệt, khoảng trắng thừa và link URL)
    sample_news = "Cảnh báo khẩn cấp: Xuất hiện hình ảnh GIẢ MẠO về lũ lụt dữ dội tại Hà Nội trên Facebook ở đường link https://tin-tuc-fake.com/chinh-sua-anh !!!"
    
    print("--- KIỂM TRA HỆ THỐNG XỬ LÝ VĂN BẢN (TEXT PIPELINE) ---")
    print("\n1. Văn bản thô ban đầu:\n", sample_news)
    
    cleaned = pipeline.clean_text(sample_news)
    print("\n2. Văn bản sau khi được làm sạch (Cleaned Text):\n", cleaned)
    
    keywords = pipeline.extract_keywords(sample_news, top_n=6)
    print("\n3. Danh sách các từ khóa quan trọng lọc được:\n", keywords)