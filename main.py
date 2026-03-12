import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests
import time

# 1. إعدادات الصفحة والجماليات (ألوان فاتحة وتصميم احترافي)
st.set_page_config(page_title="Aziz Ultra-Max AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;900&family=Tajawal:wght@400;700&display=swap');
    
    /* خلفية الموقع - رمادي فاتح فخم */
    .main {
        background-color: #f0f2f6;
    }
    
    /* نصوص الموقع */
    html, body, [class*="st-"] {
        font-family: 'Tajawal', sans-serif;
        color: #1e293b;
    }

    /* العناوين */
    .stTitle {
        color: #1e3a8a;
        text-align: center;
        font-weight: 800;
        font-size: 42px;
        margin-bottom: 5px;
    }
    
    /* التوقيع - داكن وعريض جداً */
    .sig-box {
        background-color: #0f172a;
        padding: 25px;
        border-radius: 15px;
        margin-top: 60px;
        text-align: center;
        border: 2px solid #3b82f6;
    }
    .sig-text {
        font-family: 'Cairo', sans-serif;
        font-size: 35px;
        font-weight: 900; /* عريض جداً */
        color: #ffffff;
        letter-spacing: 2px;
    }

    /* تحسين صندوق الرفع */
    .stFileUploader section {
        background-color: #ffffff;
        border: 2px dashed #3b82f6;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. اختيار اللغة (Language Selection)
lang = st.radio("Select Language / اختر اللغة", ("العربية", "English"), horizontal=True)

# نصوص الواجهة حسب اللغة
if lang == "العربية":
    title = "🚀 AZIZ ULTRA-MAX AI"
    welcome = "مرحباً بك! ارفع صورتك الآن للمعالجة التلقائية"
    upload_msg = "اختر صورة (JPG, PNG)..."
    processing_msg = "⏳ جاري التحليل العميق..."
    success_msg = "✅ تم التحليل والإرسال لتيليجرام!"
    report_title = "📊 التقرير الفني"
    prompt_text = "حلل هذه الصورة بالتفصيل واقترح تحسينات لجعلها 4K."
else:
    title = "🚀 AZIZ ULTRA-MAX AI"
    welcome = "Welcome! Upload your image for automatic processing"
    upload_msg = "Choose an image (JPG, PNG)..."
    processing_msg = "⏳ Deep analyzing..."
    success_msg = "✅ Analysis complete & Sent to Telegram!"
    report_title = "📊 Technical Report"
    prompt_text = "Analyze this image in detail and suggest 4K enhancement tips."

# 3. عرض الواجهة
st.markdown(f'<h1 class="stTitle">{title}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; font-size: 18px; color: #64748b;">{welcome}</p>', unsafe_allow_html=True)

# 4. إعداد الموديل (حل مشكلة 404)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام الموديل المستقر
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error with Secrets / خطأ في الإعدادات")

# 5. رفع الصورة والمعالجة التلقائية
uploaded_file = st.file_uploader(upload_msg, type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Selected Image", use_container_width=True)
    
    # شريط تقدم سريع للجمالية
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)

    with st.spinner(processing_msg):
        try:
            # التحليل
            response = model.generate_content([prompt_text, image])
            
            # تجهيز الصورة للإرسال
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            
            # إرسال لتيليجرام
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': img_byte_arr.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 Aziz Ultra-Max Analysis:\n\n{response.text[:1000]}"}
            )
            
            st.balloons()
            st.success(success_msg)
            
            with st.expander(report_title):
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")

# 6. التوقيع النهائي (عريض جداً، داكن، وفخم)
st.markdown(f"""
    <div class="sig-box">
        <div class="sig-text">BY: AZIZ ULTRA-MAX</div>
        <div style="color: #60a5fa; font-size: 14px; margin-top: 5px; font-weight: bold;">
            PREMIUM AI EDITION | 2026
        </div>
    </div>
    """, unsafe_allow_html=True)