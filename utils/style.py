from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]

def apply_global_style():
    css_path = ROOT_DIR / "style.css"

    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

def show_logo(width=180):
    logo_path = ROOT_DIR / "assets" / "Logo_Trimatch.jpeg"

    if logo_path.exists():
        st.image(str(logo_path), width=width)

def show_sidebar_logo(width=180):
    logo_path = ROOT_DIR / "assets" / "trimatchblackbg.png"

    if logo_path.exists():
        st.image(str(logo_path), width=width)

def page_header(kicker, title, description):
    st.markdown(
        f"""
        <div class="trimatch-hero">
            <div class="trimatch-kicker">{kicker}</div>
            <div class="trimatch-title">{title}</div>
            <div class="trimatch-subtitle">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def section_title(label, title, description=None):
    st.markdown(
        f'<div class="section-label">{label}</div>',
        unsafe_allow_html=True
    )

    st.subheader(title)

    if description:
        st.caption(description)
