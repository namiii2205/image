import streamlit as st
import requests
from PIL import Image
import io
import uuid
import base64

API_URL = "https://tekup.dongnamduocgl.com/process-image"

# Khởi tạo session_id khi mở tab lần đầu
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

st.set_page_config(page_title="Image Processor", page_icon="🎨", layout="wide")
st.title("🎨 Image Processing Tool")

# Layout 2 cột
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Input")
    col3, col4 = st.columns([1, 1])
    with col3:
        uploaded_image = st.file_uploader("Upload main image:", type=["png", "jpg", "jpeg"])
    with col4:
        ref_image = st.file_uploader("Upload reference image (optional):", type=["png", "jpg", "jpeg"])
    input_text = st.text_area("Input text prompt:", "")
    no_images = st.number_input("Number of generated results (1-10):", min_value=1, max_value=10, value=1, step=1)

    if st.button("🚀 Xử lý ảnh"):
        if uploaded_image is None or not input_text.strip():
            st.error("Please upload main image and enter text prompt.")
        else:
            try:
                files = {
                    "image": uploaded_image
                }
                if ref_image:
                    files["ref_image"] = ref_image

                data = {
                    "text": input_text,
                    "session_id": st.session_state["session_id"],
                    "no_images": str(no_images)
                }

                with st.spinner("Processing ..."):
                    response = requests.post(API_URL, files=files, data=data, timeout=300)

                if response.status_code == 200:
                    resp_json = response.json()
                    if "images" in resp_json:
                        st.session_state["result_imgs"] = []
                        for idx, img_b64 in enumerate(resp_json["images"], start=1):
                            img_bytes = base64.b64decode(img_b64)
                            st.session_state["result_imgs"].append((f"result_{idx}.png", img_bytes))
                        st.success(f"Success! (Session: {st.session_state['session_id']}) Xem kết quả bên phải 👉")
                    else:
                        pass
                else:
                    st.error(f"Lỗi: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Lỗi khi gọi API: {e}")

with col2:
    st.header("📤 Output")
    if "result_imgs" in st.session_state:
        for file_name, img_bytes in st.session_state["result_imgs"]:
            img = Image.open(io.BytesIO(img_bytes))
            st.image(img, caption=file_name, use_column_width=True)
            st.download_button(
                label=f"💾 Download {file_name}",
                data=img_bytes,
                file_name=file_name,
                mime="image/png"
            )
    else:
        st.info("Chưa có ảnh kết quả. Vui lòng xử lý ảnh ở cột bên trái.")
