import streamlit as st
import altair as alt

from utils.style import (
    apply_global_style,
    show_logo,
    show_sidebar_logo,
    page_header,
    section_title,
)

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
    "Key statistics and visualizations extracted from EDA_full.ipynb. "
    "The raw dataset does not need to be reloaded when the application runs.",
)

# =========================================================
# DATASET OVERVIEW
# =========================================================
section_title("Dataset Overview", "Dataset at a Glance")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Valid Images", f'{data["raw_total"]:,}')
m2.metric("Training Set", f'{data["train_total"]:,}')
m3.metric("Testing Set", f'{data["test_total"]:,}')
m4.metric("Corrupt Images", data["corrupt_images"])

st.caption(
    "All readable images in the EDA were recorded in RGB mode. "
    "Overall, the class distribution is relatively balanced."
)

st.divider()


# =========================================================
# SAMPLE IMAGES
# =========================================================
section_title(
    "Sample Images",
    "Examples from Each Face Shape Class"
)

st.image(
    "assets/samplephoto.jpg",
    caption="Sample images from the ovale, rectangular, round, and square classes.",
    use_container_width=True
)

st.caption(
    "These samples provide a visual overview of the facial characteristics "
    "represented by each class in the dataset."
)

st.divider()


# =========================================================
# CLASS DISTRIBUTION
# =========================================================
section_title(
    "Class Distribution",
    "Images per Face Shape"
)

class_df = class_distribution_df(data)

