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
            "Ovale faces are generally versatile and work well with many hairstyles. "
            "Clean and structured styles tend to create a balanced overall appearance."
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
            "For rectangular faces, extremely high volume on top is generally best avoided. "
            "Styles that maintain balanced facial proportions are usually more suitable."
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
            "More volume on top combined with shorter sides can help create the appearance "
            "of a longer and more defined face."
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
            "Texture on top and clean, structured sides can complement the strong jawline "
            "typically associated with square face shapes."
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

    image.convert("RGB").save(
        buffer,
        format="JPEG",
        quality=95
    )

    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")


def generate_hairstyle_collage(
    user_image: Image.Image,
    face_shape: str,
    styles: list[str]
):
    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY was not found. "
            "Please configure the API key in the Streamlit application secrets."
        )

    client = OpenAI(api_key=api_key)

    style_text = ", ".join(styles[:-1]) + f", and {styles[-1]}"

    prompt = f"""
Create one premium hairstyle try-on collage based on the provided user photo.

Requirements:
- Use the provided person's face and preserve identity as closely as possible.
- Keep the same person in all panels.
- Preserve the person's overall appearance and clothing.
- Show 5 separate panels in one single image collage.
- Each panel must show one different recommended hairstyle.
- The five hairstyles are: {style_text}.
- Add a small clean label for each panel with the hairstyle name.
- Make the result realistic, neat, professional, and suitable for a barber recommendation app.
- Keep the person male and natural-looking.
- Prefer head-and-shoulders framing so the hairstyle is clearly visible.
- The predicted face shape is {face_shape}.
- Use a polished premium barbershop aesthetic with a dark and elegant tone.
"""

    base64_image = pil_to_base64(user_image)

    response = client.responses.create(
        model="gpt-5.6",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        tools=[
            {
                "type": "image_generation"
            }
        ],
    )

    image_generation_calls = [
        output
        for output in response.output
        if output.type == "image_generation_call"
    ]

    if not image_generation_calls:
        raise RuntimeError(
            "The AI hairstyle preview could not be generated."
        )

    image_data = image_generation_calls[0].result
    image_bytes = base64.b64decode(image_data)

    return image_bytes


