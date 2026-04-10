import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")

# جلب بيانات التليجرام من الـ Secrets
TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
CHAT_ID = st.secrets.get("CHAT_ID", "")

uploaded_file = st.file_uploader("ارفع الصورة هنا للترميم...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء الترميم"):
        with st.spinner("جاري العمل..."):
            try:
                # 1. تجهيز الصورة
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
                
                # تنقية النتيجة
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # 3. عرض النتيجة
                st.image(restored_path, caption="✅ تم الترميم بجودة فائقة", use_container_width=True)
                
                # --- إضافة أيقونة الحفظ (زر التحميل) ---
                with open(restored_path, "rb") as file:
                    st.download_button(
                        label="📥 حفظ الصورة في جوالك",
                        data=file,
                        file_name="restored_image.png",
                        mime="image/png"
                    )

                # 4. محاولة الإرسال للتليجرام
                if TOKEN and CHAT_ID:
                    try:
                        bot = telebot.TeleBot(TOKEN)
                        with open(restored_path, "rb") as f:
                            bot.send_photo(CHAT_ID, f, caption="🔥 صورة جديدة جاهزة!")
                        st.toast("تم الإرسال للتليجرام بنجاح! ✅")
                    except Exception as tele_err:
                        st.warning(f"فشل الإرسال للتليجرام: {tele_err}")
                
                # تنظيف
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
            except Exception as e:
                st.error(f"حدث خطأ في المعالجة: {e}")