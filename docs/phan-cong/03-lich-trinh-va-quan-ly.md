# 7. Lịch làm việc 3 tuần

## Tuần 1 - Tách module và chạy riêng lẻ

### Mục tiêu

Mỗi người có module riêng chạy được ở mức cơ bản.

### Công việc theo ngày

| Ngày | Việc chính |
|---|---|
| Ngày 1 | Tạo repo structure, chốt output format |
| Ngày 2 | TV1 tạo 5-10 demo case đầu tiên |
| Ngày 3 | TV2 image pipeline, TV3 text pipeline |
| Ngày 4 | TV4 CLIP similarity demo |
| Ngày 5 | TV5 Streamlit UI với mock data |
| Ngày 6 | TV6 predictor mock + scoring logic |
| Ngày 7 | Họp nhóm, test ghép lần 1 |

### Kết quả cuối tuần 1

- [ ] Có 5-10 demo cases.
- [ ] Có UI demo tạm.
- [ ] Có CLIP similarity chạy riêng.
- [ ] Có text suspicious score.
- [ ] Có predictor mock.

---

## Tuần 2 - Tích hợp end-to-end

### Mục tiêu

App chạy được từ input thật đến output thật.

### Công việc

- TV1 mở rộng lên 30-50 demo cases.
- TV2 sửa image pipeline theo lỗi test.
- TV3 sửa text pipeline theo lỗi test.
- TV4 tối ưu CLIP loading để không load lại nhiều lần.
- TV5 ghép UI với predictor thật.
- TV6 ghép scoring và reasons.

### Kết quả cuối tuần 2

- [ ] App upload ảnh + nhập text + trả kết quả.
- [ ] Có lý do cảnh báo.
- [ ] Có bảng score thành phần.
- [ ] Có ít nhất 20 case test.
- [ ] Optional: có ELA.

---

## Tuần 3 - Hoàn thiện, test, báo cáo

### Mục tiêu

Sản phẩm ổn định để nộp và thuyết trình.

### Công việc

- Test toàn bộ demo cases.
- Ghi lại kết quả vào bảng.
- Chụp màn hình app.
- Viết README.
- Viết báo cáo.
- Làm slide.
- Quay video demo nếu cần.

### Kết quả cuối tuần 3

- [ ] App demo chạy ổn.
- [ ] README có hướng dẫn cài đặt và chạy.
- [ ] Có bảng evaluation.
- [ ] Có slide.
- [ ] Có phần hạn chế và hướng phát triển.

---

# 8. Checklist họp nhóm hàng ngày

Mỗi ngày mỗi thành viên trả lời 3 câu:

```text
1. Hôm qua đã làm xong gì?
2. Hôm nay sẽ làm gì?
3. Đang bị vướng ở đâu?
```

Mẫu cập nhật:

```text
Thành viên: TV3 - Text Pipeline
Done: Đã viết clean_text và suspicious_score.
Today: Làm translate_to_english.
Blocker: Thư viện dịch bị lỗi mạng, cần phương án fallback.
Need from team: Cần 10 text demo từ TV1.
```

---

# 9. Quy ước Git để tránh conflict

## 9.1. Mỗi người làm trên branch riêng

Đặt tên branch:

```text
feature/data-cases
feature/image-pipeline
feature/text-pipeline
feature/clip-similarity
feature/streamlit-app
feature/integration
```

## 9.2. Không sửa file của nhau nếu chưa báo

Ví dụ:

- TV2 chỉ sửa `src/image/`.
- TV3 chỉ sửa `src/text/`.
- TV5 chỉ sửa `app/`.
- TV6 sửa `src/inference/` và merge module.

## 9.3. Commit nhỏ và rõ nghĩa

Ví dụ:

```text
feat: add text suspicious scoring
feat: add image preprocessing pipeline
feat: integrate predictor with streamlit app
fix: handle empty text input
docs: add project setup guide
```

---

# 10. Definition of Done

## Module được xem là xong khi

- Chạy được độc lập.
- Output đúng format đã thống nhất.
- Có test hoặc demo nhỏ.
- Có ghi chú cách dùng.
- Không làm hỏng module khác.

## Sản phẩm được xem là xong khi

- App mở được.
- Upload ảnh được.
- Nhập text được.
- Bấm analyze có kết quả.
- Kết quả có label, confidence, reasons.
- Có ít nhất 20 demo cases.
- Có README hướng dẫn chạy.
- Có báo cáo giải thích pipeline.

---

# 11. Hướng mở rộng sau khi MVP xong

Nếu còn thời gian, ưu tiên theo thứ tự:

1. Thêm ELA visualization vào app.
2. Thêm FastAPI backend.
3. Làm extension prototype.
4. Thêm PhoBERT cho text tiếng Việt.
5. Train MLP fusion nhỏ.
6. Thêm dataset quốc tế và evaluation nghiêm túc hơn.

Không nên làm extension trước khi app và predictor đã ổn định.
