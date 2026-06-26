# đoạn code gọi model thật từ src, xóa cmt để thêm vào
# import sys
# import os
# from pathlib import Path
# import tempfile

# import streamlit as st

# # Thêm thư mục gốc của dự án vào sys.path để import được thư mục 'src'
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.inference.predictor import predict_fake_news


# st.set_page_config(page_title="Anti Fake News Detection", page_icon="🔎", layout="centered")

# st.title("Anti Fake News Detection")
# st.caption("Phat hien nguy co tin gia dua tren hinh anh va noi dung van ban.")

# uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
# text = st.text_area("Noi dung bai viet", height=160)

# if st.button("Analyze", type="primary"):
#     if uploaded_image is None:
#         st.error("Vui long upload anh.")
#     elif not text.strip():
#         st.error("Vui long nhap noi dung bai viet.")
#     else:
#         suffix = Path(uploaded_image.name).suffix or ".jpg"
#         with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             tmp.write(uploaded_image.getbuffer())
#             image_path = tmp.name

#         with st.spinner("Dang phan tich..."):
#             result = predict_fake_news(image_path, text)

#         st.subheader(result["result"])
#         st.metric("Confidence", f"{result['confidence']}%")

#         st.write("Scores")
#         st.json(result["scores"])

#         st.write("Reasons")
#         for reason in result["reasons"]:
#             st.write(f"- {reason}")

import streamlit as st
from PIL import Image
import numpy as np
import time

