# 5. Implement

## 5.1. Cấu trúc thư mục đề xuất

```text
nhom1-xulianh-thigiacmaytinh/
│
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt
│   └── src/
│       ├── image/
│       │   ├── preprocess.py
│       │   └── ela.py
│       ├── text/
│       │   ├── preprocess.py
│       │   └── suspicious_score.py
│       ├── models/
│       │   └── clip_model.py
│       └── inference/
│           ├── predictor.py
│           └── explanation.py
│
├── extension/
│   ├── manifest.json           # Cấu hình Extension
│   ├── background.js           # Xử lý phím tắt và context menu
│   ├── content.js              # Lấy dữ liệu DOM (ảnh, bôi đen text)
│   ├── popup.html              # UI kết quả
│   ├── popup.js                # Xử lý gọi API và render UI
│   └── styles.css
│
├── data/                       # Dữ liệu test
├── tests/                      # Unit tests
└── docs/                       # Tài liệu dự án
```

## 5.2. File/module chính

- `backend/main.py`: Chứa các endpoint của FastAPI như `@app.post("/api/analyze")`.
- `extension/background.js`: Lắng nghe context menu click, điều phối message với content script.
- `extension/content.js`: Trích xuất URL của ảnh và đoạn chữ (`window.getSelection()`).
- `backend/src/models/clip_model.py`: Chứa logic load mô hình AI.

## 5.3. Phân chia công việc cho 6 thành viên

1. **Thành viên 1**: Chuẩn bị bộ Data Demo Cases tiếng Việt để test.
2. **Thành viên 2**: Image Pipeline (Xử lý ảnh đầu vào ở Backend).
3. **Thành viên 3**: Text Pipeline (Xử lý chuỗi, Text Analyzer Rule-based ở Backend).
4. **Thành viên 4**: CLIP Similarity Module (Viết logic AI model cho Backend).
5. **Thành viên 5**: Browser Extension Frontend (Viết manifest, HTML/CSS/JS, UI popup).
6. **Thành viên 6**: FastAPI Backend Integration & DevOps (Gom module vào `main.py`, thiết lập CORS, kết nối Backend với Extension).

## 5.4. Lệnh chạy dự kiến

**Chạy Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Cài đặt Extension:**
1. Mở Chrome, truy cập `chrome://extensions/`
2. Bật chế độ "Developer mode".
3. Chọn "Load unpacked" và trỏ vào thư mục `extension/` của dự án.
