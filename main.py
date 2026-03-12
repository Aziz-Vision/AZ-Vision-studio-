import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageEnhance
import requests
import io
import numpy as np
import cv2
import streamlit_analytics # المكتبة المطلوبة للتحليلات

# Page Configuration
st.set_page_config(page_title="Aziz Ultra-Max 4K", layout="wide")

# Sidebar
st.sidebar.title("Settings | الإعدادات")
lang = st.sidebar.selectbox("Language / اللغة", ["English", "العربية"])

# رابط خاص لك أنت يا عزيز عشان تشوف الإحصائيات (تضيفه في المتصفح بعد رابط موقعك)
st.sidebar.info("To see stats, add '?analytics=on' to your URL")

# UI Strings
if lang == "العربية":
ui_title = "🛡️ رادار Aziz المطور: دقة 4K شاملة"
ui_upload = "ارفع الصورة هنا للتحسين..."
ui_btn = "🔥 تشغيل المعالجة العميقة"
ui_success = "تم إرسال النسخة والتقرير لتيليجرام!"
else:
ui_title = "🛡️ Aziz Ultra-Max: Full 4K Reconstruction"
ui_upload = "Upload Image for Enhancement..."
ui_btn = "🔥 Execute Deep Enhancement"
ui_success = "Enhanced version sent to Telegram!"

st.title(ui_title)

# Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Controls
sharp_val = st.sidebar.slider("Sharpening", 1.0, 5.0, 2.5)
upscale_val = st.sidebar.radio("Upscale", [2, 4], index=0)

uploaded_file = st.file_uploader(ui_upload, type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
image = Image.open(uploaded_file).convert("RGB")
col1, col2 = st.columns(2)

with col1:
st.image(image, caption="Original", use_container_width=True)

if st.button(ui_btn):
with st.spinner('Processing...'):
    # Processing Logic
    img_np = np.array(image)
    w, h = int(img_np.shape[1] * upscale_val), int(img_np.shape[0] * upscale_val)
    img_np = cv2.resize(img_np, (w, h), interpolation=cv2.INTER_CUBIC)
    
    # Sharpening
    gaussian = cv2.GaussianBlur(img_np, (0, 0), 3)
    img_np = cv2.addWeighted(img_np, 1.5, gaussian, -0.5, 0)
    
    final_image = Image.fromarray(img_np)
    
    with col2:
        st.image(final_image, caption="4K Result", use_container_width=True)

    # AI Analysis
    prompt = "Analyze details in " + lang
    response = model.generate_content([prompt, final_image])
    
    # Send to Telegram
    buf = io.BytesIO()
    final_image.save(buf, format='PNG')
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto", 
                  data={'chat_id': CHAT_ID, 'caption': f"New Process Done!\n\n{response.text[:500]}"}, 
                  files={'photo': buf.getvalue()})
    
    st.success(ui_success)

    st.write(response.text)
