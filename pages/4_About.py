import streamlit as st

from utils.style import (
    apply_global_style,
    show_logo,
    show_sidebar_logo,
    page_header,
    section_title,
)

st.set_page_config(
    page_title="About | Trimatch",
    page_icon="ℹ️",
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
    "About",
    "About Trimatch",
    "Final Project · Hacktiv8 Batch HCK-042 FTDS",
)

left, right = st.columns([1.25, 1], gap="large")


# =========================================================
# LEFT COLUMN
# =========================================================
with left:

    section_title(
        "Project",
        "Trimatch: Your Style, Your Cut"
    )

    st.write(
        "Trimatch is a computer vision application designed to classify men's "
        "face shapes into four categories: ovale, rectangular, round, and square. "
        "The predicted face shape is then used as the basis for providing "
        "hairstyle recommendations."
    )


    section_title(
        "Technology",
        "Built With"
    )

    st.write(
        "Python · TensorFlow/Keras · NumPy · Pandas · Streamlit · OpenAI"
    )


    section_title(
        "Scope",
        "Key Features"
    )

    st.markdown(
        """
        - Exploratory Data Analysis (EDA) summary and visualizations.
        - CNN architecture and model performance overview.
        - Image upload and camera input.
        - Probability distribution across four face-shape classes.
        - Top prediction and second-most likely face shape.
        - Hairstyle recommendations based on the predicted face shape.
        - AI-generated hairstyle previews using the user's uploaded photo.
        """
    )


# =========================================================
# RIGHT COLUMN
# =========================================================
with right:

    show_logo(width=300)

    section_title(
        "Team",
        "Project Members"
    )

    st.write(
        """
        **Muhammad Cesar Rivaldo — Data Analyst**  
        **Muhammad Rafi Addien — Data Scientist**  
        **Muhammad Zaky Ramadhan — Data Engineer**  
        **Muhammad Zulyandhika — Data Engineer & Data Analyst**
        """
    )


st.divider()


# =========================================================
# LIMITATIONS
# =========================================================
section_title(
    "Limitations",
    "Limitations & Disclaimer"
)

st.write(
    "Face-shape classification involves visual ambiguity between classes. "
    "Trimatch should therefore be used as a recommendation aid rather than "
    "an absolute assessment of a person's face shape. Prediction results may "
    "be affected by head angle, lighting conditions, image framing, hairstyle, "
    "and differences between user-submitted photos and the images used during training."
)

st.info(
    "The AI hairstyle preview is generated for visualization purposes only. "
    "The final appearance of a real haircut may vary depending on hair texture, "
    "hair density, styling technique, and individual facial characteristics."
)