chart_df = class_df.melt(
    id_vars="face_shape",
    value_vars=["training", "testing"],
    var_name="Dataset",
    value_name="Count"
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
            "Count:Q",
            title="Number of Images",
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
            alt.Tooltip("Count:Q", title="Number of Images")
        ]
    )
    .properties(
        height=380,
        padding={
            "left": 0,
            "right": 30,
            "top": 30,
            "bottom": 0
        }
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

with st.expander("View Distribution Values"):

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
    **Insight:** The total number of images is relatively balanced across classes.
    However, the training and testing proportions are not identical for every class.
    """
)

st.divider()


# =========================================================
# IMAGE DIMENSIONS
# =========================================================
section_title(
    "Image Dimensions",
    "Image Resolution Characteristics"
)

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
        "Unique Resolutions",
        data["quality"]["unique_resolutions"]
    )

    st.caption(
        "The dataset contains a wide range of image resolutions, making image "
        "resizing an important preprocessing step before data is passed to the model."
    )


with right:
    st.markdown("**10 Most Common Resolutions**")

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
                title="Number of Images",
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
                    title="Count"
                )
            ]
        )
        .properties(
            width="container",
            height=300,
            padding={
                "left": 10,
                "right": 40,
                "top": 10,
                "bottom": 10
            }
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
        resolution_chart,
        use_container_width=True
    )

st.divider()


# =========================================================
# IMAGE FILE SIZE
# =========================================================
section_title(
    "Image File Size",
    "File Size Distribution and Outliers"
)

fs = data["file_size"]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Mean", f'{fs["mean_kb"]:.1f} KB')
c2.metric("Median", f'{fs["median_kb"]:.1f} KB')
c3.metric("Maximum", f'{fs["max_kb"]:,.1f} KB')
c4.metric("IQR Outliers", fs["iqr_outliers"])

st.write(
    "The image file size distribution is relatively wide. "
    "The median is much lower than the maximum value, indicating that several "
    "files are considerably larger than the majority of the dataset."
)

st.divider()


# =========================================================
# COLOR & BRIGHTNESS
# =========================================================
section_title(
    "Color & Brightness",
    "Average Color Characteristics"
)

color_df = color_stats_df(data)


# =========================================================
# RGB CHART
# =========================================================
rgb_chart_df = color_df.melt(
    id_vars="face_shape",
    value_vars=["mean_r", "mean_g", "mean_b"],
    var_name="Channel",
    value_name="Value"
)

rgb_chart = (
    alt.Chart(rgb_chart_df)
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
                labelFontSize=12,
                labelPadding=10
            )
        ),

        y=alt.Y(
            "Value:Q",
            title="Mean Pixel Value",
            axis=alt.Axis(
                labelColor="#BDB3A5",
                titleColor="#D8D0C5",
                gridColor="#2A241C",
                tickColor="#5A4932",
                domainColor="#5A4932"
            )
        ),

        color=alt.Color(
            "Channel:N",
            scale=alt.Scale(
                domain=["mean_r", "mean_g", "mean_b"],
                range=[
                    "#F1D89A",
                    "#C89F52",
                    "#8C693D"
                ]
            ),
            legend=alt.Legend(
                title=None,
                orient="bottom",
                labelColor="#D8D0C5"
            )
        ),

        tooltip=[
            alt.Tooltip(
                "face_shape:N",
                title="Face Shape"
            ),
            alt.Tooltip(
                "Channel:N",
                title="Channel"
            ),
            alt.Tooltip(
                "Value:Q",
                title="Mean Value",
                format=".1f"
            )
        ]
    )
    .properties(
        width="container",
        height=300,
        padding={
            "left": 10,
            "right": 30,
            "top": 20,
            "bottom": 10
        }
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
    rgb_chart,
    use_container_width=True
)


# =========================================================
# BRIGHTNESS CHART
# =========================================================
brightness_chart = (
    alt.Chart(color_df)
    .mark_line(
        color="#F1D89A",
        strokeWidth=3.5,
        point=alt.OverlayMarkDef(
            filled=True,
            fill="#F1D89A",
            stroke="#8C693D",
            strokeWidth=2,
            size=110
        )
    )
    .encode(
        x=alt.X(
            "face_shape:N",
            title=None,
            axis=alt.Axis(
                labelColor="#D8D0C5",
                labelFontSize=12,
                labelPadding=10
            )
        ),

        y=alt.Y(
            "brightness:Q",
            title="Mean Brightness",
            scale=alt.Scale(
                domain=[110, 121],
                zero=False
            ),
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
                "face_shape:N",
                title="Face Shape"
            ),
            alt.Tooltip(
                "brightness:Q",
                title="Brightness",
                format=".1f"
            )
        ]
    )
    .properties(
        width="container",
        height=260,
        padding={
            "left": 10,
            "right": 30,
            "top": 20,
            "bottom": 10
        }
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
    brightness_chart,
    use_container_width=True
)

st.caption(
    "The color statistics in the EDA notebook were calculated from image samples "
    "from each class."
)

st.divider()


# =========================================================
# DATA QUALITY
# =========================================================
section_title(
    "Data Quality",
    "Duplicate and Image Quality Checks"
)

dup = data["duplicates"]

q1, q2, q3, q4 = st.columns(4)

q1.metric(
    "Exact Duplicate Groups",
    dup["exact_duplicate_groups"]
)

q2.metric(
    "Duplicate Files",
    dup["duplicate_files"]
)

q3.metric(
    "Cross-Split Leakage",
    dup["cross_split_leakage"]
)

q4.metric(
    "Conflicting Labels",
    dup["conflicting_duplicate_labels"]
)

quality = data["quality"]

q5, q6 = st.columns(2)

q5.metric(
    "Images < 50 px",
    quality["images_under_50px"]
)

q6.metric(
    "Extreme Aspect Ratio",
    quality["extreme_aspect_ratio"]
)

st.success(
    "No exact duplicates were found crossing from the training set into the testing set, "
    "and no exact duplicates were found with conflicting class labels."
)

st.markdown(
    """
    **Key Findings**
    - The initial dataset contains 1,312 valid images with no corrupt files detected.
    - The overall class distribution is relatively balanced.
    - Image resolutions vary substantially across the dataset.
    - Exact duplicates exist within the dataset, but none cross between the training and testing splits.
    - No extremely small images or extreme aspect ratios were detected based on the EDA thresholds.
    """
)
