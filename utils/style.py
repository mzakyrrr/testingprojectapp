import streamlit as st
from .config import LOGO_PATH

def apply_global_style():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1180px;
            }

            [data-testid="stSidebar"] {
                border-right: 1px solid rgba(128,128,128,.18);
            }

            .trimatch-hero {
                padding: 2.3rem 2.4rem;
                border: 1px solid rgba(128,128,128,.20);
                border-radius: 24px;
                margin-bottom: 1.5rem;
                background: rgba(128,128,128,.035);
            }

            .trimatch-kicker {
                font-size: .82rem;
                letter-spacing: .16em;
                text-transform: uppercase;
                opacity: .65;
                font-weight: 700;
            }

            .trimatch-title {
                font-size: 3rem;
                font-weight: 800;
                line-height: 1.08;
                margin-top: .35rem;
                margin-bottom: .45rem;
            }

            .trimatch-subtitle {
                font-size: 1.08rem;
                opacity: .76;
                max-width: 760px;
            }

            .section-label {
                font-size: .8rem;
                letter-spacing: .12em;
                text-transform: uppercase;
                opacity: .62;
                font-weight: 700;
                margin-top: .5rem;
                margin-bottom: .2rem;
            }

            .info-card {
                border: 1px solid rgba(128,128,128,.18);
                border-radius: 18px;
                padding: 1.15rem 1.2rem;
                min-height: 130px;
                background: rgba(128,128,128,.025);
            }

            .result-card {
                border: 1px solid rgba(128,128,128,.18);
                border-radius: 20px;
                padding: 1.4rem;
                background: rgba(128,128,128,.03);
            }

            .face-result {
                font-size: 2.2rem;
                font-weight: 800;
                text-transform: capitalize;
            }

            .soft-note {
                opacity: .72;
                font-size: .94rem;
            }

            div[data-testid="stMetric"] {
                border: 1px solid rgba(128,128,128,.18);
                padding: 1rem;
                border-radius: 16px;
                background: rgba(128,128,128,.025);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_logo(width=180):
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=width)

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
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    st.subheader(title)
    if description:
        st.caption(description)
