import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. Page Config
st.set_page_config(page_title="Aziz18 AI", layout="centered")
st.markdown("<style>.stApp {background-color: white !important;}</style>", unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")

# 2. Model Setup
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

# 3. Uploader
up = st.file_uploader("Upload your image", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    
    with st.spinner("Processing & Sending to Telegram..."):
        try:
            # AI Analysis
            response = model.generate_content(["Analyze this image in detail", image])
            
            # Telegram Process
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': img_byte_arr.getvalue()},
                data={
                    'chat_id': st.secrets['CHAT_ID'], 
                    'caption': f"🎯 Aziz18 Report:\n\n{response.text[:900]}"
                }
            )
            
            st.balloons()
            st.success("Success! Check your Telegram.")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# 4. Signature
st.markdown(
    '<div style="background:#0f172a; color:white; padding:20px; border-radius:10px; text-align:center; font-size:25px; font-weight:bold; margin-top:50px;">'
    'BY: Aziz18'
    '</div>', 
    unsafe_allow_html=True
)