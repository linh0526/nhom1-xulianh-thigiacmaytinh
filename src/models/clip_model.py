import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image, UnidentifiedImageError
import os

# ====================== GLOBAL CACHE ======================
# Biến toàn cục để lưu model, chỉ load 1 lần duy nhất trong toàn bộ chương trình
# Giúp tránh load model nhiều lần gây tốn thời gian và bộ nhớ
_model = None
_processor = None
_device = None

def load_clip_model(model_name: str = "openai/clip-vit-large-patch14"):
    """
    Load mô hình CLIP và processor.
    
    Args:
        model_name (str): Tên mô hình CLIP trên Hugging Face.
                         Mặc định dùng model nhỏ và nhanh: clip-vit-base-patch32
    
    Returns:
        tuple: (model, processor, device)
    
    Lưu ý: Model chỉ được load 1 lần nhờ cơ chế cache.
    """
    global _model, _processor, _device

    # Nếu đã load rồi thì trả về luôn (Singleton pattern)
    if _model is not None:
        return _model, _processor, _device

    print(f"[CLIP] Đang tải mô hình {model_name}... (Lần đầu có thể mất vài phút vì model này lớn hơn)")

    # Tự động chọn GPU nếu có, ngược lại dùng CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    try:
        model = CLIPModel.from_pretrained(model_name).to(device)
        processor = CLIPProcessor.from_pretrained(model_name)

        # Lưu vào cache
        _model = model
        _processor = processor
        _device = device

        print(f"[CLIP] ✅ Tải mô hình thành công! Chạy trên: {device.upper()}")
        return model, processor, device

    except Exception as e:
        raise RuntimeError(f"❌ Không thể tải mô hình CLIP. Lỗi: {e}")


def compute_clip_similarity_internal(image, text: str, model, processor, device):
    """
    Hàm nội bộ: Tính similarity giữa ảnh và text.
    Không nên gọi trực tiếp từ bên ngoài. Hãy dùng hàm `compute_clip_similarity()` bên dưới.
    """
    # ==================== XỬ LÝ ẢNH ====================
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"❌ Không tìm thấy file ảnh tại: {image}")
        
        try:
            image = Image.open(image).convert("RGB")
        except (UnidentifiedImageError, IOError) as e:
            raise ValueError(f"❌ File {image} không phải là ảnh hợp lệ!") from e

    elif not isinstance(image, Image.Image):
        raise TypeError("❌ Input 'image' phải là đường dẫn (str) hoặc đối tượng PIL.Image")

    # ==================== TÍNH SIMILARITY ====================
    try:
        # Tiền xử lý ảnh và text cho CLIP
        inputs = processor(
            text=[text], 
            images=image, 
            return_tensors="pt", 
            padding=True,
            truncation=True,
            max_length=77
        )

        # Chuyển dữ liệu sang GPU/CPU
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():  # Tắt gradient để tiết kiệm bộ nhớ và nhanh hơn
            outputs = model(**inputs)

            # Lấy vector embedding
            image_features = outputs.image_embeds
            text_features = outputs.text_embeds

            # Chuẩn hóa vector (L2 Normalization)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)

            # Tính Cosine Similarity
            similarity_score = (image_features @ text_features.T).item()

        return {
            "similarity_score": float(similarity_score),
            "image_embedding_shape": list(image_features.shape),
            "text_embedding_shape": list(text_features.shape)
        }

    except Exception as e:
        raise RuntimeError(f"❌ Lỗi khi tính similarity CLIP: {e}")


def compute_clip_similarity(image, text: str):
    """
    **HÀM CHÍNH - ĐƯỢC KHUYẾN CÁO SỬ DỤNG**
    
    Tính độ tương đồng giữa ảnh và văn bản.
    
    Args:
        image: Đường dẫn đến file ảnh (str) hoặc đối tượng PIL.Image
        text (str): Văn bản mô tả (nên là tiếng Anh hoặc đã được dịch bởi TV3)
    
    Returns:
        dict: Kết quả theo đúng format yêu cầu của dự án
    """
    if not text or not text.strip():
        raise ValueError("❌ Text không được để trống!")

    # Load model (chỉ load lần đầu)
    model, processor, device = load_clip_model()
    
    return compute_clip_similarity_internal(image, text, model, processor, device)


