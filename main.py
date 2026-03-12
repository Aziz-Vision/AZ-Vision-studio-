import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageEnhance
import requests
import io
import numpy as np
import cv2

# Page Configuration
st.set_page_config(page_title="Aziz Ultra-Max 4K", layout="wide")

# Sidebar for Language & Settings
st.sidebar.title("Settings | الإعدادات")
lang = st.sidebar.selectbox("Select Language / اختر اللغة", ["English", "العربية"])

# UI Strings Mapping based on selection
if lang == "العربية":
    ui_title = "🛡️ رادار Aziz المطور: دقة 4K وإعادة بناء شاملة"
    ui_upload = "ارفع الصورة هنا للتحسين السينمائي الشامل..."
    ui_btn = "🔥 تشغيل المعالجة العميقة ومضاعفة الحجم للكل"
    ui_sharp = "قوة التوضيح العامة"
    ui_contrast = "قوة التباين العامة"
    ui_upscale = "معامل التكبير (الريزولوشن)"
    ui_success = "تم إرسال النسخة المحسنة (كاملة) والتقرير إلى تيليجرام!"
    ui_before = "الصورة الأصلية"
    ui_after = "النتيجة بعد التحسين الشامل (4K)"
    ui_report = "تحليل الذكاء الاصطناعي العميق:"
else:
    ui_title = "🛡️ Aziz Ultra-Max: Full Image 4K Reconstruction"
    ui_upload = "Upload Image for Full Cinematic Quality..."
    ui_btn = "🔥 Execute Deep Enhancement & Upscaling for All"
    ui_sharp = "General Sharpening Strength"
    ui_contrast = "General Contrast Boost"
    ui_upscale = "Upscale Factor (Resolution)"
    ui_success = "Full enhanced version and AI report sent to Telegram!"
    ui_before = "Original Image"
    ui_after = "Enhanced Full Result (4K)"
    ui_report = "AI Deep Analysis Report:"

st.title(ui_title)

# Fetch Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

# Configure AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sliders in Sidebar for manual control
st.sidebar.markdown("---")
sharp_val = st.sidebar.slider(ui_sharp, 1.0, 5.0, 2.5)
cont_val = st.sidebar.slider(ui_contrast, 1.0, 3.0, 1.5)
upscale_val = st.sidebar.radio(ui_upscale, [2, 4], index=0)

uploaded_file = st.file_uploader(ui_upload, type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 1. Load Image
    image = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(ui_before)
        st.image(image, use_container_width=True)
    
    if st.button(ui_btn):
        with st.spinner('Processing Full Image...'):
            
            # 2. General Contrast & Color Enhancement (PIL)
            enhancer = ImageEnhance.Contrast(image)
            temp_img = enhancer.enhance(cont_val)
            
            # 3. Professional Upscaling (Cubic Interpolation - NumPy/OpenCV)
            # This reconstructs pixels across the entire image
            img_np = np.array(temp_img)
            w, h = int(img_np.shape[1] * upscale_val), int(img_np.shape[0] * upscale_val)
            img_np = cv2.resize(img_np, (w, h), interpolation=cv2.INTER_CUBIC)
            
            # 4. Deep Sharpening Filter (Unsharp Masking technique)
            # Applied to all areas: Faces, Text, and Background
            gaussian = cv2.GaussianBlur(img_np, (0, 0), 3)
            img_np = cv2.addWeighted(img_np, 1.5, gaussian, -0.5, 0)
            
            # Custom Sharpening Kernel
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * (sharp_val / 2.5)
            img_np = cv2.filter2D(img_np, -1, kernel)
            
            final_image = Image.fromarray(img_np)
            
            with col2:
                st.subheader(ui_after)
                st.image(final_image, use_container_width=True)

            # 5. AI Deep Analysis Report (Analyzes the whole improved image)
            prompt = "Analyze this enhanced high-resolution image in detail. List hidden objects, text, and faces recovered from the original blur. Response should be in the language: " + lang
            response = model.generate_content([prompt, final_image])
            
            # 6. Save and Send to Telegram (PNG for zero quality loss)
            buf = io.BytesIO()
            final_image.save(buf, format='PNG', quality=100)
            
            try:
                # Prepare caption with analysis
                caption_text = f"💎 Aziz 4K Full Result!\n\n🔍 AI Analysis:\n{response.text[:1000]}"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto", 
                    data={'chat_id': CHAT_ID, 'caption': caption_text}, 
                    files={'photo': buf.getvalue()}
                )
                st.success(ui_success)
                st.write(f"### {ui_report}")
                st.write(response.text)
            except Exception as e:
                st.error(f"Telegram Error: {e}")