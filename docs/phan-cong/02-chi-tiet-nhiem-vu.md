# 5. Phân chia công việc cho 6 thành viên

## Thành viên 1 - Data Lead

### Mục tiêu

Chuẩn bị dữ liệu demo để cả nhóm test app và đưa vào báo cáo.

### Việc cần làm

- Tạo thư mục `data/demo_cases/images/`.
- Thu thập 30-50 case demo.
- Mỗi case gồm: ảnh, text, label, loại case, ghi chú.
- Ưu tiên demo tiếng Việt.
- Tạo file `demo_cases.csv`.

### Loại case cần có

- Ảnh và text khớp nhau.
- Ảnh thật nhưng text sai ngữ cảnh.
- Ảnh không liên quan text.
- Text giật tít/cảm xúc mạnh.
- Ảnh nghi bị chỉnh sửa nếu có.

### Output bàn giao

```text
data/demo_cases/demo_cases.csv
data/demo_cases/images/
```

### Checklist

- [ ] Có ít nhất 30 case.
- [ ] Mỗi ảnh đều mở được.
- [ ] Mỗi case có label `real`, `fake` hoặc `suspicious`.
- [ ] Có ít nhất 10 case tiếng Việt để demo.
- [ ] Có bảng ghi chú giải thích vì sao label như vậy.

---

## Thành viên 2 - Image Pipeline

### Mục tiêu

Xây dựng module xử lý ảnh đầu vào.

### Việc cần làm

- Đọc file ảnh.
- Kiểm tra định dạng ảnh.
- Chuyển ảnh về RGB.
- Resize nếu cần.
- Viết hàm preprocess cho CLIP.
- Optional: viết ELA.

### File phụ trách

```text
src/image/preprocess.py
src/image/ela.py
tests/test_image_pipeline.py
```

### Hàm cần có

```python
def load_image(image_path):
    pass

def preprocess_image(image):
    pass

def analyze_image(image_path):
    return {
        "image_path": image_path,
        "image_valid": True,
        "image_size": [0, 0],
        "ela_score": 0.0,
        "ela_image_path": None,
        "image_reasons": []
    }
```

### Output bàn giao

- Hàm `analyze_image(image_path)`.
- Test cơ bản với `.jpg`, `.png`.
- Nếu làm ELA: ảnh ELA visualization và `ela_score`.

### Checklist

- [ ] Đọc được JPG/PNG.
- [ ] Báo lỗi rõ nếu ảnh không hợp lệ.
- [ ] Output đúng format chung.
- [ ] Có test với ít nhất 3 ảnh mẫu.
- [ ] Optional: có ELA score.

---

## Thành viên 3 - Text Pipeline

### Mục tiêu

Xử lý text tiếng Việt và tính điểm nghi ngờ của nội dung.

### Việc cần làm

- Clean text.
- Xử lý text rỗng/quá ngắn/quá dài.
- Dịch text sang tiếng Anh nếu dùng CLIP English.
- Tính suspicious score dựa trên keyword/rule.
- Trả về lý do cảnh báo text.

### File phụ trách

```text
src/text/preprocess.py
src/text/translate.py
src/text/suspicious_score.py
tests/test_text_pipeline.py
```

### Hàm cần có

```python
def clean_text(text):
    pass

def translate_to_english(text):
    pass

def calculate_suspicious_score(text):
    return {
        "suspicious_score": 0.0,
        "suspicious_reasons": []
    }

def analyze_text(text):
    return {
        "original_text": text,
        "clean_text": "",
        "translated_text": "",
        "suspicious_score": 0.0,
        "suspicious_reasons": []
    }
```

### Keyword gợi ý

```text
sốc
khẩn cấp
chia sẻ ngay
sự thật bị che giấu
không ai nói cho bạn
100% sự thật
cảnh báo
lan truyền
đừng bỏ qua
```

### Checklist

- [ ] Text tiếng Việt có dấu không lỗi encoding.
- [ ] Text rỗng được báo lỗi rõ.
- [ ] Tính được suspicious score từ 0 đến 1.
- [ ] Trả về reasons để app hiển thị.
- [ ] Output đúng format chung.

---

