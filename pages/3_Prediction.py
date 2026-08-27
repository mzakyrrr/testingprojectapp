import base64
import hashlib
import io
import os

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from openai import OpenAI

from utils.style import (
    apply_global_style,
    show_sidebar_logo,
    page_header,
    section_title,
)
from utils.inference import (
    CLASS_NAMES,
    load_model,
    predict,
    model_is_available,
)

st.set_page_config(
    page_title="Prediction | Trimatch",
    page_icon="✂️",
    layout="wide",
)

apply_global_style()


# =========================================================
# CONFIG
# =========================================================
HAIRSTYLE_RECOMMENDATIONS = {
    "ovale": {
        "styles": [
            "Crew Cut",
            "Textured Crop",
            "Side Part Taper",
            "Undercut",
            "Pompadour",
        ],
        "note": (
            "Wajah ovale cenderung fleksibel dan cocok dengan banyak hairstyle. "
            "Gaya dengan struktur yang bersih biasanya terlihat sangat seimbang."
        ),
    },
    "rectangular": {
        "styles": [
            "Layered Medium Length",
            "Textured Side Part",
            "Shoulder-Length Shaggy",
            "Classic Taper",
            "Textured Fringe",
        ],
        "note": (
            "Untuk wajah rectangular, sebaiknya hindari volume atas yang terlalu ekstrem. "
            "Pilih gaya yang membantu menjaga proporsi wajah tetap seimbang."
        ),
    },
    "round": {
        "styles": [
            "High Fade with Textured Top",
            "Pompadour",
            "Quiff",
            "Side Part",
            "Faux Hawk",
        ],
        "note": (
            "Bagian atas yang lebih tinggi dan sisi yang lebih pendek dapat membantu "
            "memberi kesan wajah lebih panjang dan tegas."
        ),
    },
    "square": {
        "styles": [
            "Textured Crop",
            "Quiff",
            "High Fade",
            "Undercut",
            "Side Part",
        ],
        "note": (
            "Tekstur pada bagian atas dan struktur sisi yang bersih cocok untuk "
            "menegaskan karakter rahang pada wajah square."
        ),
    },
}


# =========================================================
# HELPERS
# =========================================================
def get_api_key():
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    return os.getenv("OPENAI_API_KEY")


def pil_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=95)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def generate_hairstyle_collage(user_image: Image.Image, face_shape: str, styles: list[str]):
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY belum ditemukan. Tambahkan di .streamlit/secrets.toml "
            "atau environment variable."
        )

    client = OpenAI(api_key=api_key)

    style_text = ", ".join(styles[:-1]) + f", and {styles[-1]}"

    prompt = f"""
Create one premium hairstyle try-on collage based on the provided user photo.

Requirements:
- Use the provided person's face and preserve identity as closely as possible.
- Keep the same person in all panels.
- Keep the same black shirt and a clean, realistic studio-style portrait look.
- Show 5 separate panels in one single image collage.
- Each panel must show one different recommended hairstyle.
- The five hairstyles are: {style_text}.
- Add a small clean label for each panel with the hairstyle name.
- Make the result realistic, neat, professional, and suitable for a barber recommendation app.
- Keep the person male and natural-looking.
- Prefer head-and-shoulders framing so the hairstyle is clearly visible.
- The predicted face shape is {face_shape}.
- Use a polished premium barbershop aesthetic with a dark elegant tone.
"""

    base64_image = pil_to_base64(user_image)

    response = client.responses.create(
        model="gpt-5.6",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        tools=[{"type": "image_generation"}],
    )

    image_generation_calls = [
        output for output in response.output
        if output.type == "image_generation_call"
    ]

    if not image_generation_calls:
        raise RuntimeError("Gagal menghasilkan gambar AI hairstyle.")

    image_data = image_generation_calls[0].result
    image_bytes = base64.b64decode(image_data)
    return image_bytes


def render_probability_bars(probabilities: np.ndarray):
    labels = [c.title() for c in CLASS_NAMES]
    pairs = list(zip(labels, probabilities.tolist()))
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    rows = []

    for label, prob in pairs:
        width = max(prob * 100, 4)

        rows.append(
            f"""
            <div class="prob-row">
                <div class="prob-top">
                    <span class="prob-label">{label}</span>
                    <span class="prob-value">{prob:.1%}</span>
                </div>

                <div class="prob-track">
                    <div
                        class="prob-fill"
                        style="width:{width:.2f}%;">
                    </div>
                </div>
            </div>
            """
        )

    html = f"""
    <div class="probability-wrap">
        {''.join(rows)}
    </div>
    """

    st.html(html)

def render_style_chips(styles: list[str]):
    html = '<div class="style-chip-wrap">'
    for style in styles:
        html += f'<div class="style-chip">{style}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    show_sidebar_logo(width=165)
    st.markdown("### Trimatch")
    st.caption("Your Style, Your Cut")
    st.divider()
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_EDA.py", label="Explore the Data", icon="📊")
    st.page_link("pages/2_Model_Performance.py", label="Model & Performance", icon="🧠")
    st.page_link("pages/3_Prediction.py", label="Find My Hairstyle", icon="✂️")
    st.page_link("pages/4_About.py", label="About Trimatch", icon="ℹ️")


