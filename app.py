import streamlit as st
import requests
from PIL import Image
import io
import uuid  # Dùng để tạo session_id ngẫu nhiên

API_URL = "https://tekup.dongnamduocgl.com/process-image"  # URL API

# Khởi tạo session_id khi mở tab lần đầu
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

st.set_page_config(page_title="Image Processor", page_icon="🎨", layout="wide")
st.title("🎨 Image Processing Tool")

# Chia layout 2 cột
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Input")
    uploaded_image = st.file_uploader("Tải ảnh lên:", type=["png", "jpg", "jpeg"])
    input_text = st.text_area("Nhập mô tả (text prompt):", "")

    if st.button("🚀 Xử lý ảnh"):
        if uploaded_image is None or not input_text.strip():
            st.error("Vui lòng tải ảnh và nhập text trước khi xử lý.")
        else:
            try:
                files = {"image": uploaded_image}
                data = {
                    "text": input_text,
                    "session_id": st.session_state["session_id"]  # Gửi session_id
                }

                with st.spinner("Đang xử lý..."):
                    response = requests.post(API_URL, files=files, data=data, timeout=300)

                if response.status_code == 200:
                    st.session_state["result_img"] = response.content
                    st.success(f"Xử lý thành công! (Session: {st.session_state['session_id']}) Xem kết quả bên phải 👉")
                else:
                    st.error(f"Lỗi: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Lỗi khi gọi API: {e}")

with col2:
    st.header("📤 Output")
    if "result_img" in st.session_state:
        result_img = Image.open(io.BytesIO(st.session_state["result_img"]))
        st.image(result_img, caption="Ảnh kết quả", use_column_width=True)
        st.download_button(
            label="💾 Tải ảnh kết quả",
            data=st.session_state["result_img"],
            file_name="result.png",
            mime="image/png"
        )
    else:
        st.info("Chưa có ảnh kết quả. Vui lòng xử lý ảnh ở cột bên trái.")
