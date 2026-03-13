import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. تنسيق Aziz18
st.set_page_config(page_title="Aziz18 Vision", layout="centered")
st.markdown("<style>.stApp {background-color: white !important;}</style>", unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")

# 2. الحل اللي بيكسر الـ 404
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدمنا gemini-pro-vision لأنها النسخة الأكثر استقراراً للصور حالياً
    model = genai.GenerativeModel('gemini-pro-vision')
except Exception as e:
    st.error(f"Setup Error: {e}")

up = st.file_uploader("ارفع صورتك يا عزيز", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    
    with st.spinner("⏳ جاري التحليل والإرسال للتيليجرام..."):
        try:
            # هنا التعديل الجوهري لطريقة إرسال الصورة
            response = model.generate_content(contents=["حلل هذه الصورة بالتفصيل", image])
            
            # شغل التيليجرام
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': img_byte_arr.getvalue()},
                data={
                    'chat_id': st.secrets['CHAT_ID'], 
                    'caption': f"🎯 تقرير جديد Aziz18:\n{response.text[:900]}"
                }
            )
            
            st.balloons()
            st.success("✅ أخيراً اشتغل!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"عذراً عزيز، حدث خطأ: {str(e)}")

# 3. التوقيع
st.markdown('<div style="background:#0f172a; color:white; padding:20px; border-radius:10px; text-align:center; font-size:25px; font-weight:bold;">BY: Aziz18</div>', unsafe_allow_html=True)