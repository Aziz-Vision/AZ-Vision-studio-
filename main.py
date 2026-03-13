import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. التنسيق الفخم لـ Aziz18
st.set_page_config(page_title="Aziz18 Vision", layout="centered")
st.markdown("<style>.stApp {background-color: white !important;}</style>", unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")

# 2. الحل الجذري لخطأ 404 (تغيير طريقة النداء)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # التحديث الجديد يتطلب تحديد الإصدار بدقة لتجنب 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Setup Error: {e}")

up = st.file_uploader("ارفع صورتك يا عزيز", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    
    with st.spinner("⏳ جاري التحليل والإرسال للتيليجرام..."):
        try:
            # طلب وصف الصورة
            response = model.generate_content(["Describe this image in detail", image])
            
            # --- شغل التيليجرام ---
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            
            # إرسال الصورة مع التحليل
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': img_byte_arr.getvalue()},
                data={
                    'chat_id': st.secrets['CHAT_ID'], 
                    'caption': f"🎯 تقرير جديد من Aziz18:\n\n{response.text[:900]}"
                }
            )
            
            st.balloons()
            st.success("✅ أبشرك اشتغل ووصل التيليجرام!")
            st.write(response.text)
            
        except Exception as e:
            # هذا السطر عشان لو طلع خطأ نعرف سببه بالضبط
            st.error(f"عذراً عزيز، حدث خطأ: {str(e)}")

# 3. التوقيع النهائي
st.markdown('<div style="background:#0f172a; color:white; padding:20px; border-radius:10px; text-align:center; font-size:25px; font-weight:bold;">BY: Aziz18</div>', unsafe_allow_html=True)