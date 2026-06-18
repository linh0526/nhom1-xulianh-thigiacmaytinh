# Kế hoạch dự án: Anti Fake News Focus to Images - Multimodal Fake News Detection

## 0. Tóm tắt dự án

Dự án xây dựng một ứng dụng hỗ trợ phát hiện nguy cơ tin giả dựa trên **hình ảnh kèm nội dung văn bản**. Trong phạm vi môn Thị giác máy tính và Xử lý ảnh, hệ thống ưu tiên phân tích mối quan hệ giữa ảnh và chữ, đồng thời có thể mở rộng thêm các tín hiệu xử lý ảnh như ELA, noise analysis, metadata analysis hoặc image forensic.

Sản phẩm mục tiêu trong 3 tuần là một **app demo** có thể chạy được, cho phép người dùng upload ảnh, nhập nội dung bài viết tiếng Việt, sau đó trả về kết quả `Real`, `Fake` hoặc `Suspicious` kèm điểm tin cậy và lý do cảnh báo.

Hướng thiết kế ưu tiên:

- Dùng mô hình pretrained để tiết kiệm tài nguyên.
- Không bắt buộc train mô hình lớn.
- Dễ mở rộng về sau thành web app, API hoặc browser extension.
- Có thể demo tiếng Việt bằng cách dịch văn bản sang tiếng Anh trước khi đưa vào CLIP.

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

- Có giao diện app để demo.
- Có pipeline AI chạy thật.
- Có test case tiếng Việt.
- Có báo cáo rõ logic và mô hình sử dụng.

Không nên đặt mục tiêu:

- Xác minh tin thật/giả tuyệt đối.
- Crawl tự động mọi bài đăng trên Facebook/TikTok.
- Train mô hình deep learning lớn từ đầu.
- Làm extension hoàn chỉnh nếu chưa có app ổn định.

---

# 2. Features

## 2.1. MVP Features

Đây là các tính năng bắt buộc để có sản phẩm demo.

### Feature 1: Upload ảnh và nhập nội dung

Người dùng có thể:

- Upload ảnh từ máy tính.
- Nhập hoặc dán nội dung bài viết tiếng Việt.
- Bấm nút phân tích.

### Feature 2: Kiểm tra độ khớp ảnh - chữ

Hệ thống tính độ tương đồng giữa hình ảnh và nội dung văn bản.

Ý tưởng:

- Ảnh được đưa vào image encoder.
- Text tiếng Việt được dịch sang tiếng Anh hoặc tiền xử lý phù hợp.
- Text được đưa vào text encoder.
- Tính cosine similarity giữa image embedding và text embedding.

Kết quả:

- Similarity cao: ảnh và chữ có khả năng liên quan.
- Similarity thấp: có nguy cơ sai ngữ cảnh hoặc gắn ảnh không liên quan.

### Feature 3: Phân tích dấu hiệu văn bản đáng ngờ

Hệ thống tính điểm nghi ngờ dựa trên các dấu hiệu ngôn ngữ:

- Từ khóa giật tít: `sốc`, `khẩn cấp`, `chia sẻ ngay`, `sự thật bị che giấu`.
- Dấu chấm than quá nhiều.
- Cách viết hoa bất thường.
- Nội dung quá ngắn nhưng mang tính khẳng định mạnh.

Đây là module rule-based, dễ làm và dễ giải thích trong báo cáo.

### Feature 4: Kết luận tổng hợp

Hệ thống tổng hợp các điểm thành phần để đưa ra kết quả:

- `Real`: ảnh và chữ tương đối khớp, text không có dấu hiệu đáng ngờ.
- `Suspicious`: có một số dấu hiệu bất thường nhưng chưa đủ mạnh để kết luận fake.
- `Fake`: nhiều dấu hiệu bất thường xuất hiện đồng thời.

### Feature 5: Giải thích kết quả

Hệ thống không chỉ hiện nhãn, mà cần hiện lý do:

- Ảnh và chữ có độ tương đồng thấp.
- Nội dung có từ ngữ giật tít.
- Ảnh có dấu hiệu chỉnh sửa.
- Hệ thống không đủ chắc chắn.

## 2.2. Optional Features

Đây là các tính năng mở rộng nếu còn thời gian.

### Feature 6: ELA - Error Level Analysis

ELA giúp quan sát sự khác biệt về mức nén JPEG trong ảnh. Ảnh bị cắt ghép có thể có vùng sai khác mức lỗi nén so với phần còn lại.

Lưu ý:

- ELA không phải bằng chứng tuyệt đối.
- Ảnh trên mạng xã hội thường bị nén nhiều lần, nên ELA có thể nhiễu nhiều.
- Nên dùng ELA như một điểm phụ trợ, không phải kết luận chính.

### Feature 7: FastAPI Backend

Tách logic AI thành API:

```text
POST /predict
Input: image + text
Output: result + confidence + reasons
```

Mục đích:

- Để mở rộng thành web frontend.
- Để browser extension gọi API.
- Để chia tách frontend/backend rõ ràng.

### Feature 8: Browser Extension Prototype

Nếu app đã ổn định, có thể làm extension prototype:

- Popup extension có ô nhập text và upload ảnh.
- Gọi API backend.
- Hiện kết quả trong popup.

Extension chỉ nên làm sau khi pipeline AI và app demo đã chạy ổn.

---

