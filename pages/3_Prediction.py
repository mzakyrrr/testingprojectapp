import streamlit as st
import pandas as pd
from PIL import Image

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
# PAGE HEADER
# =========================================================
page_header(
    "Try Trimatch",
    "Find My Hairstyle",
    "Upload foto wajah atau gunakan kamera. Trimatch akan memprediksi bentuk wajah "
    "dan menampilkan probabilitas untuk empat kelas.",
)


# =========================================================
# HAIRSTYLE RECOMMENDATIONS
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
            "Wajah ovale cukup fleksibel untuk berbagai hairstyle. "
            "Gaya dengan struktur yang tetap memperlihatkan dahi biasanya cocok."
        ),
    },
    "rectangular": {
        "styles": [
            "Layered Medium Length",
            "Textured Side Part",
            "Textured Fringe",
            "Classic Taper",
        ],
        "note": (
            "Untuk wajah rectangular, volume yang terlalu tinggi dapat membuat wajah "
            "terlihat semakin panjang. Pilih tekstur dan volume yang lebih seimbang."
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
            "Tambahan tinggi di bagian atas dan sisi yang lebih pendek dapat membantu "
            "memberi kesan wajah yang lebih panjang dan terstruktur."
        ),
    },
    "square": {
        "styles": [
            "Textured Crop",
            "Quiff",
            "High Fade",
            "Undercut",
            "Side Part",
            "Pompadour",
        ],
        "note": (
            "Tekstur dan volume pada bagian atas dapat melengkapi karakter rahang "
            "yang tegas pada wajah square."
        ),
    },
}


# =========================================================
# MODEL STATUS
# =========================================================
if not model_is_available():
    st.error(
        "model.pkl belum ditemukan. Taruh model.pkl di root repository, "
        "sejajar dengan app.py."
    )
    st.stop()

try:
    load_model()
except Exception as exc:
    st.error("Model ditemukan, tetapi gagal dimuat.")
    st.code(str(exc))
    st.info(
        "Pastikan deployment menggunakan Python 3.12 dan dependency di requirements.txt "
        "sesuai file integrasi model."
    )
    st.stop()


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
    st.info(
        "Gunakan foto wajah yang jelas, menghadap kamera, dan memiliki pencahayaan yang cukup."
    )
    st.stop()


image = Image.open(uploaded).convert("RGB")

left, right = st.columns([0.85, 1.15], gap="large")

with left:
    st.image(
        image,
        caption="Foto yang dianalisis",
        use_container_width=True,
    )


# =========================================================
# PREDICTION
# =========================================================
with right:
    if st.button(
        "Analyze Face Shape",
        type="primary",
        use_container_width=True,
    ):
        try:
            with st.spinner("Menganalisis bentuk wajah..."):
                result = predict(image)

            top1 = result["top1_class"]
            top2 = result["top2_class"]
            top1_prob = result["top1_probability"]
            top2_prob = result["top2_probability"]

            st.html(
                f"""
                <div class="result-card">
                    <div class="section-label">Predicted Face Shape</div>
                    <div class="face-result">{top1}</div>
                    <div class="soft-note">
                        Confidence: <strong>{top1_prob:.1%}</strong><br>
                        Second possibility:
                        <strong>{top2.title()}</strong> ({top2_prob:.1%})
                    </div>
                </div>
                """
            )

            st.markdown("### Prediction Probability")

            probability_df = pd.DataFrame(
                {
                    "Face Shape": [name.title() for name in CLASS_NAMES],
                    "Probability": [
                        float(p) for p in result["probabilities"]
                    ],
                }
            ).set_index("Face Shape")

            st.bar_chart(
                probability_df,
                horizontal=True,
                color="#C89F52",
            )

            confidence_gap = top1_prob - top2_prob

            if confidence_gap < 0.10:
                st.warning(
                    "Prediksi pertama dan kedua cukup berdekatan. "
                    "Pertimbangkan keduanya sebagai kemungkinan bentuk wajah."
                )

            st.divider()

            section_title("Recommendation", "Hairstyle Recommendations")

            recommendation = HAIRSTYLE_RECOMMENDATIONS[top1]

            cols = st.columns(3)

            for idx, style_name in enumerate(recommendation["styles"]):
                with cols[idx % 3]:
                    st.html(
                        f"""
                        <div class="info-card">
                            <strong>✂️ {style_name}</strong>
                        </div>
                        """
                    )

            st.info(recommendation["note"])

        except Exception as exc:
            st.error("Prediction gagal dijalankan.")
            st.code(str(exc))
