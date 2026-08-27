import streamlit as st

from utils.style import apply_global_style, show_logo, page_header, section_title

st.set_page_config(
    page_title="Model | Trimatch",
    page_icon="🧠",
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
    "Model",
    "Model & Performance",
    "Halaman ini mengikuti training.ipynb terbaru. "
    "Metrik final sengaja belum dikunci karena model masih dalam proses perbaikan.",
)

section_title("Current Architecture", "Arsitektur CNN terbaru")

st.code(
    """
Input (224 × 224 × 3)
        ↓
Conv2D 32 + Batch Normalization
        ↓
Conv2D 32 + Batch Normalization
        ↓
Max Pooling
        ↓
Conv2D 64 + Batch Normalization
        ↓
Conv2D 64 + Batch Normalization
        ↓
Max Pooling
        ↓
Conv2D 128 + Batch Normalization
        ↓
Conv2D 128 + Batch Normalization
        ↓
Max Pooling
        ↓
Global Average Pooling
        ↓
Dropout (0.25)
        ↓
Dense (128)
        ↓
Dense (4, Softmax)
    """,
    language="text",
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Input size", "224 × 224")
c2.metric("Output classes", "4")
c3.metric("Optimizer", "Adam")
c4.metric("Initial LR", "1e-3")

section_title("Preprocessing", "Input pipeline")
st.markdown(
    """
    1. Gambar dikonversi ke RGB.
    2. Gambar di-resize menjadi 224 × 224.
    3. Nilai piksel dibagi 255 sehingga berada pada rentang 0–1.
    4. Output model menggunakan empat kelas: `ovale`, `rectangular`, `round`, `square`.
    """
)

st.warning(
    "Catatan dari training.ipynb yang diberikan: EarlyStopping dan ReduceLROnPlateau "
    "sudah didefinisikan, tetapi perlu dipastikan benar-benar diteruskan ke model.fit() "
    "pada training final."
)

st.divider()

section_title("Final Evaluation", "Menunggu hasil model final")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Test Accuracy", "TBD")
m2.metric("Validation Accuracy", "TBD")
m3.metric("Precision", "TBD")
m4.metric("F1 Score", "TBD")

st.info(
    "Setelah model final selesai, halaman ini akan diisi dengan metric final, "
    "classification report, confusion matrix, serta grafik training/validation loss dan accuracy."
)
