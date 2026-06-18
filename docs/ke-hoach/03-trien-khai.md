# 5. Implement

## 5.1. Cấu trúc thư mục đề xuất

Có thể áp dụng cho repo `linh0526/nhom1-xulianh-thigiacmaytinh`.

```text
nhom1-xulianh-thigiacmaytinh/
│
├── app/
│   ├── streamlit_app.py
│   └── components/
│       └── result_card.py
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── image/
│   │   ├── __init__.py
│   │   ├── preprocess.py
│   │   ├── clip_image.py
│   │   └── ela.py
│   │
│   ├── text/
│   │   ├── __init__.py
│   │   ├── preprocess.py
│   │   ├── translate.py
│   │   └── suspicious_score.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── clip_model.py
│   │   └── fusion_model.py
│   │
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── predictor.py
│   │   └── explanation.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── demo_cases/
│       └── demo_cases.csv
│
├── notebooks/
│   ├── 01_clip_similarity_demo.ipynb
│   └── 02_evaluation.ipynb
│
├── tests/
│   ├── test_image_pipeline.py
│   ├── test_text_pipeline.py
│   └── test_predictor.py
│
├── docs/
│   ├── project_plan.md
│   ├── system_design.md
│   └── report_outline.md
│
├── requirements.txt
├── README.md
└── run_app.py
```

## 5.2. File/module chính

### `src/image/preprocess.py`

Nhiệm vụ:

- Đọc ảnh.
- Chuyển về RGB.
- Resize.
- Chuẩn hóa input cho CLIP.

### `src/image/ela.py`

Nhiệm vụ:

- Tạo ảnh ELA.
- Tính điểm bất thường đơn giản.
- Lưu ảnh ELA để hiển thị trong app nếu cần.

### `src/text/preprocess.py`

Nhiệm vụ:

- Xóa khoảng trắng thừa.
- Chuẩn hóa dấu câu.
- Giới hạn độ dài text.

### `src/text/translate.py`

Nhiệm vụ:

- Dịch text tiếng Việt sang tiếng Anh.
- Trong MVP có thể dùng thư viện dịch miễn phí hoặc nhập text đã dịch thủ công cho demo nếu bị lỗi mạng.

### `src/text/suspicious_score.py`

Nhiệm vụ:

- Tính điểm giật tít.
- Đếm từ khóa đáng ngờ.
- Đếm dấu chấm than, viết hoa bất thường.

### `src/models/clip_model.py`

Nhiệm vụ:

- Load CLIP pretrained.
- Extract image embedding.
- Extract text embedding.
- Tính cosine similarity.

### `src/inference/predictor.py`

Nhiệm vụ:

- Gọi các module image/text/model.
- Tính final score.
- Trả về kết quả chung.

Output mẫu:

```python
{
    "result": "Suspicious",
    "confidence": 78,
    "scores": {
        "similarity": 0.21,
        "text_suspicious": 0.65,
        "image_manipulation": 0.10
    },
    "reasons": [
        "Nội dung văn bản và hình ảnh có độ tương đồng thấp.",
        "Văn bản có dấu hiệu giật tít hoặc cảm xúc mạnh."
    ]
}
```

## 5.3. Phân chia công việc cho 6 thành viên

### Thành viên 1: Dataset và demo cases

Công việc:

- Tìm 30-50 mẫu demo tiếng Việt.
- Mỗi mẫu gồm ảnh, text, label dự kiến.
- Tạo file `data/demo_cases/demo_cases.csv`.
- Chia case thành các nhóm:
  - Ảnh đúng + text đúng.
  - Ảnh không liên quan + text sai ngữ cảnh.
  - Text giật tít.
  - Ảnh nghi bị chỉnh sửa.

Deliverable:

- `demo_cases.csv`
- Thư mục ảnh demo.
- Bảng mô tả từng case.

### Thành viên 2: Image pipeline

Công việc:

- Viết module đọc và tiền xử lý ảnh.
- Tích hợp CLIP image encoder.
- Optional: viết ELA.

Deliverable:

- `src/image/preprocess.py`
- `src/image/ela.py`
- Hàm trả về image embedding.

### Thành viên 3: Text pipeline

Công việc:

- Tiền xử lý text tiếng Việt.
- Dịch text sang tiếng Anh.
- Tính suspicious text score.

Deliverable:

- `src/text/preprocess.py`
- `src/text/translate.py`
- `src/text/suspicious_score.py`

### Thành viên 4: CLIP similarity và scoring

Công việc:

- Load CLIP.
- Tính similarity giữa ảnh và text.
- Xây dựng công thức fake_score.

Deliverable:

- `src/models/clip_model.py`
- Một notebook demo similarity.

### Thành viên 5: App demo

Công việc:

- Xây dựng giao diện Streamlit.
- Upload ảnh, nhập text.
- Hiện result, confidence, reasons, scores.
- Optional: hiện ảnh ELA.

Deliverable:

- `app/streamlit_app.py`
- `run_app.py`

### Thành viên 6: Integration, testing, report

Công việc:

- Gom các module thành pipeline chạy được.
- Viết test cơ bản.
- Viết README.
- Làm slide và báo cáo.

Deliverable:

- `src/inference/predictor.py`
- `tests/`
- `README.md`
- Báo cáo/thuyết trình.

## 5.4. Timeline 3 tuần

### Tuần 1: Chốt scope và làm pipeline riêng lẻ

Mục tiêu:

- Có dataset demo nhỏ.
- Chạy được CLIP similarity với 1 ảnh + 1 text.
- Có rule tính suspicious text score.
- Có khung app Streamlit.

Công việc:

- Ngày 1-2: chốt requirement, tạo repo structure.
- Ngày 3-4: image pipeline và text pipeline.
- Ngày 5-6: CLIP similarity.
- Ngày 7: demo nội bộ lần 1.

### Tuần 2: Tích hợp sản phẩm

Mục tiêu:

- App chạy end-to-end.
- Nhập ảnh + text -> ra kết quả.
- Có giải thích kết quả.

Công việc:

- Tích hợp predictor vào app.
- Chỉnh scoring logic.
- Thêm ELA nếu kịp.
- Tạo 10-15 demo case tốt nhất.

### Tuần 3: Test, hoàn thiện và báo cáo

Mục tiêu:

- Sản phẩm demo ổn định.
- Có report và slide.
- Có video demo nếu cần.

Công việc:

- Test với tất cả demo cases.
- Ghi lại kết quả vào bảng.
- Viết đánh giá hạn chế.
- Hoàn thiện README.
- Chuẩn bị thuyết trình.

## 5.5. Lệnh chạy dự kiến

Cài thư viện:

```bash
pip install -r requirements.txt
```

Chạy app:

```bash
streamlit run app/streamlit_app.py
```

Chạy predict bằng script:

```bash
python run_app.py --image data/demo_cases/sample.jpg --text "Nội dung bài viết tiếng Việt"
```

---

