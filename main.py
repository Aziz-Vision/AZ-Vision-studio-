import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# Aziz18 Edition
st.set_page_config(page_title="Aziz18 Vision", layout="centered")

# الحل النهائي لخطأ الـ 404 (إجبار الموديل المستقر)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدمنا gemini-1.5-flash بدون أي v1beta في الخلفية
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error: {e}")

up = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image)
    
    if st.button("Analyze & Send"):
        with st.spinner("Processing..."):
            try:
                # النداء المباشر
                response = model.generate_content(["Describe this image", image])
                
                # Telegram
                buf = io.BytesIO()
                image.save(buf, format='JPEG')
                requests.post(
                    f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                    files={'photo': buf.getvalue()},
                    data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"Aziz18:\n{response.text[:800]}"}
                )
                
                st.balloons()
                st.success("Done!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Details: {str(e)}")

st.markdown("---")
st.write("BY: Aziz18")