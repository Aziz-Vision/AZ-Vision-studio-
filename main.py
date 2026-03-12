import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageEnhance, ImageOps
import requests
import io
import numpy as np
import cv2

# Page Setup
st.set_page_config(page_title="Aziz Pro Ultra-Res", layout="centered")
st.title("🛡️ Aziz Pro: Deep Image Restoration")

# Get Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Upload image for Ultra-Enhancement...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 1. Load Image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Original Image', use_column_width=True)
    
    if st.button('🚀 Execute Deep Enhancement'):
        with st.spinner('Applying Deep Sharpening & AI Analysis...'):
            
            # 2. Manual Enhancement (The "Pro" Step)
            # Enhance Contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2) # Increase contrast by 20%
            
            # Deep Sharpening using OpenCV
            img_np = np.array(image)
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) # Sharpening Filter
            img_np = cv2.filter2D(img_np, -1, kernel)
            enhanced_image = Image.fromarray(img_np)
            
            # 3. AI Analysis Report
            prompt = (
                "Act as a forensic photo analyst. Identify every single detail, "
                "text, and object in this image. Describe them in clear Arabic "
                "so I can understand what was hidden in the blur."
            )
            response = model.generate_content([prompt, enhanced_image])
            
            # 4. Save and Send
            img_byte_arr = io.BytesIO()
            enhanced_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            files = {'photo': img_byte_arr}
            caption_text = f"🔥 Ultra-Enhanced Result for Aziz!\n\n🔍 Report:\n{response.text}"
            
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto", 
                    data={'chat_id': CHAT_ID, 'caption': caption_text[:1000]}, 
                    files=files
                )
                st.success("The 'Cinematic' version is now on your Telegram!")
                st.image(enhanced_image, caption='Enhanced Version (Preview)', use_column_width=True)
                st.write("### AI Deep Dive Report:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Telegram Error: {e}")