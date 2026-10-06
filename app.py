import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Destiny's Smiski Collection",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = "smiski_collection_data.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["own"] = df["own"].astype(bool)
    df["secret"] = df["secret"].astype(bool)
    return df


df = load_data()

# Exclude secret figures
regular = df[~df["secret"]].copy()
is_moving_series = regular["series"].str.contains("Moving", case=False, na=False)
is_smiski_question = regular["name"].str.strip().str.startswith("Smiski?")
regular = regular[~(is_moving_series & is_smiski_question)].copy()

# Metrics calculations
owned = int(regular["own"].sum())
total = len(regular)
completion = (owned / total) if total else 0

series_stats = (
    regular.groupby("series", sort=False)
    .agg(collected=("own", "sum"), total=("own", "size"))
    .reset_index()
)
series_stats["percent"] = (series_stats["collected"] / series_stats["total"]) * 100
series_half_or_more = int((series_stats["percent"] >= 50).sum())
total_series = len(series_stats)

# Custom CSS
st.markdown(
    """
    <style>
    /* Smiski soft green background */
    .stApp {
        background-color: #edf4de;
    }
    section[data-testid="stSidebar"] {
        background-color: #e2eccb;
    }

    /* Keep Streamlit header transparent so the sidebar toggle arrow is accessible */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Container padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 100%;
    }

    /* Centered, bold Dark Green page title & subtitle */
    .main-title {
        text-align: center;
        font-size: 1.85rem;
        font-weight: 850;
        letter-spacing: -0.01em;
        color: #1b3823;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        text-align: center;
        font-size: 0.92rem;
        font-weight: 600;
        color: #3b563f;
        margin-bottom: 1.4rem;
    }
    .main-subtitle a {
        color: #1b3823;
        text-decoration: underline;
        text-underline-offset: 2px;
        transition: color 0.15s ease;
    }
    .main-subtitle a:hover {
        color: #4b7b30;
    }

    /* Dark Green series section headings */
    .series-heading {
        font-size: 1.25rem;
        font-weight: 800;
        color: #1b3823;
        margin-top: 1.8rem;
        margin-bottom: 0.75rem;
        border-bottom: 2px solid #b7cc9e;
        padding-bottom: 0.35rem;
    }

    /* Metric cards (3 evenly distributed columns) */
    .metric-container {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid #d4e2be;
        border-radius: 10px;
        padding: 0.65rem 0.8rem;
        text-align: center;
        backdrop-filter: blur(4px);
    }
    .metric-val {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1b3823;
        line-height: 1.1;
    }
    .metric-lbl {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #4a634e;
        margin-top: 3px;
    }

    /* Dark Green Progress Bars in Sidebar */
    div[data-testid="stProgressBar"] > div {
        background-color: #c9dbb3 !important; /* progress track background */
        border-radius: 6px;
    }
    div[data-testid="stProgressBar"] div[role="progressbar"],
    div[data-testid="stProgressBar"] div[data-testid="stProgressValue"],
    div[data-testid="stProgressBar"] > div > div {
        background-color: #1b3823 !important; /* fill color */
        border-radius: 6px;
    }

    /* Full-width responsive grid */
    .figure-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 0.9rem;
        width: 100%;
        margin-bottom: 1rem;
    }

    /* Larger Figure Card */
    .smiski-chip {
        position: relative;
        background: #ffffff;
        border: 1.5px solid #dbe6cb;
        border-radius: 12px;
        padding: 0.8rem 0.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .smiski-chip:hover {
        box-shadow: 0 6px 14px rgba(138, 179, 78, 0.32);
        border-color: #8ebb27;
        transform: translateY(-3px);
    }
    .smiski-chip.missing {
        background: rgba(255, 255, 255, 0.5);
        border-color: #dbe6cb;
    }
    .smiski-thumb {
        width: 100%;
        height: 160px;
        object-fit: contain;
    }
    .figure-caption {
        font-size: 0.78rem;
        font-weight: 700;
        line-height: 1.25;
        margin-top: 0.5rem;
        color: #1b3823;
        word-break: break-word;
    }
    .badge-dot {
        height: 7px;
        width: 7px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 4px;
    }
    .badge-dot.owned {
        background-color: #6da739;
    }
    .badge-dot.missing {
        background-color: #b0b7a8;
    }
    .badge-row {
        display: flex;
        align-items: center;
        font-size: 0.68rem;
        font-weight: 600;
        color: #556956;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Filters
with st.sidebar:
    st.markdown("### Filters")
    all_series_list = ["All Series"] + list(regular["series"].drop_duplicates())
    selected_series = st.selectbox("Series", all_series_list)
    show_status = st.radio(
        "Display Status",
        ["All", "Collected Only", "Missing Only"],
        horizontal=True,
    )

    st.markdown("---")
    st.markdown("### Progress")
    for _, row in series_stats.iterrows():
        pct = row["percent"] / 100
        st.write(f"**{row['series']}** ({row['collected']}/{row['total']})")
        st.progress(pct)

    st.markdown("---")
    st.caption("Secret figures are not represented.")

# Dashboard Title
st.markdown('<div class="main-title">Destiny\'s Smiski Collection</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="main-subtitle">Destiny Brewington • <a href="https://github.com/destinykb" target="_blank">GitHub</a></div>',
    unsafe_allow_html=True,
)

# 3-Column Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{owned} <span style="font-size:0.9rem; color:#6b7d6c;">/ {total}</span></div><div class="metric-lbl">Collected</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{completion:.0%}</div><div class="metric-lbl">Progress</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{series_half_or_more} <span style="font-size:0.9rem; color:#6b7d6c;">/ {total_series}</span></div><div class="metric-lbl">Series ≥ 50% Collected</div></div>',
        unsafe_allow_html=True,
    )

# Filter dataset
display_df = regular.copy()
if selected_series != "All Series":
    display_df = display_df[display_df["series"] == selected_series]

if show_status == "Collected Only":
    display_df = display_df[display_df["own"]]
elif show_status == "Missing Only":
    display_df = display_df[~display_df["own"]]

# Display figures by series
series_order = (
    [selected_series]
    if selected_series != "All Series"
    else list(regular["series"].drop_duplicates())
)

for series_name in series_order:
    series_group = display_df[display_df["series"] == series_name]
    if series_group.empty:
        continue

    # Series
    clean_series_name = str(series_name).replace('"', '&quot;')
    st.markdown(f'<div class="series-heading">{clean_series_name}</div>', unsafe_allow_html=True)

    # Cards
    card_html_list = []
    for _, row in series_group.iterrows():
        is_owned = bool(row["own"])
        img = row["image"] if pd.notna(row["image"]) else ""
        name = str(row["name"]).replace('"', '&quot;')

        opacity = "1.0" if is_owned else "0.22"
        grayscale = "grayscale(0%)" if is_owned else "grayscale(100%)"
        card_class = "smiski-chip" if is_owned else "smiski-chip missing"
        dot_class = "owned" if is_owned else "missing"
        status_text = "Own" if is_owned else "Missing"

        card_html = (
            f'<div class="{card_class}" title="{name}">'
            f'<img class="smiski-thumb" src="{img}" style="opacity:{opacity}; filter:{grayscale};" loading="lazy" />'
            f'<div class="figure-caption">{name}</div>'
            f'<div class="badge-row"><span class="badge-dot {dot_class}"></span>{status_text}</div>'
            f'</div>'
        )
        card_html_list.append(card_html)

    grid_markup = f'<div class="figure-grid">{"".join(card_html_list)}</div>'
    st.markdown(grid_markup, unsafe_allow_html=True)

# app is deployed on following link
# https://destinys-smiski-collection.streamlit.app/