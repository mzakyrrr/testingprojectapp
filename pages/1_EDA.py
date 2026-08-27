import streamlit as st
import altair as alt

from utils.style import apply_global_style, show_logo, show_sidebar_logo, page_header, section_title
from utils.eda import (
    load_eda_summary,
    class_distribution_df,
    resolution_stats_df,
    top_resolutions_df,
    color_stats_df,
)

st.set_page_config(
    page_title="EDA | Trimatch",
    page_icon="📊",
    layout="wide",
)

apply_global_style()
data = load_eda_summary()

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
    "Explore the Data",
    "Exploratory Data Analysis",
    "Statistik dan visualisasi utama dari EDA_full.ipynb. "
    "Dataset mentah tidak perlu dimuat ulang saat aplikasi dijalankan.",
)

section_title("Dataset Overview", "Gambaran umum dataset")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total valid images", f'{data["raw_total"]:,}')
m2.metric("Training set", f'{data["train_total"]:,}')
m3.metric("Testing set", f'{data["test_total"]:,}')
m4.metric("Corrupt images", data["corrupt_images"])

st.caption(
    "EDA mencatat seluruh gambar yang terbaca berada pada mode RGB. "
    "Distribusi kelas secara total relatif seimbang."
)

st.divider()

section_title("Class Distribution", "Distribusi gambar per bentuk wajah")

class_df = class_distribution_df(data)

chart_df = class_df.melt(
    id_vars="face_shape",
    value_vars=["training", "testing"],
    var_name="Dataset",
    value_name="Jumlah"
)

chart = (
    alt.Chart(chart_df)
    .mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    )
    .encode(
        x=alt.X(
            "face_shape:N",
            title=None,
            axis=alt.Axis(
                labelColor="#D8D0C5",
                labelFontSize=13,
                labelPadding=12
            )
        ),

        y=alt.Y(
            "Jumlah:Q",
            title="Jumlah Gambar",
            axis=alt.Axis(
                labelColor="#BDB3A5",
                titleColor="#D8D0C5",
                gridColor="rgba(216,180,106,0.10)"
            )
        ),

        color=alt.Color(
            "Dataset:N",
            scale=alt.Scale(
                domain=["training", "testing"],
                range=["#C89F52", "#F1D89A"]
            ),
            legend=alt.Legend(
                title=None,
                labelColor="#D8D0C5",
                orient="bottom"
            )
        ),

        tooltip=[
            alt.Tooltip("face_shape:N", title="Face Shape"),
            alt.Tooltip("Dataset:N"),
            alt.Tooltip("Jumlah:Q")
        ]
    )
    .properties(
        height=380
    )
    .configure_view(
        stroke=None,
        fill="transparent"
    )
    .configure(
        background="transparent"
    )
)

st.altair_chart(
    chart,
    use_container_width=True
)

with st.expander("Lihat angka distribusi"):

    view = class_df.rename(
        columns={
            "face_shape": "Face Shape",
            "training": "Training",
            "testing": "Testing",
            "total": "Total",
        }
    )

    table_html = """
    <div class="trimatch-table-wrap">
        <table class="trimatch-table">
            <thead>
                <tr>
                    <th>Face Shape</th>
                    <th>Training</th>
                    <th>Testing</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
    """

    for _, row in view.iterrows():
        table_html += f"""
                <tr>
                    <td class="shape-name">{row["Face Shape"]}</td>
                    <td>{row["Training"]}</td>
                    <td>{row["Testing"]}</td>
                    <td class="total-value">{row["Total"]}</td>
                </tr>
        """

    table_html += """
            </tbody>
        </table>
    </div>
    """

    st.html(table_html)

st.markdown(
    """
    **Insight:** jumlah data antarkelas relatif seimbang secara total. Namun,
    komposisi training dan testing tidak identik pada setiap kelas.
    """
)

st.divider()

section_title("Image Dimensions", "Karakteristik resolusi gambar")

left, right = st.columns([1, 1.15], gap="large")

