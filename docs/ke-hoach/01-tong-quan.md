# Kế hoạch dự án: Anti Fake News Focus to Images - Multimodal Fake News Detection

## 0. Tóm tắt dự án

Dự án xây dựng một công cụ hỗ trợ phát hiện nguy cơ tin giả dựa trên **hình ảnh kèm nội dung văn bản**. Trong phạm vi môn Thị giác máy tính và Xử lý ảnh, hệ thống ưu tiên phân tích mối quan hệ giữa ảnh và chữ, đồng thời kết hợp kiểm tra các dấu hiệu đáng ngờ trong văn bản.

Sản phẩm mục tiêu trong 3 tuần là một **Browser Extension (Tiện ích mở rộng trình duyệt)** kết hợp hệ thống backend API. Extension cho phép người dùng quét nhanh nội dung (chọn ảnh và bôi đen văn bản) ngay trên các nền tảng mạng xã hội (Facebook, X, báo mạng...) thông qua **phím tắt hoặc context menu**. Hệ thống sau đó trả về kết quả `Real`, `Fake` hoặc `Suspicious` kèm điểm tin cậy và lý do cảnh báo trực tiếp trên màn hình.

Hướng thiết kế ưu tiên:

- Dùng mô hình pretrained (CLIP) để tiết kiệm tài nguyên.
- Tách biệt rõ ràng Client (Browser Extension) và Server (FastAPI).
- Chú trọng trải nghiệm người dùng nhanh, gọn (quét bằng phím tắt).
- Có thể demo tiếng Việt bằng cách dịch văn bản hoặc tiền xử lý trước khi đưa vào CLIP.

---

# 1. User's Requirement

## 1.1. Nhu cầu người dùng

Người dùng cần một công cụ hỗ trợ đánh giá độ đáng tin cậy của một bài đăng/tin tức trên mạng xã hội dựa trên hai thành phần:

- Hình ảnh đi kèm bài viết.
- Tiêu đề hoặc nội dung văn bản bằng tiếng Việt.

Hệ thống không thay thế người kiểm chứng tin tức, mà đóng vai trò **cảnh báo sớm** khi phát hiện ảnh và chữ có dấu hiệu không khớp, nội dung có tính giật tít, hoặc ảnh có dấu hiệu bất thường.

## 1.2. Đầu vào

- 1 file ảnh: `.jpg`, `.jpeg`, `.png`.
- 1 đoạn văn bản tiếng Việt: tiêu đề, mô tả hoặc nội dung bài đăng.

Ví dụ:

```text
Ảnh: flood_old_image.jpg
Text: "Khẩn cấp! Hà Nội vừa bị ngập lịch sử trong hôm nay, chia sẻ ngay để mọi người biết!"
```

## 1.3. Đầu ra

Hệ thống trả về:

- Kết quả: `Real`, `Fake` hoặc `Suspicious`.
- Điểm tin cậy: từ 0 đến 100%.
- Lý do cảnh báo.
- Các điểm thành phần:
  - Image-text similarity score.
  - Text suspicious score.
  - Optional image manipulation score.

Ví dụ:

```text
Result: Suspicious
Confidence: 78%
Reasons:
- Nội dung văn bản và hình ảnh có độ tương đồng thấp.
- Văn bản có dấu hiệu giật tít/cảm xúc mạnh.
```

## 1.4. Phạm vi sản phẩm trong 3 tuần

Trong 3 tuần, sản phẩm nên ưu tiên:

- Xây dựng được **Backend Server (API)** chạy pipeline AI ổn định.
- Phát triển một **Browser Extension** hoạt động được ở mức prototype (quét ảnh/text qua phím tắt hoặc context menu và hiện popup thông báo).
- Có test case tiếng Việt.
- Có báo cáo rõ logic và mô hình sử dụng.

Không nên đặt mục tiêu:

- Xác minh tin thật/giả tuyệt đối.
- Extension quét DOM tự động hoàn toàn mọi bài viết (auto-scan feed) - tính năng này quá phức tạp và rủi ro.
- Train mô hình deep learning lớn từ đầu.

---

# 2. Features

## 2.1. Kiến trúc Client - Server

Do mô hình AI (CLIP) khá nặng để chạy trực tiếp trên trình duyệt, hệ thống bắt buộc chia làm 2 phần:
- **Backend (FastAPI/Flask)**: Chạy pipeline AI, nhận ảnh/text, phân tích và trả về kết quả JSON.
- **Client (Browser Extension)**: Lắng nghe thao tác người dùng, lấy dữ liệu DOM, gọi API và hiển thị UI cảnh báo.

## 2.2. MVP Features (Các tính năng bắt buộc)

### Feature 1: Quét nội dung bằng Phím tắt / Context Menu (Extension)

Người dùng có thể thao tác trực tiếp trên mạng xã hội:
- Bôi đen một đoạn văn bản nghi ngờ.
- Click chuột phải vào hình ảnh liên quan và chọn "Phân tích tin giả" (hoặc bấm tổ hợp phím tắt).
- Extension sẽ tự động trích xuất URL hình ảnh và đoạn text đã bôi đen để gửi đi.

### Feature 2: Hiển thị kết quả nhanh (Extension)

- Hiển thị kết quả dưới dạng Popup, Toast Notification hoặc Sidebar ngay trên trang web hiện tại.
- Hiển thị trạng thái đang phân tích (Loading spinner).
- Hiển thị kết quả tổng hợp: Nhãn (Real/Fake/Suspicious), phần trăm độ tin cậy và lý do chi tiết.

### Feature 3: API Backend nhận và tiền xử lý dữ liệu

- Cung cấp endpoint POST nhận `image_url` (hoặc ảnh dạng base64) và `text`.
- Xử lý tải ảnh từ URL về server (hoặc decode base64).
- Dịch văn bản tiếng Việt sang tiếng Anh (nếu dùng CLIP nguyên bản tiếng Anh) hoặc xử lý text phù hợp.

### Feature 4: Kiểm tra độ khớp ảnh - chữ (AI Pipeline)

- Ảnh và chữ được đưa vào image encoder và text encoder của CLIP.
- Tính độ tương đồng (cosine similarity) giữa hai embedding.
- Đánh giá khả năng "râu ông nọ cắm cằm bà kia".

### Feature 5: Phân tích dấu hiệu văn bản đáng ngờ (Rule-based)

- Đánh giá các từ khóa mang tính chất giật tít, câu view (`sốc`, `khẩn cấp`, `sự thật che giấu`,...).
- Tính điểm dựa trên cách hành văn (viết hoa toàn bộ, dùng quá nhiều dấu chấm than).
- Đây là module phụ trợ, chạy song song với CLIP để tăng độ chính xác.

### Feature 6: Kết luận tổng hợp và Giải thích

- Backend có hàm logic tổng hợp điểm số từ CLIP và Text Analyzer.
- Cấu trúc lại lý do rõ ràng: "Độ tương đồng ảnh và văn bản thấp", "Văn bản có chứa nhiều từ ngữ giật tít",... để trả về cho Client.

## 2.3. Optional Features

Đây là các tính năng mở rộng nếu nhóm thực hiện xong sớm phần MVP.

### Feature 7: ELA - Error Level Analysis

- Tích hợp thêm script tính toán ELA cho ảnh để phát hiện dấu vết cắt ghép, chỉnh sửa vùng ảnh bằng Photoshop.
- Điểm ELA sẽ được tính thêm vào trọng số cuối cùng.

### Feature 8: Lưu lịch sử và Báo cáo

- Popup Extension có tab lịch sử (History) lưu lại cục bộ (local storage) các nội dung đã kiểm tra.

---

