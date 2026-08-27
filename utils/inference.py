import os
from pathlib import Path
import pickle

# Keras 3 needs a backend. Use TensorFlow because the model was trained with it.
os.environ.setdefault("KERAS_BACKEND", "tensorflow")

import keras
import numpy as np
import streamlit as st
from PIL import Image


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "model.pkl"

CLASS_NAMES = ["ovale", "rectangular", "round", "square"]


@st.cache_resource(show_spinner=False)
def load_model():
    """
    Load the final Trimatch Keras model stored as a pickle.

    The pickle references Keras classes directly, so `keras` must be imported
    before `pickle.load()` runs and the deployed Keras version should match
    the version used to create the file.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model tidak ditemukan di: {MODEL_PATH}. "
            "Pastikan model.pkl berada sejajar dengan app.py."
        )

    with MODEL_PATH.open("rb") as f:
        model = pickle.load(f)

    return model


def prepare_image(image: Image.Image) -> np.ndarray:
    """
    Preprocessing mengikuti notebook inference terbaru:
    1. RGB
    2. Resize 224 x 224
    3. Float32
    4. Scale pixel / 255
    5. Tambahkan batch dimension
    """
    image = image.convert("RGB")
    image = image.resize((224, 224))

    arr = np.asarray(image, dtype=np.float32)
    arr = arr / 255.0
    arr = np.expand_dims(arr, axis=0)

    return arr


def predict(image: Image.Image) -> dict:
    model = load_model()
    batch = prepare_image(image)

    raw_prediction = model.predict(batch, verbose=0)
    probabilities = np.asarray(raw_prediction, dtype=np.float32)[0]

    if probabilities.ndim != 1:
        raise ValueError(
            f"Output model tidak sesuai. Shape output: {probabilities.shape}"
        )

    if probabilities.shape[0] != len(CLASS_NAMES):
        raise ValueError(
            f"Model menghasilkan {probabilities.shape[0]} kelas, "
            f"sedangkan aplikasi mengharapkan {len(CLASS_NAMES)} kelas."
        )

    order = np.argsort(probabilities)[::-1]

    top1_idx = int(order[0])
    top2_idx = int(order[1])

    return {
        "probabilities": probabilities,
        "top1_index": top1_idx,
        "top2_index": top2_idx,
        "top1_class": CLASS_NAMES[top1_idx],
        "top2_class": CLASS_NAMES[top2_idx],
        "top1_probability": float(probabilities[top1_idx]),
        "top2_probability": float(probabilities[top2_idx]),
    }


def model_is_available() -> bool:
    return MODEL_PATH.exists()
