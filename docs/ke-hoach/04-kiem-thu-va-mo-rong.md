# 6. Test

## 6.1. Unit Test

### Test image pipeline

Cần kiểm tra:

- Đọc được ảnh `.jpg`, `.jpeg`, `.png`.
- Ảnh grayscale hoặc RGBA được chuyển về RGB.
- Ảnh sau tiền xử lý đúng kích thước input.
- Ảnh lỗi được báo lỗi rõ ràng.

### Test text pipeline

Cần kiểm tra:

- Text tiếng Việt có dấu không bị lỗi encoding.
- Text rỗng được xử lý.
- Text quá dài được cắt ngắn.
- Từ khóa giật tít được phát hiện.

### Test predictor

Cần kiểm tra:

- Input hợp lệ trả về dictionary đúng format.
- Kết quả có `result`, `confidence`, `scores`, `reasons`.
- Confidence nằm trong 0-100.

## 6.2. Scenario Test

Chuẩn bị các kịch bản demo sau:

### Scenario 1: Ảnh đúng + text đúng

Ví dụ:

- Ảnh về ngập lụt.
- Text nói về tình trạng ngập lụt.

Kỳ vọng:

- `Real` hoặc `Suspicious` với mức nghi ngờ thấp.

### Scenario 2: Ảnh không liên quan + text giật tít

Ví dụ:

- Ảnh đám đông thể thao.
- Text nói về thiên tai khẩn cấp.

Kỳ vọng:

- `Fake` hoặc `Suspicious`.
- Lý do: image-text similarity thấp.

### Scenario 3: Ảnh cũ gắn với sự kiện mới

Ví dụ:

- Ảnh lũ lụt cũ.
- Text nói rằng đó là sự kiện hôm nay.

Kỳ vọng:

- `Suspicious`.
- Lưu ý: nếu không có metadata/thời gian, hệ thống chỉ có thể cảnh báo ngữ cảnh, không xác minh ngày tháng tuyệt đối.

### Scenario 4: Text giật tít nhưng ảnh có liên quan

Kỳ vọng:

- `Suspicious`.
- Lý do: text suspicious score cao.

### Scenario 5: Ảnh có dấu hiệu chỉnh sửa rõ

Kỳ vọng:

- Nếu có ELA: thêm cảnh báo image manipulation.
- Nếu chưa có ELA: hệ thống vẫn có thể đưa kết quả dựa trên image-text và text score.

## 6.3. Evaluation

Nếu có tập demo gán nhãn, có thể tính:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.

Bảng kết quả mẫu:

| Metric | Giá trị |
|---|---:|
| Accuracy | ... |
| Precision | ... |
| Recall | ... |
| F1-score | ... |

Lưu ý khi viết báo cáo:

> Do thời gian và tài nguyên giới hạn, hệ thống trong phiên bản MVP sử dụng pretrained model và rule-based scoring. Kết quả được đánh giá trên tập demo/case study tiếng Việt nhỏ, mục tiêu chính là chứng minh pipeline multimodal fake news detection có thể hoạt động end-to-end.

---

# 7. Mở rộng sau này

## 7.1. Mở rộng thành browser extension

Khi app demo đã ổn định, có thể tách backend:

```text
Streamlit/App UI
        |
        |-- FastAPI backend
                |
                |-- predictor.py
```

Sau đó extension gọi:

```text
POST http://localhost:8000/predict
```

Extension có các thành phần:

```text
extension/
├── manifest.json
├── popup.html
├── popup.js
└── styles.css
```

## 7.2. Mở rộng model AI

Có thể bổ sung:

- PhoBERT cho text tiếng Việt.
- Fusion MLP có train.
- Dataset quốc tế như Weibo, FakeNewsNet.
- Dataset tiếng Việt tự thu thập.
- Metadata analysis nếu có EXIF.
- Reverse image search nếu có API phù hợp.

## 7.3. Mở rộng xử lý ảnh

Có thể bổ sung:

- ELA visualization.
- Noise inconsistency.
- Copy-move detection.
- Face/object inconsistency.
- AI-generated image detection.

## 7.4. Mở rộng báo cáo

Báo cáo có thể thêm:

- So sánh unimodal text-only, image-only, multimodal.
- Ablation study: bỏ CLIP similarity, bỏ text score, bỏ ELA.
- Phân tích lỗi: case nào model đoán sai và vì sao.

---

# 8. Rủi ro và cách giảm thiểu

## Rủi ro 1: CLIP không hiểu tốt tiếng Việt

Cách giảm thiểu:

- Dịch text sang tiếng Anh trước khi đưa vào CLIP.
- Ghi rõ hạn chế trong báo cáo.
- Sau này mở rộng bằng PhoBERT hoặc multilingual CLIP.

## Rủi ro 2: Không có GPU

Cách giảm thiểu:

- Dùng pretrained model.
- Chạy inference với số lượng demo nhỏ.
- Không train model lớn.
- Có thể chạy trên Colab nếu máy yếu.

## Rủi ro 3: Dataset tiếng Việt khó thu thập

Cách giảm thiểu:

- Dùng dataset quốc tế để tham khảo.
- Tự tạo case study tiếng Việt nhỏ cho demo.
- Tập trung vào pipeline và sản phẩm.

## Rủi ro 4: ELA không ổn định

Cách giảm thiểu:

- Không dùng ELA làm kết luận chính.
- Dùng ELA như tín hiệu phụ.
- Giải thích hạn chế của ELA trong report.

## Rủi ro 5: Extension tốn thời gian

Cách giảm thiểu:

- Ưu tiên Streamlit app.
- Chỉ làm extension prototype nếu app đã xong.
- Tách predictor để sau này gọi qua API.

---

# 9. Kết luận

Hướng đi đề xuất cho nhóm là xây dựng **ứng dụng phát hiện nguy cơ tin giả đa phương thức dựa trên ảnh và văn bản**, trong đó trọng tâm là:

- Kiểm tra sự phù hợp giữa hình ảnh và nội dung.
- Phân tích dấu hiệu giật tít trong text.
- Bổ sung xử lý ảnh/ELA nếu kịp.
- Tạo app demo hoàn chỉnh trong 3 tuần.

Phiên bản MVP không cần train model lớn, mà dùng pretrained CLIP và scoring logic. Cách tiếp cận này phù hợp với thời gian ngắn, tài nguyên giới hạn, và vẫn thể hiện được nội dung cốt lõi của môn Thị giác máy tính và Xử lý ảnh.
