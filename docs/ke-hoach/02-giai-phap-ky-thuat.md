# 3. Tech Solutions

## 3.1. Hướng tiếp cận tổng thể

Phương pháp chính:

```text
Pretrained Model + Rule-based Scoring + Lightweight App
```

Lý do:

- Thời gian chỉ có 3 tuần.
- Nhóm chưa chắc có GPU.
- Mục tiêu ưu tiên sản phẩm demo.
- Dễ giải thích với giảng viên.
- Dễ mở rộng về sau.

## 3.2. Công nghệ đề xuất

| Thành phần | Công nghệ đề xuất | Vai trò |
|---|---|---|
| App demo | Streamlit | Tạo giao diện nhanh |
| Xử lý ảnh | PIL, OpenCV | Đọc ảnh, resize, ELA |
| AI image-text | CLIP pretrained | Tính độ khớp ảnh - chữ |
| Xử lý tiếng Việt | translate module hoặc API dịch | Đưa text tiếng Việt về tiếng Anh cho CLIP |
| Logic tổng hợp | Python rule-based scoring | Tạo kết quả Real/Fake/Suspicious |
| Optional API | FastAPI | Mở rộng thành backend |
| Optional extension | Chrome Extension Manifest V3 | Mở rộng thành extension |

## 3.3. Mô hình AI đề xuất

### CLIP

CLIP là mô hình pretrained học mối quan hệ giữa ảnh và văn bản. CLIP phù hợp với bài toán vì:

- Có image encoder và text encoder.
- Có thể tính similarity giữa ảnh và mô tả.
- Không cần train lại.
- Phù hợp cho demo image-text matching.

Hạn chế:

- CLIP phổ biến hỗ trợ tiếng Anh tốt hơn tiếng Việt.
- Cần dịch text tiếng Việt sang tiếng Anh hoặc dùng model multilingual nếu tìm được.

### PhoBERT - optional

PhoBERT phù hợp với tiếng Việt, nhưng nếu dùng PhoBERT cùng CLIP image encoder thì cần thêm fusion model để ghép đặc trưng. Trong phạm vi 3 tuần, PhoBERT nên để ở hướng mở rộng.

Hướng mở rộng:

```text
Image embedding: CLIP/ResNet
Text embedding: PhoBERT
Fusion: MLP classifier nhỏ
```

### ELA

ELA dùng xử lý ảnh truyền thống để phát hiện dấu hiệu bất thường về nén JPEG.

Công nghệ:

- PIL để lưu lại ảnh ở chất lượng JPEG thấp hơn.
- OpenCV/Numpy để tính sai khác pixel.
- Sinh ảnh ELA visualization để đưa vào báo cáo/demo.

---

# 4. Logic + AI

## 4.1. Kiến trúc pipeline MVP

```text
Input: Image + Vietnamese Text
        |
        |-- Image Preprocessing
        |      - read image
        |      - resize
        |      - normalize
        |
        |-- Text Preprocessing
        |      - clean text
        |      - translate Vietnamese to English
        |
        |-- CLIP Image Encoder
        |      -> image embedding
        |
        |-- CLIP Text Encoder
        |      -> text embedding
        |
        |-- Cosine Similarity
        |      -> image_text_similarity_score
        |
        |-- Text Suspicious Analysis
        |      -> text_suspicious_score
        |
        |-- Optional ELA Analysis
        |      -> image_manipulation_score
        |
        |-- Final Scoring
        |      -> Real / Fake / Suspicious
        |
        |-- Explanation Generator
               -> reasons
```

## 4.2. Logic tính điểm đề xuất

Hệ thống có thể dùng 3 điểm chính:

```text
similarity_score: 0 -> 1
text_suspicious_score: 0 -> 1
image_manipulation_score: 0 -> 1
```

Trong MVP, nếu chưa làm ELA thì đặt:

```text
image_manipulation_score = 0
```

Công thức điểm fake tham khảo:

```text
fake_score =
    0.55 * (1 - similarity_score)
  + 0.30 * text_suspicious_score
  + 0.15 * image_manipulation_score
```

Quy tắc phân loại:

```text
if fake_score >= 0.70:
    result = "Fake"
elif fake_score >= 0.40:
    result = "Suspicious"
else:
    result = "Real"
```

Confidence:

```text
confidence = round(max(fake_score, 1 - fake_score) * 100)
```

## 4.3. Logic sinh lý do

Ví dụ:

```text
if similarity_score < 0.25:
    add_reason("Nội dung văn bản và hình ảnh có độ tương đồng thấp.")

if text_suspicious_score > 0.50:
    add_reason("Văn bản có dấu hiệu giật tít hoặc cảm xúc mạnh.")

if image_manipulation_score > 0.60:
    add_reason("Ảnh có dấu hiệu bất thường về nén/chỉnh sửa.")

if no reason:
    add_reason("Không phát hiện dấu hiệu bất thường rõ ràng.")
```

## 4.4. Hướng mở rộng AI sau MVP

Sau khi MVP chạy ổn, có thể mở rộng:

### Hướng 1: Fusion model nhỏ

Train một MLP nhỏ:

```text
Input:
- image embedding
- text embedding
- similarity score
- text suspicious score
- ELA score

Output:
- Real/Fake
```

Ưu điểm:

- Vẫn nhẹ.
- Có train model để báo cáo thêm.
- Phù hợp Colab miễn phí.

### Hướng 2: PhoBERT cho tiếng Việt

Dùng PhoBERT để lấy text embedding tiếng Việt thay vì dịch sang tiếng Anh.

### Hướng 3: Dataset lớn hơn

Có thể thử nghiệm với:

- Image Verification Corpus.
- Weibo Dataset.
- FakeNewsNet/Politifact/Gossipcop.
- Tập demo tiếng Việt tự tạo.

---

