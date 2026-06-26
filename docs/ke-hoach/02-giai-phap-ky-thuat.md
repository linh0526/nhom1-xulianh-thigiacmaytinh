# 3. Tech Solutions

## 3.1. Hướng tiếp cận tổng thể

Phương pháp chính:
```text
Pretrained Model + Rule-based Scoring + FastAPI Backend + Browser Extension
```

Lý do:
- Đáp ứng trải nghiệm người dùng nhanh chóng trên nền tảng mạng xã hội (bôi đen text, chọn ảnh bằng phím tắt).
- Thời gian chỉ có 3 tuần nên cần phân chia rõ Server xử lý nặng và Client gọn nhẹ.
- Nhóm ưu tiên sử dụng model Pretrained để không tốn thời gian train lại model lớn.

## 3.2. Công nghệ đề xuất

| Thành phần | Công nghệ đề xuất | Vai trò |
|---|---|---|
| Client (Frontend) | Chrome/Edge Extension (HTML/CSS/JS, Manifest V3) | Lắng nghe phím tắt/context menu, lấy ảnh và text, gọi API và hiện popup kết quả. |
| Server (Backend) | FastAPI (Python) | Nhận request từ Extension, chạy pipeline AI và trả về JSON. |
| Xử lý ảnh | PIL, OpenCV | Đọc ảnh, resize, chuẩn bị input. |
| AI image-text | CLIP pretrained | Tính độ tương đồng giữa ảnh và chữ (Cosine similarity). |
| Xử lý tiếng Việt | Module dịch (google-translate) hoặc API dịch | Chuyển text tiếng Việt sang tiếng Anh trước khi đưa vào mô hình CLIP. |
| Text Analyzer | Python rule-based scoring | Đếm từ khóa giật tít, dấu chấm than để tìm điểm đáng ngờ trong text. |

## 3.3. Mô hình AI đề xuất

### CLIP (Contrastive Language-Image Pre-Training)
- CLIP là mô hình học được mối quan hệ giữa ảnh và văn bản. Nó có thể trích xuất đặc trưng (embedding) cho cả ảnh và văn bản rồi tính khoảng cách (similarity).
- Điểm yếu: Hỗ trợ tiếng Anh tốt nhất, nên cần dịch tiếng Việt sang tiếng Anh.

### Rule-based Text Analyzer
- Phân tích từ khóa giật tít, số lượng ký tự in hoa, dấu câu quá đà.

---

# 4. Logic + AI

## 4.1. Kiến trúc pipeline MVP

```text
[Browser Extension]
    |-- Lấy ảnh + Text bôi đen
    |-- Gửi POST /api/analyze
            |
            v
[FastAPI Backend]
    |-- Image Preprocessing (Resize, Normalize)
    |-- Text Preprocessing (Clean, Translate to English)
    |
    |-- CLIP Image Encoder -> image embedding
    |-- CLIP Text Encoder -> text embedding
    |-- Cosine Similarity -> image_text_similarity_score
    |
    |-- Text Suspicious Analysis -> text_suspicious_score
    |
    |-- Final Scoring Logic -> Real / Fake / Suspicious
    |-- Explanation Generator -> Lý do cảnh báo
            |
            v
[Browser Extension]
    |-- Hiển thị kết quả UI dạng Toast / Popup
```

## 4.2. Logic tính điểm đề xuất

- `similarity_score`: 0 -> 1 (càng cao càng khớp)
- `text_suspicious_score`: 0 -> 1 (càng cao càng giật tít)

Công thức fake score tham khảo:
```text
fake_score = 0.60 * (1 - similarity_score) + 0.40 * text_suspicious_score
```

Phân loại:
- `Fake` nếu fake_score >= 0.70
- `Suspicious` nếu fake_score >= 0.45
- `Real` nếu fake_score < 0.45

## 4.3. Sinh lý do cảnh báo
- Similarity < 0.25: "Hình ảnh và văn bản không ăn nhập với nhau."
- Text Suspicious > 0.6: "Văn bản chứa từ ngữ giật tít câu view."
