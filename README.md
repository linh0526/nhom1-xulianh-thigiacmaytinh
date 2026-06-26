# Anti Fake News Detection - Focus to Images

Dự án môn Thị giác máy tính và Xử lý ảnh: phát hiện nguy cơ tin giả dựa trên **hình ảnh kèm nội dung văn bản**.

MVP của dự án là một app demo cho phép người dùng upload ảnh, nhập nội dung tiếng Việt, sau đó hệ thống trả về:

- Kết quả: `Real`, `Fake` hoặc `Suspicious`
- Điểm tin cậy
- Điểm thành phần: image-text similarity, text suspicious score, image manipulation score
- Lý do cảnh báo

## Hướng tiếp cận

Phiên bản đầu tiên ưu tiên sản phẩm chạy được trong 3 tuần:

- Streamlit app để demo nhanh
- CLIP pretrained để kiểm tra độ khớp giữa ảnh và chữ
- Rule-based text suspicious score
- Optional ELA cho xử lý ảnh
- Dễ mở rộng về sau thành FastAPI hoặc browser extension

## Cấu trúc thư mục

```text
.
├── app/
│   └── streamlit_app.py
├── data/
│   └── demo_cases/
│       ├── images/
│       └── demo_cases.csv
├── docs/
│   ├── ke-hoach/
│   │   ├── 01-tong-quan.md
│   │   ├── 02-giai-phap-ky-thuat.md
│   │   ├── 03-trien-khai.md
│   │   └── 04-kiem-thu-va-mo-rong.md
│   └── phan-cong/
│       ├── 01-nguyen-tac-va-cau-truc.md
│       ├── 02-chi-tiet-nhiem-vu.md
│       └── 03-lich-trinh-va-quan-ly.md
├── notebooks/
├── src/
│   ├── image/
│   ├── inference/
│   ├── models/
│   ├── text/
│   └── utils/
├── tests/
├── requirements.txt
└── run_app.py
```

## Cài đặt

Tạo môi trường ảo:

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
.venv\Scripts\activate
```

Cài thư viện:

```bash
pip install -r requirements.txt
```

## Chạy app

```bash
streamlit run app/streamlit_app.py
```

## Chạy bằng CLI

```bash
python run_app.py --image path/to/your-image.jpg --text "Nội dung bài viết tiếng Việt"
```

## Chạy test

```bash
pytest
```

## Phân công nhanh

- TV1: dataset và demo cases
- TV2: image pipeline
- TV3: text pipeline
- TV4: CLIP similarity
- TV5: Streamlit app
- TV6: integration, testing, report

Xem chi tiết trong thư mục `docs/phan-cong/`.

## Hướng mở rộng

- Thêm ELA visualization vào app
- Thêm FastAPI backend
- Làm browser extension prototype
- Dùng PhoBERT cho text tiếng Việt
- Train MLP fusion nhỏ
- Thêm dataset lớn hơn và evaluation đầy đủ