## Thành viên 4 - CLIP Similarity

### Mục tiêu

Tính độ tương đồng giữa hình ảnh và text.

### Việc cần làm

- Load CLIP pretrained.
- Lấy image embedding.
- Lấy text embedding.
- Tính cosine similarity.
- Viết hàm để predictor gọi trực tiếp.

### File phụ trách

```text
src/models/clip_model.py
notebooks/01_clip_similarity_demo.ipynb
```

### Hàm cần có

```python
def load_clip_model():
    pass

def compute_clip_similarity(image, text):
    return {
        "similarity_score": 0.0,
        "image_embedding_shape": [512],
        "text_embedding_shape": [512]
    }
```

### Checklist

- [ ] Load được CLIP.
- [ ] Chạy được với 1 ảnh + 1 text English.
- [ ] Chạy được với text tiếng Việt đã dịch.
- [ ] Similarity score nằm trong khoảng hợp lý.
- [ ] Có notebook demo ngắn.

---

## Thành viên 5 - App Demo

### Mục tiêu

Xây dựng giao diện để người dùng upload ảnh, nhập text và xem kết quả.

### Việc cần làm

- Tạo app Streamlit.
- Upload ảnh.
- Nhập text.
- Nút Analyze.
- Hiện kết quả Real/Fake/Suspicious.
- Hiện confidence, scores, reasons.
- Optional: hiện ảnh ELA.

### File phụ trách

```text
app/streamlit_app.py
README.md
```

### Giao diện tối thiểu

```text
Title: Anti Fake News Detection

[Upload image]
[Text area]
[Analyze button]

Result:
- Label
- Confidence
- Reasons
- Scores
```

### Checklist

- [ ] App mở được bằng `streamlit run app/streamlit_app.py`.
- [ ] Upload ảnh được.
- [ ] Nhập text được.
- [ ] Hiện kết quả predictor.
- [ ] UI dễ demo trước lớp.

---

## Thành viên 6 - Integration, Testing, Report

### Mục tiêu

Ghép tất cả module thành pipeline hoàn chỉnh và chuẩn bị báo cáo.

### Việc cần làm

- Viết `predictor.py`.
- Tổng hợp image/text/CLIP/scoring.
- Viết final scoring logic.
- Viết explanation generator.
- Viết test pipeline.
- Viết README hướng dẫn chạy.
- Hỗ trợ slide/report.

### File phụ trách

```text
src/inference/predictor.py
src/inference/explanation.py
tests/test_predictor.py
README.md
docs/report_outline.md
```

### Hàm cần có

```python
def predict_fake_news(image_path, text):
    return {
        "result": "Suspicious",
        "confidence": 78,
        "scores": {
            "similarity": 0.0,
            "text_suspicious": 0.0,
            "image_manipulation": 0.0,
            "fake_score": 0.0
        },
        "reasons": []
    }
```

### Checklist

- [ ] Gọi được image module.
- [ ] Gọi được text module.
- [ ] Gọi được CLIP module.
- [ ] Tính được fake score.
- [ ] Trả output đúng format cho app.
- [ ] Có test end-to-end với 5 case.

---

# 6. Ma trận phụ thuộc giữa các thành viên

| Thành viên | Phụ thuộc vào | Cần bàn giao cho |
|---|---|---|
| TV1 Data | Không phụ thuộc | TV2, TV3, TV4, TV6 |
| TV2 Image | Ảnh demo từ TV1 | TV4, TV6 |
| TV3 Text | Text demo từ TV1 | TV4, TV6 |
| TV4 CLIP | TV2 image, TV3 translated text | TV6 |
| TV5 App | Output predictor từ TV6 | Người dùng demo |
| TV6 Integration | TV2, TV3, TV4 | TV5, report |

Để làm song song trong tuần 1:

- TV1 tạo trước 5 demo case mẫu.
- TV2 làm image pipeline bằng ảnh bất kỳ.
- TV3 làm text pipeline bằng text mẫu.
- TV4 test CLIP bằng ảnh/text mẫu.
- TV5 tạo UI fake data trước, chưa cần predictor thật.
- TV6 viết predictor với mock output trước, sau đó thay bằng module thật.

---

