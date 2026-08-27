import streamlit as st
import pandas as pd
from PIL import Image

from utils.style import apply_global_style, show_logo, page_header
from utils.config import CLASS_NAMES, HAIRSTYLE_RECOMMENDATIONS
from utils.inference import load_model, predict

st.set_page_config(
    page_title="Prediction | Trimatch",
    page_icon="✂️",
    layout="wide",
)

apply_global_style()

with st.sidebar:
    show_logo(width=165)
    st.markdown("### Trimatch")
    st.caption("Your Style, Your Cut")
    st.divider()
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_EDA.py", label="Explore the Data", icon="📊")
    st.page_link("pages/2_Model_Performance.py", label="Model & Performance", icon="🧠")
    st.page_link("pages/3_Prediction.py", label="Find My Hairstyle", icon="✂️")
    st.page_link("pages/4_About.py", label="About Trimatch", icon="ℹ️")

page_header(
    "Try Trimatch",
    "Find My Hairstyle",
    "Unggah foto atau gunakan kamera. Prediksi akan aktif ketika model.pkl final tersedia.",
)

model = None
model_error = None

try:
    model = load_model()
except Exception as exc:
    model_error = str(exc)

if model is None:
    if model_error:
        st.error(f"model.pkl ditemukan tetapi gagal dimuat: {model_error}")
    else:
        st.warning(
            "Model final belum tersedia. UI prediction sudah siap. "
            "Nanti cukup tambahkan model.pkl ke root folder project."
        )

mode = st.radio(
    "Pilih sumber gambar",
    ["Upload image", "Camera"],
    horizontal=True,
)

uploaded = None

if mode == "Upload image":
    uploaded = st.file_uploader(
        "Upload foto wajah",
        type=["jpg", "jpeg", "png"],
    )
else:
    uploaded = st.camera_input("Ambil foto")

if uploaded is None:
    st.caption(
        "Gunakan foto dengan wajah yang terlihat jelas, pencahayaan cukup, "
        "dan framing yang mendekati karakteristik data training."
    )
    st.stop()

image = Image.open(uploaded).convert("RGB")

left, right = st.columns([1, 1.15], gap="large")

with left:
    st.image(image, caption="Input image", use_container_width=True)

with right:
    if model is None:
        st.markdown("### Image preview")
        st.write(
            "Gambar berhasil dibaca. Prediction baru dijalankan ketika model final tersedia."
        )
        st.code(
            "model.pkl → resize 224×224 → /255 → predict → probability → hairstyle",
            language="text",
        )
        st.stop()

    if st.button("Analyze Face Shape", type="primary", use_container_width=True):
        try:
            with st.spinner("Analyzing face shape..."):
                result = predict(model, image)

            top1 = result["top1_class"]
            top2 = result["top2_class"]
            top1_prob = result["top1_probability"]
            top2_prob = result["top2_probability"]

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="section-label">Predicted face shape</div>
                    <div class="face-result">{top1}</div>
                    <div class="soft-note">
                        Confidence: {top1_prob:.1%}<br>
                        Second possibility: {top2.title()} ({top2_prob:.1%})
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### Prediction probabilities")

            prob_df = pd.DataFrame(
                {
                    "Face Shape": [x.title() for x in CLASS_NAMES],
                    "Probability": [
                        float(p) for p in result["probabilities"]
                    ],
                }
            ).set_index("Face Shape")

            st.bar_chart(prob_df)

            recommendation = HAIRSTYLE_RECOMMENDATIONS[top1]

            st.markdown("### Recommended hairstyles")

            styles = recommendation["styles"]
            columns = st.columns(3)

            for idx, style in enumerate(styles):
                with columns[idx % 3]:
                    st.markdown(
                        f'<div class="info-card"><b>✂️ {style}</b></div>',
                        unsafe_allow_html=True,
                    )

            st.info(recommendation["note"])

            confidence_gap = top1_prob - top2_prob
            if confidence_gap < 0.10:
                st.warning(
                    "Prediksi pertama dan kedua cukup berdekatan. "
                    "Interpretasikan hasil sebagai dua kemungkinan bentuk wajah."
                )

        except Exception as exc:
            st.error(f"Prediction gagal dijalankan: {exc}")
