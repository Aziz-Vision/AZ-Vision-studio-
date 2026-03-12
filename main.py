import streamlit as st
import google.generativeai as genai

# 1. تصميم بسيط جداً للتأكد من اللون
st.markdown("<style>.stApp {background-color: white !important;}</style>", unsafe_allow_html=True)

st.title("🛠️ اختبار الاتصال - Aziz18")

# 2. فحص الـ Secrets مباشرة
try:
    key = st.secrets["GOOGLE_API_KEY"]
    st.success(f"✅ تم العثور على المفتاح ويبدأ بـ: {key[:5]}...")
    
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # اختبار وهمي سريع
    test_res = model.generate_content("Say Hello")
    st.write(f"🤖 رد الذكاء الاصطناعي: {test_res.text}")
    
except Exception as e:
    st.error(f"❌ العلة هنا: {e}")

st.info("إذا شفت رد 'Hello' فوق، فالمشكلة انتهت ونقدر نرجع كودنا كامل.")