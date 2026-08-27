import streamlit as st

from utils.style import apply_global_style, show_logo, page_header, section_title

st.set_page_config(
    page_title="Trimatch | Your Style, Your Cut",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
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
    st.divider()
    st.caption("Final Project · HCK-042 FTDS")

page_header(
    "Trimatch",
    "Your Style, Your Cut",
    "Aplikasi computer vision untuk membantu mengidentifikasi bentuk wajah pria "
    "dan menghubungkannya dengan rekomendasi gaya rambut.",
)

left, right = st.columns([1.2, 1], gap="large")

# =========================
# SECTION 01 - LEFT
# =========================
with left:
    section_title("01", "Kenapa Trimatch?")

    st.write(
        "Menentukan bentuk wajah sendiri tidak selalu mudah karena batas visual "
        "antara ovale, rectangular, round, dan square dapat terlihat mirip. "
        "Trimatch membantu proses tersebut melalui klasifikasi gambar wajah."
    )


# =========================
# SECTION 01 - RIGHT
# =========================
with right:
    show_logo(width=340)

    st.markdown("### Face-shape Classes")

    st.write(
        "Ovale · Rectangular · Round · Square"
    )


# =========================
# SECTION 02 - FULL WIDTH
# =========================
st.markdown("<br>", unsafe_allow_html=True)

section_title("02", "Cara Kerja Aplikasi")

st.html("""
<div class="process-grid">

    <div class="process-card">
        <div class="process-step">01</div>

        <div class="process-title">
            Input Foto
        </div>

        <div class="process-desc">
            Unggah gambar atau gunakan kamera untuk memulai analisis.
        </div>
    </div>

    <div class="process-card">
        <div class="process-step">02</div>

        <div class="process-title">
            Klasifikasi
        </div>

        <div class="process-desc">
            Model menganalisis gambar dan menghasilkan probabilitas empat bentuk wajah.
        </div>
    </div>

    <div class="process-card">
        <div class="process-step">03</div>

        <div class="process-title">
            Rekomendasi
        </div>

        <div class="process-desc">
            Hasil prediksi digunakan sebagai dasar rekomendasi hairstyle yang sesuai.
        </div>
    </div>

</div>
""")

st.divider()
section_title("Navigation", "Explore Trimatch")

a, b, c = st.columns(3)
with a:
    st.markdown("#### 📊 Explore the Data")
    st.write("Lihat statistik dan visualisasi utama dataset.")
    st.page_link("pages/1_EDA.py", label="Open EDA")

with b:
    st.markdown("#### 🧠 Model & Performance")
    st.write("Lihat arsitektur model dan hasil evaluasi final.")
    st.page_link("pages/2_Model_Performance.py", label="Open Model Page")

with c:
    st.markdown("#### ✂️ Find My Hairstyle")
    st.write("Upload foto dan jalankan prediksi ketika model final tersedia.")
    st.page_link("pages/3_Prediction.py", label="Try Trimatch")

st.info(
    "Model final belum dimasukkan. Struktur aplikasi tetap bisa dikembangkan sekarang, "
    "lalu model.pkl final tinggal ditambahkan ke root project."
)
