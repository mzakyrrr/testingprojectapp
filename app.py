import streamlit as st

from utils.style import (
    apply_global_style,
    show_logo,
    show_sidebar_logo,
    page_header,
    section_title,
)

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
    "A computer vision application designed to help identify men's face shapes "
    "and connect them with suitable hairstyle recommendations.",
)

left, right = st.columns([1.35, 0.65], gap="large")

# =========================
# SECTION 01 - LEFT
# =========================
with left:
    section_title("01", "Why Trimatch?")

    st.html("""
    <div class="why-card">
        <div class="why-card-text">
            Identifying your own face shape is not always easy because the visual
            differences between <strong>ovale</strong>, <strong>rectangular</strong>,
            <strong>round</strong>, and <strong>square</strong> can sometimes appear similar.
            Trimatch helps simplify this process by classifying facial images and
            providing hairstyle recommendations that better match the predicted face shape.
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

section_title("02", "How Trimatch Works")

st.html("""
<div class="process-grid">

    <div class="process-card">
        <div class="process-step">01</div>

        <div class="process-title">
            Photo Input
        </div>

        <div class="process-desc">
            Upload an image or use your camera to begin the analysis.
        </div>
    </div>

    <div class="process-card">
        <div class="process-step">02</div>

        <div class="process-title">
            Classification
        </div>

        <div class="process-desc">
            The model analyzes the image and produces probabilities for four face-shape classes.
        </div>
    </div>

    <div class="process-card">
        <div class="process-step">03</div>

        <div class="process-title">
            Recommendation
        </div>

        <div class="process-desc">
            The prediction result is used as the basis for recommending suitable hairstyles.
        </div>
    </div>

</div>
""")

st.divider()
section_title("Navigation", "Explore Trimatch")

st.html("""
<div class="nav-grid">

    <a class="nav-card-link" href="/EDA">
        <div class="nav-card">
            <div class="nav-card-icon">📊</div>

            <div class="nav-card-title">
                Explore the Data
            </div>

            <div class="nav-card-desc">
                View key statistics and visualizations
                to better understand the dataset.
            </div>

            <div class="nav-card-button">
                Open EDA
                <span>→</span>
            </div>
        </div>
    </a>


    <a class="nav-card-link" href="/Model_Performance">
        <div class="nav-card">
            <div class="nav-card-icon">🧠</div>

            <div class="nav-card-title">
                Model & Performance
            </div>

            <div class="nav-card-desc">
                Explore the model architecture and review
                its performance evaluation results.
            </div>

            <div class="nav-card-button">
                Open Model Page
                <span>→</span>
            </div>
        </div>
    </a>


    <a class="nav-card-link" href="/Prediction">
        <div class="nav-card">
            <div class="nav-card-icon">✂️</div>

            <div class="nav-card-title">
                Find My Hairstyle
            </div>

            <div class="nav-card-desc">
                Upload a facial image to get a face-shape
                prediction and hairstyle recommendations.
            </div>

            <div class="nav-card-button">
                Try Trimatch
                <span>→</span>
            </div>
        </div>
    </a>

</div>
""")
