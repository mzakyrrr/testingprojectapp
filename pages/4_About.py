import streamlit as st

from utils.style import apply_global_style, show_logo, show_sidebar_logo, page_header, section_title

st.set_page_config(
    page_title="About | Trimatch",
    page_icon="ℹ️",
    layout="wide",
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

page_header(
    "About",
    "About Trimatch",
    "Final Project Hacktiv8 Batch HCK-042 FTDS.",
)

left, right = st.columns([1.25, 1], gap="large")

with left:
    section_title("Project", "Trimatch: Your Style, Your Cut")
    st.write(
        "Trimatch adalah aplikasi berbasis computer vision untuk mengklasifikasikan "
        "bentuk wajah pria ke dalam empat kategori: ovale, rectangular, round, dan square. "
        "Hasil klasifikasi digunakan sebagai dasar rekomendasi hairstyle."
    )

    section_title("Technology", "Built with")
    st.write("Python · TensorFlow/Keras · NumPy · Pandas · Streamlit")

    section_title("Scope", "Fitur utama")
    st.markdown(
        """
        - Ringkasan EDA dataset.
        - Penjelasan model.
        - Upload gambar dan camera input.
        - Probabilitas empat kelas wajah.
        - Top-1 dan second possibility.
        - Hairstyle recommendation berdasarkan hasil klasifikasi.
        """
    )

with right:
    show_logo(width=300)

    section_title("Team", "Project members")
    st.write(
        """
        **Muhammad Cesar Rivaldo (Data Analyst)**  
        **Muhammad Rafi Addien (Data Scientist)**  
        **Muhammad Zaky Ramadhan (Data Engineer)**  
        **Muhammad Zulyandhika (Data Engineer, Data Analyst)**
        """
    )

st.divider()

section_title("Limitations", "Batasan aplikasi")
st.write(
    "Klasifikasi bentuk wajah memiliki ambiguitas visual antarkelas. "
    "Hasil aplikasi sebaiknya digunakan sebagai bantuan rekomendasi, bukan penilaian absolut. "
    "Sudut wajah, pencahayaan, framing, dan perbedaan karakteristik foto pengguna terhadap "
    "data training dapat memengaruhi prediksi."
)
