import streamlit as st

from utils.style import apply_global_style, show_logo, show_sidebar_logo, page_header, section_title

st.set_page_config(
    page_title="Trimatch | Your Style, Your Cut",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_style()

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
    st.divider()
    st.caption("Final Project · HCK-042 FTDS")

page_header(
    "Trimatch",
    "Your Style, Your Cut",
    "Aplikasi computer vision untuk membantu mengidentifikasi bentuk wajah pria "
    "dan menghubungkannya dengan rekomendasi gaya rambut.",
)

left, right = st.columns([1.35, 0.65], gap="large")

# =========================
# SECTION 01 - LEFT
# =========================
with left:
    section_title("01", "Kenapa Trimatch?")

    st.html("""
    <div class="why-card">
        <div class="why-card-text">
            Menentukan bentuk wajah sendiri tidak selalu mudah karena batas visual
            antara <strong>ovale</strong>, <strong>rectangular</strong>,
            <strong>round</strong>, dan <strong>square</strong> dapat terlihat mirip.
            Trimatch membantu proses tersebut melalui klasifikasi gambar wajah
            untuk memberikan rekomendasi hairstyle yang lebih sesuai.
        </div>
    </div>
    """)

# =========================
# SECTION 01 - RIGHT
# =========================
with right:
    show_logo(width=300)

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

nav1, nav2, nav3 = st.columns(3, gap="large")

with nav1:
    st.html("""
    <div class="nav-card">
        <div class="nav-card-icon">📊</div>
        <div class="nav-card-title">Explore the Data</div>
        <div class="nav-card-desc">
            Lihat statistik dan visualisasi utama untuk memahami karakteristik dataset.
        </div>
    </div>
    """)

    st.page_link(
        "pages/1_EDA.py",
        label="Open EDA",
        icon="→",
        use_container_width=True
    )


with nav2:
    st.html("""
    <div class="nav-card">
        <div class="nav-card-icon">🧠</div>
        <div class="nav-card-title">Model & Performance</div>
        <div class="nav-card-desc">
            Pelajari arsitektur model dan lihat hasil evaluasi performa model.
        </div>
    </div>
    """)

    st.page_link(
        "pages/2_Model_Performance.py",
        label="Open Model Page",
        icon="→",
        use_container_width=True
    )


with nav3:
    st.html("""
    <div class="nav-card">
        <div class="nav-card-icon">✂️</div>
        <div class="nav-card-title">Find My Hairstyle</div>
        <div class="nav-card-desc">
            Upload foto wajah dan dapatkan prediksi bentuk wajah serta rekomendasi hairstyle.
        </div>
    </div>
    """)

    st.page_link(
        "pages/3_Prediction.py",
        label="Try Trimatch",
        icon="→",
        use_container_width=True
    )
