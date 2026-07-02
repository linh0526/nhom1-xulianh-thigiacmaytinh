import streamlit as st
from PIL import Image
import os
import sys
import time

# Tự động cấu hình sys.path để nhận diện thư mục src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import hàm predictor trung tâm
from src.inference.predictor import predict_fake_news

# ==========================================
# 1. CẤU HÌNH TRANG WEB CHUYÊN NGHIỆP
# ==========================================
st.set_page_config(
    page_title="VN Fake-Check | AI Đa phương thức",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pop-up thông báo mượt mà khi vừa mở app
if 'welcome_popup_shown' not in st.session_state:
    st.toast('👋 Chào mừng đến với Hệ thống VN Fake-Check!')
    time.sleep(0.5)
    st.toast('🕵️ Động cơ AI đã sẵn sàng hoạt động.')
    st.session_state.welcome_popup_shown = True

# ==========================================
# 2. CSS HIỆN ĐẠI TƯƠNG THÍCH DARK/LIGHT MODE
# ==========================================
st.markdown("""
    <style>
    /* Hiệu ứng chữ Gradient cho Tiêu đề chính */
    .gradient-text {
        font-size: 42px;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #0072ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle { 
        font-size: 18px; 
        color: gray; 
        text-align: center; 
        margin-bottom: 30px; 
        font-weight: 500;
    }
    
    /* Thiết kế nút bấm nổi bật */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 4px 12px rgba(0, 114, 255, 0.3) !important;
    }
    
    /* Bo góc các thành phần UI để nhìn mềm mại, hiện đại hơn */
    .stTextArea textarea, .stFileUploader {
        border-radius: 12px !important;
    }
    
    /* Làm đẹp các thẻ Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        font-size: 16px; 
        font-weight: bold; 
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR (THANH BÊN) GỌN GÀNG
# ==========================================
with st.sidebar:
    st.markdown("## 🛡️ VN Fake-Check")
    st.caption("Phiên bản v1.0.0 (Bản thử nghiệm)")
    st.markdown("---")
    
    st.markdown("### ⚙️ Engine AI Cốt lõi")
    st.markdown("- **Thị giác:** `CLIP Large`")
    st.markdown("- **Giám định:** `Thuật toán ELA`")
    st.markdown("- **Fact-Check:** `Gemini 2.5 Flash`")
    
    st.markdown("---")
    st.info("Hệ thống tự động phát hiện tin giả đa phương thức, kiểm chứng chéo hình ảnh và văn bản theo thời gian thực.")

# ==========================================
# 4. HEADER & TABS CHÍNH
# ==========================================
st.markdown('<div class="gradient-text">HỆ THỐNG PHÁT HIỆN TIN GIẢ</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Phân tích đa tầng Hình ảnh, Ngữ cảnh và Truy vết Internet</div>', unsafe_allow_html=True)

tab_home, tab_scanner = st.tabs(["🏠 TRANG CHỦ & KIẾN TRÚC", "🚀 TRUNG TÂM PHÂN TÍCH"])

# ==========================================
# TAB 1: TRANG CHỦ
# ==========================================
with tab_home:
    st.markdown("### 🌟 Tổng quan về hệ thống")
    st.write("Hệ thống của chúng tôi tự động hóa quy trình kiểm chứng thông tin bằng cách kết hợp sức mạnh của 3 lớp AI tiên tiến nhất hiện nay.")
    
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.info("#### 1️⃣ Nhận diện Lệch pha")
        st.write("Dùng AI để phát hiện các bài viết 'Treo đầu dê, bán thịt chó' (Hình ảnh và chữ viết không liên quan đến nhau).")
    with col_f2:
        st.warning("#### 2️⃣ Soi lỗi Cắt ghép")
        st.write("Dùng thuật toán ELA quét ma trận điểm ảnh để phát hiện vết Photoshop che giấu vật thể mà mắt thường không thấy.")
    with col_f3:
        st.success("#### 3️⃣ Xác minh Sự thật")
        st.write("Tự động lên mạng tìm kiếm các bài báo chính thống và dùng AI Gemini phân tích xem sự kiện đó có thật hay không.")

# ==========================================
# TAB 2: TRUNG TÂM PHÂN TÍCH CHÍNH
# ==========================================
with tab_scanner:
    col_input, col_result = st.columns([1, 1.2], gap="large")

    # --- KHU VỰC NHẬP LIỆU ---
    with col_input:
        st.markdown("### 📥 Dữ liệu đầu vào")
        text_input = st.text_area(
            "📝 Nội dung văn bản / Tiêu đề:", 
            placeholder="Dán đoạn văn bản hoặc status nghi vấn vào đây...", 
            height=140
        )
        uploaded_file = st.file_uploader("🖼️ Tải lên hình ảnh đi kèm:", type=["jpg", "jpeg", "png"])
        
        temp_image_path = None
        if uploaded_file:
            image = Image.open(uploaded_file)
            # Hiển thị ảnh bo góc
            st.image(image, caption="Hình ảnh gốc", use_container_width=True)
            
            temp_dir = "data/temp"
            os.makedirs(temp_dir, exist_ok=True)
            temp_image_path = os.path.join(temp_dir, uploaded_file.name)
            image.save(temp_image_path)

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.button("🚀 TIẾN HÀNH KIỂM TRA BÀI VIẾT", use_container_width=True, type="primary")

    # --- KHU VỰC HIỂN THỊ KẾT QUẢ ---
    with col_result:
        st.markdown("### 📊 Kết quả phân tích từ AI")
        
        if submit_btn:
            if not text_input or not uploaded_file:
                st.error("⚠️ Vui lòng nhập cả nội dung chữ và tải hình ảnh lên trước khi phân tích.")
            else:
                with st.spinner("🕵️ Hệ thống đang xử lý ELA, CLIP và tra cứu Fact-Check..."):
                    try:
                        res = predict_fake_news(temp_image_path, text_input)
                        
                        verdict = res["result"]
                        confidence = res["confidence"]
                        scores = res["scores"]
                        fc_status = res.get("fact_check_status", "Unknown")
                        reasons = res["reasons"]
                        
                        # 1. BANNER KẾT LUẬN
                        if verdict == "Real":
                            st.success(f"### 🎉 TIN THẬT (Độ tin cậy: {confidence}%)")
                        elif verdict == "Suspicious":
                            st.warning(f"### ⚠️ NGHI NGỜ (Độ nghi vấn: {confidence}%)")
                        else:
                            st.error(f"### 🚨 TIN GIẢ / XUYÊN TẠC (Nguy hiểm: {confidence}%)")
                        
                        st.markdown("---")
                        
                        # 2. THẺ CHỈ SỐ AI
                        st.markdown("#### 📈 Chỉ số đánh giá kỹ thuật")
                        m_col1, m_col2, m_col3 = st.columns(3)
                        with m_col1:
                            st.metric(label="🔗 Khớp Ảnh - Chữ", value=f"{scores['similarity']}")
                        with m_col2:
                            st.metric(label="✍️ Từ ngữ độc hại", value=f"{scores['text_suspicious']}")
                        with m_col3:
                            st.metric(label="🖼️ Lỗi Cắt ghép (ELA)", value=f"{scores['image_manipulation']}")
                        
                        st.markdown("---")
                        
                        # 3. KẾT QUẢ FACT-CHECK INTERNET
                        st.markdown("#### 🌐 Đối chiếu Báo chí (Internet Fact-Check)")
                        if fc_status == "Real":
                            st.info("✅ **XÁC NHẬN:** Báo chí chính thống có đưa tin về sự kiện này.")
                        elif fc_status == "Fake":
                            st.error("❌ **BÁC BỎ:** Các nguồn uy tín khẳng định đây là tin đồn thất thiệt.")
                        elif fc_status == "Unverified":
                            st.warning("❓ **CHƯA KIỂM CHỨNG:** Chưa có bài báo chính thống nào đưa tin về sự việc này.")
                        else:
                            st.text("⚠️ Lỗi kết nối mạng Fact-Check.")
                        
                        # 4. CHI TIẾT LÝ DO (Được giấu gọn gàng trong Expander)
                        if reasons:
                            with st.expander("📝 Xem chi tiết lý do AI đánh giá"):
                                for r in reasons:
                                    st.write(f"- {r}")
                                
                        # Dọn dẹp bộ nhớ
                        if temp_image_path and os.path.exists(temp_image_path):
                            os.remove(temp_image_path)
                            
                    except Exception as e:
                        st.error(f"❌ Lỗi hệ thống: {e}")
        else:
            st.info("💡 **Hướng dẫn:** Nhập dữ liệu ở bảng bên trái và nhấn nút xanh để khởi động AI.")