def render_probability_bars(probabilities: np.ndarray):
    labels = [
        class_name.title()
        for class_name in CLASS_NAMES
    ]

    pairs = list(
        zip(
            labels,
            probabilities.tolist()
        )
    )

    pairs = sorted(
        pairs,
        key=lambda x: x[1],
        reverse=True
    )

    rows = []

    for label, probability in pairs:

        width = max(
            probability * 100,
            4
        )

        rows.append(
            f"""
            <div class="prob-row">

                <div class="prob-top">
                    <span class="prob-label">
                        {label}
                    </span>

                    <span class="prob-value">
                        {probability:.1%}
                    </span>
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

    html = """
    <div class="style-chip-wrap">
    """

    for style in styles:

        html += f"""
        <div class="style-chip">
            {style}
        </div>
        """

    html += """
    </div>
    """

    st.html(html)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    show_sidebar_logo(width=165)

    st.markdown("### Trimatch")

    st.caption(
        "Your Style, Your Cut"
    )

    st.divider()

    st.page_link(
        "app.py",
        label="Home",
        icon="🏠"
    )

    st.page_link(
        "pages/1_EDA.py",
        label="Explore the Data",
        icon="📊"
    )

    st.page_link(
        "pages/2_Model_Performance.py",
        label="Model & Performance",
        icon="🧠"
    )

    st.page_link(
        "pages/3_Prediction.py",
        label="Find My Hairstyle",
        icon="✂️"
    )

    st.page_link(
        "pages/4_About.py",
        label="About Trimatch",
        icon="ℹ️"
    )


# =========================================================
# MODEL CHECK
# =========================================================
if not model_is_available():

    st.error(
        "model.pkl could not be found. "
        "Make sure the model file is located in the root directory of the repository."
    )

    st.stop()


try:

    load_model()

except Exception as exc:

    st.error(
        "The model was found, but it could not be loaded."
    )

    st.code(
        str(exc)
    )

    st.stop()


# =========================================================
# PAGE HEADER
# =========================================================
page_header(
    "Try Trimatch",
    "Find My Hairstyle",
    "Upload a facial image, predict your face shape, and receive hairstyle "
    "recommendations with an optional AI-generated hairstyle preview.",
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
section_title(
    "Input",
    "Upload or Capture a Photo"
)

mode = st.radio(
    "Choose an image source",
    [
        "Upload Image",
        "Camera"
    ],
    horizontal=True,
)


uploaded = None


if mode == "Upload Image":

    uploaded = st.file_uploader(
        "Upload a facial image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
    )

else:

    uploaded = st.camera_input(
        "Take a photo"
    )


if uploaded is None:

    st.info(
        "For the best prediction, use a clear front-facing photo "
        "with sufficient lighting and a visible face."
    )

    st.stop()


raw_bytes = uploaded.getvalue()

current_signature = hashlib.md5(
    raw_bytes
).hexdigest()


if st.session_state.image_signature != current_signature:

    st.session_state.image_signature = current_signature

    st.session_state.prediction_result = None

    st.session_state.generated_collage = None


image = Image.open(
    io.BytesIO(raw_bytes)
).convert("RGB")


left, right = st.columns(
    [0.9, 1.1],
    gap="large"
)


# =========================================================
# IMAGE PREVIEW
# =========================================================
with left:

    st.image(
        image,
        caption="Image to be analyzed",
        use_container_width=True,
    )


# =========================================================
# INSTRUCTIONS
# =========================================================
with right:

    st.html(
        """
        <div class="info-panel">

            <div class="info-panel-title">
                How to Use Trimatch
            </div>

            <ul class="info-panel-list">

                <li>
                    Upload a facial image or use your camera.
                </li>

                <li>
                    Click <strong>Analyze Face Shape</strong>.
                </li>

                <li>
                    Review the predicted face shape and five recommended hairstyles.
                </li>

                <li>
                    Click <strong>Generate 5 AI Looks</strong>
                    to preview the recommended hairstyles on your photo.
                </li>

            </ul>

        </div>
        """
    )


    if st.button(
        "Analyze Face Shape",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Analyzing face shape..."
            ):

                result = predict(
                    image
                )


            st.session_state.prediction_result = result

            st.session_state.generated_collage = None


        except Exception as exc:

            st.error(
                "The face-shape prediction could not be completed."
            )

            st.code(
                str(exc)
            )


# =========================================================
# RESULT
# =========================================================
if st.session_state.prediction_result is not None:

    result = st.session_state.prediction_result

    top1 = result[
        "top1_class"
    ]

    top2 = result[
        "top2_class"
    ]

    top1_prob = result[
        "top1_probability"
    ]

    top2_prob = result[
        "top2_probability"
    ]

    probs = result[
        "probabilities"
    ]


    rec = HAIRSTYLE_RECOMMENDATIONS[
        top1
    ]

    styles = rec[
        "styles"
    ]


    st.divider()


    result_left, result_right = st.columns(
        [0.8, 1.2],
        gap="large"
    )


    # =====================================================
    # PREDICTION RESULT
    # =====================================================
    with result_left:

        st.html(
            f"""
            <div class="result-card">

                <div class="result-kicker">
                    Predicted Face Shape
                </div>

                <div class="result-main">
                    {top1.title()}
                </div>

                <div class="result-sub">

                    Confidence:
                    <strong>
                        {top1_prob:.1%}
                    </strong>

                    <br>

                    Second possibility:
                    <strong>
                        {top2.title()}
                    </strong>

                    ({top2_prob:.1%})

                </div>

            </div>
            """
        )


        confidence_gap = (
            top1_prob
            -
            top2_prob
        )


        if confidence_gap < 0.10:

            st.warning(
                "The two highest predictions have similar confidence scores. "
                "Both face shapes may therefore be worth considering."
            )


    # =====================================================
    # PROBABILITY DISTRIBUTION
    # =====================================================
    with result_right:

        section_title(
            "Probability",
            "Class Probability Distribution"
        )

        render_probability_bars(
            np.asarray(probs)
        )


    st.divider()


    # =====================================================
    # HAIRSTYLE RECOMMENDATIONS
    # =====================================================
    section_title(
        "Recommendation",
        "Recommended Hairstyles for You"
    )


    render_style_chips(
        styles
    )


    st.caption(
        rec["note"]
    )


    # =====================================================
    # AI GENERATION
    # =====================================================
    if st.button(
        "Generate 5 AI Looks",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Generating your AI hairstyle preview..."
            ):

                collage_bytes = generate_hairstyle_collage(
                    user_image=image,
                    face_shape=top1,
                    styles=styles,
                )


            st.session_state.generated_collage = collage_bytes


        except Exception as exc:

            st.error(
                "The AI hairstyle preview could not be generated."
            )

            st.code(
                str(exc)
            )


    # =====================================================
    # AI RESULT
    # =====================================================
    if st.session_state.generated_collage is not None:

        st.html(
            """
            <div class="generated-title-wrap">

                <div class="generated-kicker">
                    AI PREVIEW
                </div>

                <div class="generated-title">
                    Your 5 Recommended Hairstyle Previews
                </div>

            </div>
            """
        )


        st.image(
            st.session_state.generated_collage,
            caption="AI-generated hairstyle preview collage",
            use_container_width=True,
        )


        st.download_button(
            "Download AI Preview",
            data=st.session_state.generated_collage,
            file_name="trimatch_ai_hairstyles.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