def analyze_image_text(image, text: str):
    """
    Hàm tiện ích: Phân tích và đưa ra đánh giá mức độ khớp.
    Dùng cho Predictor (TV6) và Streamlit App.
    """
    result = compute_clip_similarity(image, text)
    sim = result["similarity_score"]

    # Đánh giá mức độ
    if sim >= 0.75:
        level = "Rất khớp (Tin có khả năng thật)"
        color = "green"
        suspicious = False
    elif sim >= 0.50:
        level = "Khớp trung bình"
        color = "orange"
        suspicious = False
    elif sim >= 0.30:
        level = "Lệch ngữ cảnh - Nghi ngờ"
        color = "red"
        suspicious = True
    else:
        level = "Hoàn toàn không khớp - Rất nghi ngờ tin giả"
        color = "darkred"
        suspicious = True

    result.update({
        "match_level": level,
        "match_color": color,
        "is_suspicious": suspicious,
        "interpretation": "Ảnh và nội dung khớp nhau" if not suspicious else "Ảnh và nội dung không khớp → Có dấu hiệu tin giả"
    })

    return result
def get_text_embedding(text: str):
    """
    Trích xuất embedding của văn bản.

    Returns:
        torch.Tensor shape [512]
    """

    if not text or not text.strip():
        raise ValueError("Text không được để trống")

    model, processor, device = load_clip_model()

    inputs = processor(
        text=[text],
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        outputs = model.text_model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"]
        )

        # Lấy vector CLS
        text_features = outputs.pooler_output

        # Project sang không gian CLIP
        text_features = model.text_projection(
            text_features
        )

        # Chuẩn hóa
        text_features = text_features / torch.norm(
            text_features,
            dim=-1,
            keepdim=True
        )

    return text_features.squeeze(0)


def load_image(image):
    """
    Đọc và kiểm tra ảnh đầu vào.

    Hỗ trợ:
    - Đường dẫn ảnh (str)
    - PIL.Image

    Returns:
        PIL.Image
    """

    if isinstance(image, str):

        if not os.path.exists(image):
            raise FileNotFoundError(
                f"Không tìm thấy file ảnh: {image}"
            )

        try:
            image = Image.open(image).convert("RGB")

        except UnidentifiedImageError:
            raise ValueError(
                "File không phải ảnh hợp lệ"
            )

    elif isinstance(image, Image.Image):

        image = image.convert("RGB")

    else:
        raise TypeError(
            "image phải là đường dẫn hoặc PIL.Image"
        )

    return image
def get_image_embedding(image):

    model, processor, device = load_clip_model()

    image = load_image(image)

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        outputs = model.vision_model(
            pixel_values=inputs["pixel_values"]
        )

        image_features = outputs.pooler_output

        image_features = model.visual_projection(
            image_features
        )

        image_features = image_features / torch.norm(
            image_features,
            dim=-1,
            keepdim=True
        )

    return image_features.squeeze(0)

# ====================== TEST NHANH ======================
if __name__ == "__main__":
    print("=== BẮT ĐẦU TEST MODULE CLIP ===")
    
    test_image_path = "test_image.jpg"
    
    # Tạo ảnh test nếu chưa có
    if not os.path.exists(test_image_path):
        img = Image.new('RGB', (400, 300), color='red')
        img.save(test_image_path)
        print(f"✅ Đã tạo ảnh test giả lập tại: {test_image_path}")

    test_text = "A photo of a red background"

    try:
        result = compute_clip_similarity(test_image_path, test_text)
        print("\n✅ KẾT QUẢ TEST THÀNH CÔNG:")
        print(result)
        
        analyze = analyze_image_text(test_image_path, test_text)
        print(f"\n📊 Mức độ khớp: {analyze['match_level']}")
        print(f"🔴 Nghi ngờ tin giả: {'Có' if analyze['is_suspicious'] else 'Không'}")
        
    except Exception as e:
        print(f"❌ Lỗi khi test: {e}")