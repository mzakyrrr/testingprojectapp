from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"

LOGO_PATH = ASSETS_DIR / "Logo_Trimatch.jpeg"
MODEL_PATH = ROOT_DIR / "model.pkl"

CLASS_NAMES = ["ovale", "rectangular", "round", "square"]

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
            "Bentuk wajah ovale cukup fleksibel untuk banyak gaya rambut. "
            "Gaya yang mempertahankan dahi tetap terlihat biasanya membantu menjaga proporsi wajah."
        ),
    },
    "rectangular": {
        "styles": [
            "Layered Medium Length",
            "Side Part with Texture",
            "Textured Fringe",
            "Classic Taper",
        ],
        "note": (
            "Pilih gaya dengan volume yang terkontrol agar wajah tidak terlihat semakin panjang. "
            "Tekstur di sisi kepala dapat membantu menyeimbangkan proporsi."
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
            "Tambahan tinggi di bagian atas dan sisi yang lebih pendek dapat memberi kesan "
            "wajah yang lebih panjang dan terstruktur."
        ),
    },
    "square": {
        "styles": [
            "Textured Crop",
            "Quiff",
            "High Fade",
            "Undercut",
            "Side Part",
            "Pompadour",
        ],
        "note": (
            "Tekstur dan volume di bagian atas dapat melengkapi karakter rahang yang tegas "
            "pada wajah square."
        ),
    },
}