# =========================================================
# MODEL CHECK
# =========================================================
if not model_is_available():
    st.error("model.pkl belum ditemukan. Pastikan file berada di root repo.")
    st.stop()

try:
    load_model()
except Exception as exc:
    st.error("Model ditemukan, tetapi gagal dimuat.")
    st.code(str(exc))
    st.stop()


# =========================================================
# PAGE HEADER
# =========================================================
page_header(
    "Try Trimatch",
    "Find My Hairstyle",
    "Upload foto wajah, prediksi bentuk wajah, lalu generate preview AI hairstyle "
    "berdasarkan rekomendasi untuk bentuk wajah tersebut.",
)


# =========================================================
# SESSION STATE
# =========================================================
if "image_signature" not in st.session_state:
    st.session_state.image_signature = None

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "generated_collage" not in st.session_state:
    st.session_state.generated_collage = None


# =========================================================
# INPUT
# =========================================================
section_title("Input", "Upload atau Ambil Foto")

mode = st.radio(
    "Pilih sumber gambar",
    ["Upload Image", "Camera"],
    horizontal=True,
)

uploaded = None
if mode == "Upload Image":
    uploaded = st.file_uploader(
        "Upload foto wajah",
        type=["jpg", "jpeg", "png"],
    )
else:
    uploaded = st.camera_input("Ambil foto")

if uploaded is None:
    st.info("Gunakan foto wajah yang jelas, menghadap kamera, dan pencahayaannya cukup.")
    st.stop()

raw_bytes = uploaded.getvalue()
current_signature = hashlib.md5(raw_bytes).hexdigest()

if st.session_state.image_signature != current_signature:
    st.session_state.image_signature = current_signature
    st.session_state.prediction_result = None
    st.session_state.generated_collage = None

image = Image.open(io.BytesIO(raw_bytes)).convert("RGB")

left, right = st.columns([0.9, 1.1], gap="large")

with left:
    st.image(
        image,
        caption="Foto yang dianalisis",
        use_container_width=True,
    )

with right:
    st.markdown(
        """
        <div class="info-panel">
            <div class="info-panel-title">Cara pakai</div>
            <ul class="info-panel-list">
                <li>Upload foto wajah atau gunakan kamera.</li>
                <li>Klik <strong>Analyze Face Shape</strong>.</li>
                <li>Lihat hasil prediksi dan 5 rekomendasi hairstyle.</li>
                <li>Klik <strong>Generate 5 AI Looks</strong> untuk melihat preview AI.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Analyze Face Shape", type="primary", use_container_width=True):
        try:
            with st.spinner("Menganalisis bentuk wajah..."):
                result = predict(image)
            st.session_state.prediction_result = result
            st.session_state.generated_collage = None
        except Exception as exc:
            st.error("Prediction gagal dijalankan.")
            st.code(str(exc))


# =========================================================
# RESULT
# =========================================================
if st.session_state.prediction_result is not None:
    result = st.session_state.prediction_result

    top1 = result["top1_class"]
    top2 = result["top2_class"]
    top1_prob = result["top1_probability"]
    top2_prob = result["top2_probability"]
    probs = result["probabilities"]

    rec = HAIRSTYLE_RECOMMENDATIONS[top1]
    styles = rec["styles"]

    st.divider()

    result_left, result_right = st.columns([0.8, 1.2], gap="large")

    with result_left:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-kicker">Predicted Face Shape</div>
                <div class="result-main">{top1.title()}</div>
                <div class="result-sub">
                    Confidence: <strong>{top1_prob:.1%}</strong><br>
                    Second possibility: <strong>{top2.title()}</strong> ({top2_prob:.1%})
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        confidence_gap = top1_prob - top2_prob
        if confidence_gap < 0.10:
            st.warning(
                "Prediksi pertama dan kedua cukup berdekatan. "
                "Pertimbangkan dua bentuk wajah teratas sebagai kemungkinan."
            )

    with result_right:
        section_title("Probability", "Distribusi probabilitas kelas")
        render_probability_bars(np.asarray(probs))

    st.divider()

    section_title("Recommendation", "Recommended hairstyles for you")
    render_style_chips(styles)
    st.caption(rec["note"])

    if st.button("Generate 5 AI Looks", use_container_width=True):
        try:
            with st.spinner("Membuat preview AI hairstyle..."):
                collage_bytes = generate_hairstyle_collage(
                    user_image=image,
                    face_shape=top1,
                    styles=styles,
                )
            st.session_state.generated_collage = collage_bytes
        except Exception as exc:
            st.error("Gagal generate preview AI hairstyle.")
            st.code(str(exc))

    if st.session_state.generated_collage is not None:
        st.markdown(
            """
            <div class="generated-title-wrap">
                <div class="generated-kicker">AI PREVIEW</div>
                <div class="generated-title">5 rekomendasi hairstyle pada foto kamu</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.image(
            st.session_state.generated_collage,
            caption="AI hairstyle preview collage",
            use_container_width=True,
        )

        st.download_button(
            "Download AI Preview",
            data=st.session_state.generated_collage,
            file_name="trimatch_ai_hairstyles.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