st.set_page_config(
    page_title="Anti Fake News Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .real {
        background-color: #D1FAE5;
        border: 2px solid #059669;
        color: #065F46;
    }
    .fake {
        background-color: #FEE2E2;
        border: 2px solid #DC2626;
        color: #991B1B;
    }
    .suspicious {
        background-color: #FEF3C7;
        border: 2px solid #D97706;
        color: #92400E;
    }
    .metric-card {
        background-color: #F9FAFB;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        margin: 5px 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)
# hàm logic giả lập demo, nhớ xóa thêm lại đúng model đang làm
class FakeNewsPredictor:
    
    @staticmethod
    def predict(image, text):
        text_lower = text.lower()
        suspicious_keywords = ['shocking', 'amazing', 'secret', 'cure', 'miracle', 
                              'conspiracy', 'they don\'t want you to know']
        real_keywords = ['according to', 'research', 'study', 'official', 'report',
                        'university', 'published', 'confirmed by']
        
        suspicious_count = sum(1 for word in suspicious_keywords if word in text_lower)
        real_count = sum(1 for word in real_keywords if word in text_lower)
        
        base_score = 0.5
        
        if suspicious_count > real_count:
            authenticity_score = max(0.1, base_score - 0.2 * suspicious_count)
            label = "FAKE"
            confidence = min(95, 60 + suspicious_count * 10)
        elif real_count > suspicious_count:
            authenticity_score = min(0.9, base_score + 0.1 * real_count)
            label = "REAL"
            confidence = min(95, 65 + real_count * 8)
        else:
            authenticity_score = base_score
            label = "SUSPICIOUS"
            confidence = 50
        
        confidence += np.random.uniform(-5, 5)
        confidence = max(0, min(100, confidence))
        
        reasons = []
        if label == "FAKE":
            reasons.append("⚠️ Phát hiện ngôn ngữ giật gân, cường điệu")
            reasons.append("🔍 Thiếu nguồn tin đáng tin cậy")
            reasons.append("📊 Mẫu hình tin giả được nhận diện")
        elif label == "REAL":
            reasons.append("✅ Ngôn ngữ chuyên nghiệp, khách quan")
            reasons.append("📰 Trích dẫn nguồn tin có thẩm quyền")
            reasons.append("🔬 Phân tích dữ liệu nhất quán")
        else:
            reasons.append("🤔 Thông tin không đủ để kết luận")
            reasons.append("📝 Cần thêm ngữ cảnh để xác minh")
            reasons.append("🔎 Khuyến nghị kiểm tra chéo nguồn tin")
        
        scores = {
            "Authenticity Score": f"{authenticity_score:.2%}",
            "Text Analysis": f"{min(0.9, max(0.1, authenticity_score + np.random.uniform(-0.1, 0.1))):.2%}",
            "Image Analysis": f"{min(0.9, max(0.1, authenticity_score + np.random.uniform(-0.15, 0.15))):.2%}",
            "Source Reliability": f"{min(0.9, max(0.1, authenticity_score + np.random.uniform(-0.12, 0.12))):.2%}",
            "Context Coherence": f"{min(0.9, max(0.1, authenticity_score + np.random.uniform(-0.08, 0.08))):.2%}"
        }
        
        return {
            "label": label,
            "confidence": round(confidence, 1),
            "reasons": reasons,
            "scores": scores
        }

def generate_ela_image(image):
    img_array = np.array(image.convert('RGB'))
    
    ela_array = np.abs(np.diff(img_array, axis=0))
    ela_array = np.pad(ela_array, ((0, 1), (0, 0), (0, 0)), mode='constant')
    
    ela_array = ela_array * 10
    ela_array = np.clip(ela_array, 0, 255).astype(np.uint8)
    
    return Image.fromarray(ela_array)

def display_result(result):
    st.markdown("---")
    st.markdown("## 📊 Kết quả phân tích")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        label_color = {
            "REAL": "real",
            "FAKE": "fake",
            "SUSPICIOUS": "suspicious"
        }
        
        label_emoji = {
            "REAL": "✅",
            "FAKE": "🚫",
            "SUSPICIOUS": "⚠️"
        }
        
        st.markdown(f"""
        <div class="result-box {label_color.get(result['label'], '')}">
            <h2 style="margin:0;">{label_emoji.get(result['label'], '')} {result['label']}</h2>
            <p style="font-size: 1.2rem; margin: 10px 0 0 0;">
                Confidence: <strong>{result['confidence']}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"**Độ tin cậy: {result['confidence']}%**")
        st.progress(result['confidence'] / 100)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 Lý do đánh giá")
    for reason in result['reasons']:
        st.markdown(f"- {reason}")
    
    st.markdown("### 📈 Chi tiết điểm số")
    cols = st.columns(len(result['scores']))
    for idx, (metric, score) in enumerate(result['scores'].items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="metric-card">
                <small>{metric}</small><br>
                <strong style="font-size: 1.5rem;">{score}</strong>
            </div>
            """, unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-title">🔍 Anti Fake News Detection</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Hệ thống phát hiện tin giả sử dụng AI & Machine Learning</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("## ℹ️ Hướng dẫn sử dụng")
        st.markdown("""
        1. **Upload ảnh** liên quan đến tin tức
        2. **Nhập nội dung** text cần kiểm tra
        3. **Nhấn Analyze** để phân tích
        4. **Xem kết quả** đánh giá
        
        ---
        ### 📝 Lưu ý
        - Hỗ trợ định dạng: JPG, PNG, JPEG
        - Text nên có độ dài tối thiểu 50 ký tự
        - Kết quả chỉ mang tính tham khảo
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Thống kê phiên")
        if 'analysis_count' not in st.session_state:
            st.session_state.analysis_count = 0
        st.metric("Số lần phân tích", st.session_state.analysis_count)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📸 Upload Ảnh")
        uploaded_file = st.file_uploader(
            "Chọn file ảnh để phân tích",
            type=['jpg', 'jpeg', 'png'],
            help="Upload ảnh liên quan đến tin tức cần kiểm tra"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Ảnh đã upload", use_column_width=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <small>📏 Kích thước: {image.size[0]}x{image.size[1]}px</small><br>
                <small>📦 Dung lượng: {len(uploaded_file.getvalue())/1024:.1f} KB</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ✍️ Nội dung Text")
        text_input = st.text_area(
            "Nhập nội dung text cần phân tích",
            height=200,
            placeholder="Ví dụ: Theo báo cáo mới nhất từ Đại học Harvard, các nhà nghiên cứu đã phát hiện ra một phương pháp đột phá...",
            help="Nhập nội dung tin tức cần kiểm tra tính xác thực"
        )
        
        if text_input:
            char_count = len(text_input)
            st.markdown(f"""
            <div class="metric-card">
                <small>📝 Số ký tự: {char_count}</small>
                {"<small style='color: #059669;'>✅ Đủ dữ liệu phân tích</small>" if char_count >= 50 else "<small style='color: #DC2626;'>⚠️ Nên nhập ít nhất 50 ký tự</small>"}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("🔬 Phân tích", use_container_width=True)
    
    if analyze_button:
        if not uploaded_file:
            st.error("❌ Vui lòng upload ảnh trước khi phân tích!")
        elif not text_input:
            st.warning("⚠️ Vui lòng nhập text để phân tích!")
        elif len(text_input) < 10:
            st.warning("⚠️ Text quá ngắn. Vui lòng nhập ít nhất 10 ký tự!")
        else:
            st.session_state.analysis_count += 1
            
            with st.spinner("🔄 Đang phân tích..."):
                time.sleep(1.5)
                
                image = Image.open(uploaded_file)
                #gọi hàm logic giả lập
                predictor = FakeNewsPredictor()
                result = predictor.predict(image, text_input)
                
                st.session_state.last_result = result
                st.session_state.last_image = image
                
                display_result(result)
                
                if st.checkbox("🔬 Hiển thị phân tích ELA (Error Level Analysis)", value=True):
                    st.markdown("### 🔍 Ảnh ELA (Error Level Analysis)")
                    st.markdown("*Phân tích mức độ chỉnh sửa ảnh dựa trên mức nén JPEG*")
                    
                    ela_col1, ela_col2 = st.columns(2)
                    with ela_col1:
                        ela_image = generate_ela_image(image)
                        st.image(ela_image, caption="Ảnh ELA", use_column_width=True)
                    
                    with ela_col2:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>📊 Giải thích ELA</h4>
                            <ul>
                                <li><strong>Vùng sáng:</strong> Có thể đã bị chỉnh sửa</li>
                                <li><strong>Vùng tối:</strong> Ảnh gốc, chưa chỉnh sửa</li>
                                <li><strong>Đồng đều:</strong> Ảnh nguyên bản</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
    
    elif 'last_result' in st.session_state:
        st.markdown("---")
        st.info("📋 Kết quả phân tích gần nhất:")
        display_result(st.session_state.last_result)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280;">
        <p>🔍 Anti Fake News Detection System | Demo Version 1.0</p>
        <p><small>⚠️ Kết quả chỉ mang tính tham khảo và phục vụ mục đích demo</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
