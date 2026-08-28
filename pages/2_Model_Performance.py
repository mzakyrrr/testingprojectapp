import streamlit as st

from utils.style import (
    apply_global_style,
    show_logo,
    show_sidebar_logo,
    page_header,
    section_title,
)

st.set_page_config(
    page_title="Model | Trimatch",
    page_icon="🧠",
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
    "Model",
    "Model & Performance",
    "This page presents the CNN architecture, preprocessing pipeline, "
    "and final evaluation results of the Trimatch face-shape classification model.",
)


# =========================================================
# MODEL ARCHITECTURE
# =========================================================
section_title(
    "Current Architecture",
    "CNN Architecture"
)

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

c1.metric("Input Size", "224 × 224")
c2.metric("Output Classes", "4")
c3.metric("Optimizer", "Adam")
c4.metric("Initial Learning Rate", "1e-3")


# =========================================================
# PREPROCESSING
# =========================================================
section_title(
    "Preprocessing",
    "Input Pipeline"
)

st.markdown(
    """
    1. The input image is converted to RGB.
    2. The image is resized to **224 × 224 pixels**.
    3. Pixel values are divided by **255** and normalized to the **0–1 range**.
    4. The model predicts one of four face-shape classes:
       `ovale`, `rectangular`, `round`, or `square`.
    """
)

st.divider()


# =========================================================
# FINAL EVALUATION
# =========================================================
section_title(
    "Final Evaluation",
    "Final Model Performance"
)

m1, m2 = st.columns(2)

m1.metric(
    "Test Accuracy",
    "58.0%"
)

m2.metric(
    "Validation Accuracy",
    "67.0%"
)

st.caption(
    "Test accuracy measures the model's performance on unseen test data, "
    "while validation accuracy reflects performance during model development."
)

st.markdown("### Per-Class Performance")

performance = {
    "Ovale": {
        "support": 66,
        "precision": 0.64,
        "recall": 0.55,
        "f1": 0.59,
    },
    "Rectangular": {
        "support": 58,
        "precision": 0.46,
        "recall": 0.66,
        "f1": 0.54,
    },
    "Round": {
        "support": 64,
        "precision": 0.70,
        "recall": 0.61,
        "f1": 0.65,
    },
    "Square": {
        "support": 62,
        "precision": 0.59,
        "recall": 0.53,
        "f1": 0.56,
    },
}

table_html = """
<div class="trimatch-table-wrap">
    <table class="trimatch-table">
        <thead>
            <tr>
                <th>Face Shape</th>
                <th>Support</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1 Score</th>
            </tr>
        </thead>
        <tbody>
"""

for face_shape, metrics in performance.items():
    table_html += f"""
        <tr>
            <td class="shape-name">{face_shape}</td>
            <td>{metrics["support"]}</td>
            <td>{metrics["precision"]:.2f}</td>
            <td>{metrics["recall"]:.2f}</td>
            <td class="total-value">{metrics["f1"]:.2f}</td>
        </tr>
    """

table_html += """
        </tbody>
    </table>
</div>
"""

st.html(table_html)


# =========================================================
# PERFORMANCE INTERPRETATION
# =========================================================
st.markdown("### Performance Interpretation")

st.markdown(
    """
    - **Round** achieved the strongest overall class-level performance, with a
      precision of **0.70** and an F1-score of **0.65**.
    - **Rectangular** achieved the highest recall at **0.66**, meaning the model
      identified a relatively high proportion of rectangular faces. However,
      its precision was the lowest at **0.46**, indicating more false-positive
      predictions for this class.
    - **Ovale** achieved a precision of **0.64**, recall of **0.55**, and
      F1-score of **0.59**.
    - **Square** achieved a precision of **0.59**, recall of **0.53**, and
      F1-score of **0.56**.
    """
)

st.info(
    "The final CNN achieved 58% test accuracy and 67% validation accuracy. "
    "The class-level metrics show that model performance varies across face-shape classes, "
    "with the round class producing the strongest F1-score."
)