with left:
    res_df = resolution_stats_df(data).rename(
        columns={
            "statistic": "Statistic",
            "width": "Width (px)",
            "height": "Height (px)",
            "megapixels": "Megapixels",
        }
    )

    table_html = """
    <div class="trimatch-table-wrap">
        <table class="trimatch-table">
            <thead>
                <tr>
                    <th>Statistic</th>
                    <th>Width (px)</th>
                    <th>Height (px)</th>
                    <th>Megapixels</th>
                </tr>
            </thead>
            <tbody>
    """

    for _, row in res_df.iterrows():
        table_html += f"""
                <tr>
                    <td class="shape-name">{row["Statistic"]}</td>
                    <td>{row["Width (px)"]}</td>
                    <td>{row["Height (px)"]}</td>
                    <td class="total-value">{row["Megapixels"]}</td>
                </tr>
        """

    table_html += """
            </tbody>
        </table>
    </div>
    """

    st.html(table_html)

    st.metric(
        "Unique resolutions",
        data["quality"]["unique_resolutions"]
    )

    st.caption(
        "Dataset memiliki variasi resolusi yang besar, sehingga proses resize "
        "sebelum masuk ke model menjadi penting."
    )


with right:
    st.markdown("**10 resolusi paling umum**")

    top_df = top_resolutions_df(data)

    resolution_chart = (
        alt.Chart(top_df)
        .mark_bar(
            color="#C89F52",
            cornerRadiusTopLeft=6,
            cornerRadiusTopRight=6
        )
        .encode(
            x=alt.X(
                "resolution:N",
                title=None,
                sort="-y",
                axis=alt.Axis(
                    labelColor="#D8D0C5",
                    labelAngle=-45,
                    labelFontSize=11,
                    labelPadding=8
                )
            ),
            y=alt.Y(
                "count:Q",
                title="Jumlah Gambar",
                axis=alt.Axis(
                    labelColor="#BDB3A5",
                    titleColor="#D8D0C5",
                    gridColor="#2A241C",
                    tickColor="#5A4932",
                    domainColor="#5A4932"
                )
            ),
            tooltip=[
                alt.Tooltip(
                    "resolution:N",
                    title="Resolution"
                ),
                alt.Tooltip(
                    "count:Q",
                    title="Jumlah"
                )
            ]
        )
        .properties(
            height=330
        )
        .configure_view(
            stroke="#5A4932",
            strokeWidth=1,
            cornerRadius=16,
            fill="#0F0E0D"
        )
        .configure(
            background="transparent"
        )
    )

    st.altair_chart(
        resolution_chart,
        use_container_width=True
    )
    
st.divider()

section_title("Image File Size", "Ukuran file dan outlier")

fs = data["file_size"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mean", f'{fs["mean_kb"]:.1f} KB')
c2.metric("Median", f'{fs["median_kb"]:.1f} KB')
c3.metric("Maximum", f'{fs["max_kb"]:,.1f} KB')
c4.metric("IQR outliers", fs["iqr_outliers"])

st.write(
    "Distribusi ukuran file cukup lebar. Nilai median jauh di bawah nilai maksimum, "
    "menunjukkan adanya sejumlah file berukuran jauh lebih besar dari mayoritas data."
)

st.divider()

section_title("Color & Brightness", "Karakteristik warna rata-rata")

color_df = color_stats_df(data)

rgb = color_df.set_index("face_shape")[["mean_r", "mean_g", "mean_b"]]
rgb.columns = ["Mean R", "Mean G", "Mean B"]
st.bar_chart(rgb)

brightness = color_df.set_index("face_shape")[["brightness"]]
brightness.columns = ["Brightness"]
st.line_chart(brightness)

st.caption(
    "Statistik warna pada notebook EDA dihitung dari sampel gambar per kelas."
)

st.divider()

section_title("Data Quality", "Duplicate dan pemeriksaan gambar bermasalah")

dup = data["duplicates"]
q1, q2, q3, q4 = st.columns(4)
q1.metric("Exact duplicate groups", dup["exact_duplicate_groups"])
q2.metric("Duplicate files", dup["duplicate_files"])
q3.metric("Cross-split leakage", dup["cross_split_leakage"])
q4.metric("Conflicting labels", dup["conflicting_duplicate_labels"])

quality = data["quality"]
q5, q6 = st.columns(2)
q5.metric("Images < 50 px", quality["images_under_50px"])
q6.metric("Extreme aspect ratio", quality["extreme_aspect_ratio"])

st.success(
    "Tidak ditemukan exact duplicate yang menyeberang dari training_set ke testing_set "
    "dan tidak ditemukan exact duplicate dengan label kelas yang berbeda."
)

st.markdown(
    """
    **Key findings**
    - Dataset awal berisi 1.312 gambar valid dan tidak ditemukan file corrupt.
    - Distribusi kelas relatif seimbang secara total.
    - Terdapat variasi resolusi yang besar.
    - Exact duplicate ditemukan di dalam dataset, tetapi tidak melintasi split.
    - Tidak ditemukan gambar yang sangat kecil atau aspect ratio ekstrem berdasarkan threshold EDA.
    """
)
