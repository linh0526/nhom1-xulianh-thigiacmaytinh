# 6. Test

## 6.1. Unit Test

### Test API Endpoint (FastAPI)
- Gọi API `/api/analyze` với ảnh hợp lệ và text hợp lệ -> Trả về HTTP 200 và kết quả JSON.
- Gọi API với ảnh lỗi (không thể tải/không decode được) -> Trả về lỗi 400 rõ ràng.

### Test Extension
- Lắng nghe được sự kiện bấm context menu hoặc phím tắt trên Chrome.
- Trích xuất đúng URL của ảnh và đoạn text bôi đen.
- Hiển thị đúng dữ liệu trả về từ API lên Popup UI.

## 6.2. Scenario Test (Kịch bản demo)

- **Scenario 1:** Ảnh đúng ngữ cảnh + text đúng. (Kỳ vọng: Real)
- **Scenario 2:** Ảnh cũ gắn với text mô tả thiên tai khẩn cấp hôm nay. (Kỳ vọng: Fake/Suspicious)
- **Scenario 3:** Text giật tít nhưng ảnh khớp một phần (Kỳ vọng: Suspicious)

---

# 7. Mở rộng sau này

## 7.1. Mở rộng Extension (Auto-scan)
Nếu phiên bản MVP (bôi đen + bấm phím tắt) chạy ổn định, có thể nâng cấp thuật toán Content Script để Extension tự động phát hiện bài viết trên màn hình, quét tự động và gán cờ đỏ vào bài viết đó trên tường Facebook/Twitter.

## 7.2. Mở rộng model AI
- Sử dụng mô hình PhoBERT kết hợp với ảnh để tạo Multimodal Fusion cho tiếng Việt (thay vì dịch ra tiếng Anh).
- Sử dụng Image Forensics (phân tích mức lỗi nén, EXIF data) để đánh giá độ nguyên bản của bức ảnh.

---

# 8. Rủi ro và cách giảm thiểu

## Rủi ro 1: Lỗi Cross-Origin (CORS) giữa Extension và FastAPI
**Giảm thiểu:** Cấu hình FastAPI `CORSMiddleware` cho phép truy cập từ mọi origin hoặc cấu hình quyền truy cập cụ thể trong manifest.json.

## Rủi ro 2: CLIP không hiểu tốt tiếng Việt
**Giảm thiểu:** Dùng google-translate API dịch sang tiếng Anh trước khi phân tích.

## Rủi ro 3: Model quá nặng, Server phản hồi chậm
**Giảm thiểu:** Thiết kế UI Extension có hiệu ứng Loading (Spinner) và cảnh báo người dùng "Đang xử lý phân tích AI...". Sử dụng pre-trained model nhẹ thay vì các model ViT siêu lớn.
