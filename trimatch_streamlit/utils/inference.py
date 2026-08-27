import pickle
import numpy as np
import streamlit as st
from PIL import Image

from .config import MODEL_PATH, CLASS_NAMES

@st.cache_resource(show_spinner=False)
def load_model():
    if not MODEL_PATH.exists():
        return None

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def prepare_image(image: Image.Image) -> np.ndarray:
    """
    Current preprocessing based on inf.ipynb:
    - RGB
    - resize 224x224
    - scale pixels to 0-1
    - add batch dimension

    IMPORTANT:
    Re-check this function when the final model is delivered.
    """
    image = image.convert("RGB")
    image = image.resize((224, 224))

    arr = np.asarray(image).astype(np.float32)
    arr = arr / 255.0
    arr = np.expand_dims(arr, axis=0)

    return arr

def predict(model, image: Image.Image):
    batch = prepare_image(image)

    raw = model.predict(batch, verbose=0)
    probabilities = np.asarray(raw)[0]

    if probabilities.shape[0] != len(CLASS_NAMES):
        raise ValueError(
            f"Expected {len(CLASS_NAMES)} output classes, "
            f"but model returned {probabilities.shape[0]}."
        )

    order = np.argsort(probabilities)[::-1]

    return {
        "probabilities": probabilities,
        "order": order,
        "top1_index": int(order[0]),
        "top2_index": int(order[1]),
        "top1_class": CLASS_NAMES[int(order[0])],
        "top2_class": CLASS_NAMES[int(order[1])],
        "top1_probability": float(probabilities[int(order[0])]),
        "top2_probability": float(probabilities[int(order[1])]),
    }
