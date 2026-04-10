import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")
st.subheader("ترميم الصور بالذكاء الاصطناعي - جودة فائقة")

# جلب بيانات التليجرام من الـ Secrets
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
bot = telebot.TeleBot(TOKEN)

# واجهة رفع الملفات
uploaded_file = st.file_uploader("اختر صورة لترميمها...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 بدء عملية التحسين العميق"):
        with st.spinner("جاري الترميم بجودة Ultra... انتظر ثواني"):
            try:
                # 1. تصغير حجم الصورة إذا كانت كبيرة جداً لتجنب رفض السيرفر
                max_size = 1500  # الحد الأقصى للعرض أو الطول
                if max(image.size) > max_size:
                    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # 2. حفظ الصورة المرفوعة مؤقتاً
                temp_path = "temp_input.png"
                image.save(temp_path)
                
                # 3. استدعاء محرك CodeFormer المجاني
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_path),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2
                )
                
                # النتيجة المسلمة هي مسار الصورة المحسنة
                restored_image_path = result
                
                # 4. عرض النتيجة في الموقع
                st.image(restored_image_path, caption="النتيجة النهائية (جودة Ultra)", use_container_width=True)
                
                # 5. إرسال الصورة الفعلية للتليجرام
                with open(restored_image_path, "rb") as f:
                    bot.send_photo(CHAT_ID, f, caption="✅ تم ترميم صورتك بجودة Ultra بنجاح!")
                
                st.success("تم إرسال الصورة إلى جوالك بنجاح! 📱")
                
                # 6. تنظيف الملفات المؤقتة
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

# تذييل الصفحة
st.markdown("---")
st.caption("Developed by Aziz | Powered by CodeFormer AI")