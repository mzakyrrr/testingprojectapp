import json
import pandas as pd
from .config import DATA_DIR

def load_eda_summary():
    path = DATA_DIR / "eda_summary.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def class_distribution_df(data):
    df = pd.DataFrame(data["class_distribution"])
    df["total"] = df["training"] + df["testing"]
    return df

def resolution_stats_df(data):
    return pd.DataFrame(data["resolution_stats"])

def top_resolutions_df(data):
    return pd.DataFrame(data["top_resolutions"])

def color_stats_df(data):
    return pd.DataFrame(data["color_stats"])
