# 5. Phân chia công việc cho 6 thành viên

## Thành viên 1 - Data Lead
- Chuẩn bị dữ liệu demo để cả nhóm test app và đưa vào báo cáo. Tạo file `demo_cases.csv` (Có ít nhất 30 cases tiếng Việt).
- Tìm kiếm các bài post mẫu trên mạng xã hội để demo trực tiếp bằng Extension.

## Thành viên 2 - Backend Image Pipeline
- Đọc file ảnh từ URL (hoặc base64), tiền xử lý đưa về RGB và resize chuẩn bị input cho mô hình CLIP.

## Thành viên 3 - Backend Text Pipeline
- Viết Text Analyzer rule-based để chấm điểm giật tít tiếng Việt, tính toán suspicious score.
- Tích hợp dịch văn bản sang tiếng Anh.

## Thành viên 4 - Backend AI Model (CLIP)
- Load CLIP pretrained, lấy image embedding và text embedding, tính toán similarity score. Xây dựng công thức tổng hợp thành `fake_score`.

## Thành viên 5 - Browser Extension UI/UX
- Cấu hình `manifest.json`.
- Thiết kế Popup HTML/CSS đẹp mắt để hiển thị trạng thái Loading và Kết quả nhận được từ Server.

## Thành viên 6 - Integration & API
- Viết logic `background.js` và `content.js` cho Extension để bắt event phím tắt/context menu.
- Viết `backend/main.py` (FastAPI endpoints), gắn các hàm AI vào API.
- Đảm bảo Client (Extension) gọi Server (API) thành công và sửa lỗi CORS (nếu có).
