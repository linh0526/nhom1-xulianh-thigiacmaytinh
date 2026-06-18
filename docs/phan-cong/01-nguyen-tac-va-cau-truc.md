# Phân chia công việc song song - Dự án Anti Fake News Multimodal

## 1. Mục tiêu của file

File này dùng để nhóm 6 người có thể làm việc song song mà không bị chờ nhau. Mỗi thành viên có:

- Nhiệm vụ riêng.
- File/module cần phụ trách.
- Input cần nhận từ người khác.
- Output cần bàn giao.
- Checklist hoàn thành.

Sản phẩm ưu tiên trong 3 tuần:

```text
App demo phát hiện nguy cơ tin giả dựa trên ảnh + nội dung tiếng Việt
```

Hướng làm:

```text
Streamlit App + CLIP pretrained + text suspicious score + optional ELA
```

---

# 2. Nguyên tắc làm song song

## 2.1. Chia module rõ ràng

Mỗi người chỉ cần quan tâm module của mình, miễn là output đúng format đã thống nhất.

Ví dụ:

```python
def analyze_text(text: str) -> dict:
    return {
        "clean_text": "...",
        "translated_text": "...",
        "suspicious_score": 0.65,
        "suspicious_reasons": [...]
    }
```

Người làm app không cần biết chi tiết cách tính `suspicious_score`, chỉ cần gọi hàm và hiện kết quả.

## 2.2. Chốt interface trước khi code

Tất cả module nên trả về dictionary theo format thống nhất. Làm vậy để các thành viên có thể code độc lập.

## 2.3. Làm demo case nhỏ ngay từ đầu

Không đợi dataset lớn mới bắt đầu code. Tuần đầu chỉ cần 5-10 case mẫu để test pipeline.

## 2.4. Ưu tiên chạy được trước, tối ưu sau

Thứ tự ưu tiên:

1. App chạy được end-to-end.
2. Kết quả có lý do giải thích.
3. Giao diện dễ nhìn.
4. Thêm ELA/FastAPI/extension nếu còn thời gian.

---

# 3. Cấu trúc repo để làm song song

Đề xuất cấu trúc:

```text
nhom1-xulianh-thigiacmaytinh/
│
├── app/
│   └── streamlit_app.py
│
├── src/
│   ├── image/
│   │   ├── preprocess.py
│   │   └── ela.py
│   │
│   ├── text/
│   │   ├── preprocess.py
│   │   ├── translate.py
│   │   └── suspicious_score.py
│   │
│   ├── models/
│   │   └── clip_model.py
│   │
│   ├── inference/
│   │   ├── predictor.py
│   │   └── explanation.py
│   │
│   └── utils/
│       └── file_utils.py
│
├── data/
│   └── demo_cases/
│       ├── images/
│       └── demo_cases.csv
│
├── tests/
│   ├── test_image_pipeline.py
│   ├── test_text_pipeline.py
│   └── test_predictor.py
│
├── docs/
│   ├── ke-hoach-du-an.md
│   └── phan-chia-cong-viec-song-song.md
│
├── requirements.txt
└── README.md
```

---

# 4. Format dữ liệu chung

## 4.1. File demo cases

File:

```text
data/demo_cases/demo_cases.csv
```

Cột đề xuất:

```csv
case_id,image_path,text,label,case_type,note
001,data/demo_cases/images/flood_real.jpg,"Mưa lớn gây ngập tại Hà Nội",real,matched_image_text,Ảnh và text khớp ngữ cảnh
002,data/demo_cases/images/sport_crowd.jpg,"Khẩn cấp! Bão lớn vừa tàn phá miền Trung",fake,mismatched_image_text,Ảnh không liên quan text
```

## 4.2. Output của text module

```python
{
    "original_text": "text người dùng nhập",
    "clean_text": "text đã làm sạch",
    "translated_text": "translated text if available",
    "suspicious_score": 0.0,
    "suspicious_reasons": []
}
```

## 4.3. Output của image module

```python
{
    "image_path": "path/to/image.jpg",
    "image_valid": True,
    "image_size": [640, 480],
    "ela_score": 0.0,
    "ela_image_path": None,
    "image_reasons": []
}
```

## 4.4. Output của CLIP module

```python
{
    "similarity_score": 0.42,
    "image_embedding_shape": [512],
    "text_embedding_shape": [512]
}
```

## 4.5. Output cuối của predictor

```python
{
    "result": "Suspicious",
    "confidence": 78,
    "scores": {
        "similarity": 0.21,
        "text_suspicious": 0.65,
        "image_manipulation": 0.10,
        "fake_score": 0.62
    },
    "reasons": [
        "Nội dung văn bản và hình ảnh có độ tương đồng thấp.",
        "Văn bản có dấu hiệu giật tít hoặc cảm xúc mạnh."
    ]
}
```

---

