import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# Aziz18 Pro Config
st.set_page_config(page_title="Aziz18 Vision", layout="centered")

# Configure API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Secrets!")

# Force Use Stable Model
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🚀 AZIZ ULTRA-MAX AI")

up = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    
    if st.button("Analyze & Send"):
        with st.spinner("Processing..."):
            try:
                # Direct Analysis
                response = model.generate_content(["Describe this image briefly", image])
                
                # Telegram Send
                buf = io.BytesIO()
                image.save(buf, format='JPEG')
                
                requests.post(
                    f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                    files={'photo': buf.getvalue()},
                    data={
                        'chat_id': st.secrets['CHAT_ID'], 
                        'caption': f"🎯 Aziz18 Report:\n\n{response.text[:800]}"
                    }
                )
                
                st.balloons()
                st.success("✅ Success! Check Telegram.")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error Details: {str(e)}")

st.markdown("---")
st.markdown("<h3 style='text-align: center;'>BY: Aziz18</h3>", unsafe_allow_html=True)