# Phân chia công việc song song - Dự án Anti Fake News (Extension + FastAPI)

## 1. Mục tiêu của file

File này dùng để nhóm 6 người có thể làm việc song song mà không bị chờ nhau. Kiến trúc dự án tách biệt rõ giữa Frontend (Extension) và Backend (FastAPI).

Sản phẩm ưu tiên trong 3 tuần:
```text
Browser Extension + FastAPI phát hiện tin giả (ảnh + text)
```

---

# 2. Nguyên tắc làm song song

## 2.1. Phân tách Client - Server rõ ràng
Frontend chỉ lo UI và bắt sự kiện. Backend chỉ lo nhận ảnh/text và chạy model AI. Frontend không cần biết CLIP chạy thế nào, Backend không cần biết Extension chạy ra sao.

## 2.2. Chốt API Payload (Interface)
Tất cả đều phải tuân thủ format dữ liệu truyền/nhận.
- Payload Client gửi lên:
```json
{
  "image_url": "https://example.com/img.jpg",
  "text": "Bão khẩn cấp"
}
```
- Payload Server trả về:
```json
{
  "result": "Fake",
  "confidence": 85,
  "reasons": ["Giật tít", "Hình ảnh không khớp nội dung"]
}
```

---

# 3. Cấu trúc repo

```text
nhom1-xulianh-thigiacmaytinh/
├── backend/
│   ├── main.py
│   └── src/
├── extension/
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   └── popup.js
├── data/
└── docs/
```
