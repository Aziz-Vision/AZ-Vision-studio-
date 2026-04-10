import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")
st.subheader("ترميم الصور بالذكاء الاصطناعي - جودة فائقة")

# جلب توكن التليجرام من الـ Secrets
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
bot = telebot.TeleBot(TOKEN)

uploaded_file = st.file_uploader("اختر صورة لترميمها...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء عملية التحسين العميق"):
        with st.spinner("جاري الترميم بجودة Ultra... انتظر ثواني"):
            try:
                # حفظ الصورة مؤقتاً
                temp_path = "temp_image.png"
                image.save(temp_path)
                
                # استخدام محرك CodeFormer المجاني عبر Hugging Face
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_path),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2,
                    api_name="/predict"
                )
                
                # النتيجة تكون مسار لصورة
                restored_image_path = result
                
                # عرض النتيجة في الموقع
                st.image(restored_image_path, caption="النتيجة النهائية", use_container_width=True)
                
                # إرسال للتليجرام
                with open(restored_image_path, "rb") as f:
                    bot.send_photo(CHAT_ID, f, caption="✅ تم ترميم صورتك بجودة Ultra!")
                
                st.success("تم التوصيل لجوالك بنجاح! 📱")
                
                # تنظيف الملفات المؤقتة
                os.remove(temp_path)
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")