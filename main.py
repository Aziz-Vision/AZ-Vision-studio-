import streamlit as st
import os
import subprocess
import sys

# --- هذي هي الشاشة اللي تحبها يا عزيز ---
def initial_setup():
    # قائمة المكتبات اللي تسبب ثقل
    packages = [
        "numpy==1.24.3",
        "torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu",
        "torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu",
        "facexlib",
        "basicsr==1.4.2",
        "git+https://github.com/sczhou/CodeFormer.git"
    ]
    
    container = st.empty()
    with container.container():
        st.info("🔄 جاري تهيئة المحرك لأول مرة... يرجى الانتظار دقيقة.")
        progress_bar = st.progress(0)
        for i, pkg in enumerate(packages):
            subprocess.run(f"{sys.executable} -m pip install {pkg}", shell=True, capture_output=True)
            progress_bar.progress((i + 1) / len(packages))
    container.empty()

# محاولة التشغيل
try:
    import torch
    from codeformer.archs.codeformer_arch import CodeFormer
except ImportError:
    initial_setup()
    st.rerun()

import cv2
import numpy as np
from PIL import Image
from torchvision.transforms.functional import normalize
from basicsr.utils import img2tensor, tensor2img
from facelib.utils.face_restoration_helper import FaceRestoreHelper
import telebot
import tempfile

st.set_page_config(page_title="Aziz Ultra Restoration", page_icon="🌟")
st.title("🌟 Aziz Ultra Restoration")

# جلب السكرت من الخزنة
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
bot = telebot.TeleBot(TOKEN)

@st.cache_resource
def load_model():
    device = torch.device('cpu')
    model = CodeFormer(dim_embd=512, codebook_size=1024, latency_unit=2, nb_blocks=2, oversampling_2x=True, disable_perceptual_loss=True).to(device)
    if os.path.exists('weights/codeformer.pth'):
        model.load_state_dict(torch.load('weights/codeformer.pth', map_location='cpu')['params_ema'])
    model.eval()
    return model, device

# --- كود الترميم اللي طلع عيون الطفلة ---
def process_aziz(image, model, device):
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

uploaded_file = st.file_uploader("ارفع صورتك يا بطل...", type=["jpg", "png", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="الأصل")
    if st.button("بدء الترميم ⚡"):
        with st.spinner("لحظات والنتيجة عندك..."):
            model, device = load_model()
            res = process_aziz(img, model, device)
            st.image(res, caption="النتيجة النهائية ✨")
            # إرسال للتليجرام
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                res.save(tmp.name)
                with open(tmp.name, "rb") as f: bot.send_photo(CHAT_ID, f, caption="✅ تم بنجاح")
