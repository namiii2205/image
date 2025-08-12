import streamlit as st
import requests
from PIL import Image
import io

API_URL = "http://tekup.dongnamduocgl.com/process-image"  # URL API

st.set_page_config(page_title="Image Processor", page_icon="🎨", layout="wide")
st.title("🎨 Image Processing Tool")

# Chia layout 2 cột
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Input")
    uploaded_image = st.file_uploader("Tải ảnh lên (vui lòng chỉ upload ảnh vuông):", type=["png", "jpg", "jpeg"])
    input_text = st.text_area("Nhập mô tả (text prompt):", "")

    if st.button("🚀 Xử lý ảnh"):
        if uploaded_image is None or not input_text.strip():
            st.error("Vui lòng tải ảnh và nhập text trước khi xử lý.")
        else:
            try:
                files = {"image": uploaded_image}
                data = {"text": input_text}

                with st.spinner("Đang xử lý..."):
                    response = requests.post(API_URL, files=files, data=data)

                if response.status_code == 200:
                    # Lưu ảnh kết quả vào session_state để hiển thị bên cột 2
                    st.session_state["result_img"] = response.content
                    st.success("Xử lý thành công! Xem kết quả bên phải 👉")
                else:
                    st.error(f"Lỗi: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Lỗi khi gọi API: {e}")

with col2:
    st.header("📤 Output")
    if "result_img" in st.session_state:
        result_img = Image.open(io.BytesIO(st.session_state["result_img"]))
        st.image(result_img, caption="Ảnh kết quả", use_column_width=True)
        # Nút tải ảnh
        st.download_button(
            label="💾 Tải ảnh kết quả",
            data=st.session_state["result_img"],
            file_name="result.png",
            mime="image/png"
        )
    else:
        st.info("Chưa có ảnh kết quả. Vui lòng xử lý ảnh ở cột bên trái.")
