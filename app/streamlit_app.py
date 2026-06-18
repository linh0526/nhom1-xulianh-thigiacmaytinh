from pathlib import Path
import tempfile

import streamlit as st

from src.inference.predictor import predict_fake_news


st.set_page_config(page_title="Anti Fake News Detection", page_icon="🔎", layout="centered")

st.title("Anti Fake News Detection")
st.caption("Phat hien nguy co tin gia dua tren hinh anh va noi dung van ban.")

uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
text = st.text_area("Noi dung bai viet", height=160)

if st.button("Analyze", type="primary"):
    if uploaded_image is None:
        st.error("Vui long upload anh.")
    elif not text.strip():
        st.error("Vui long nhap noi dung bai viet.")
    else:
        suffix = Path(uploaded_image.name).suffix or ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_image.getbuffer())
            image_path = tmp.name

        with st.spinner("Dang phan tich..."):
            result = predict_fake_news(image_path, text)

        st.subheader(result["result"])
        st.metric("Confidence", f"{result['confidence']}%")

        st.write("Scores")
        st.json(result["scores"])

        st.write("Reasons")
        for reason in result["reasons"]:
            st.write(f"- {reason}")

