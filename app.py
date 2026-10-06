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
regular = df[~df["secret"]].copy()

# Metrics calculations
owned = int(regular["own"].sum())
total = len(regular)
remaining = total - owned
completion = (owned / total) if total else 0

series_stats = (
    regular.groupby("series", sort=False)
    .agg(collected=("own", "sum"), total=("own", "size"))
    .reset_index()
)
series_stats["percent"] = (series_stats["collected"] / series_stats["total"]) * 100
series_complete = int((series_stats["percent"] == 100).sum())

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

    /* Ensure Streamlit header is transparent so the reopen-sidebar arrow is visible */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    /* Centered, compact title */
    .main-title {
        text-align: center;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        color: #2b3a2f;
        margin-bottom: 0.75rem;
    }

    /* Series section headings */
    .series-heading {
        font-size: 1.05rem;
        font-weight: 750;
        color: #314434;
        margin-top: 1.2rem;
        margin-bottom: 0.4rem;
        border-bottom: 1.5px solid #d4e2be;
        padding-bottom: 0.2rem;
    }

    /* Metric cards */
    .metric-container {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid #d4e2be;
        border-radius: 9px;
        padding: 0.4rem 0.6rem;
        text-align: center;
        backdrop-filter: blur(4px);
    }
    .metric-val {
        font-size: 1.25rem;
        font-weight: 800;
        color: #2e3e2b;
        line-height: 1.1;
    }
    .metric-lbl {
        font-size: 0.62rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #5c7457;
        margin-top: 2px;
    }

    /* Compact grid per series */
    .figure-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(88px, 1fr));
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Individual figure card */
    .smiski-chip {
        position: relative;
        background: #ffffff;
        border: 1px solid #dbe6cb;
        border-radius: 8px;
        padding: 0.35rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        text-align: center;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .smiski-chip:hover {
        box-shadow: 0 4px 10px rgba(138, 179, 78, 0.3);
        border-color: #9fcc5f;
        transform: translateY(-2px);
    }
    .smiski-chip.missing {
        background: rgba(255, 255, 255, 0.45);
        border-color: #dbe6cb;
    }
    .smiski-thumb {
        width: 100%;
        height: 72px;
        object-fit: contain;
    }
    .figure-caption {
        font-size: 0.63rem;
        font-weight: 600;
        line-height: 1.15;
        margin-top: 0.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
        color: #2b3a2f;
    }
    .badge-dot {
        height: 6px;
        width: 6px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 3px;
    }
    .badge-dot.owned {
        background-color: #7bb547;
    }
    .badge-dot.missing {
        background-color: #b0b7a8;
    }
    .badge-row {
        display: flex;
        align-items: center;
        font-size: 0.58rem;
        font-weight: 600;
        color: #637565;
        margin-top: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# filters
with st.sidebar:
    st.markdown("### 🔍 Filters")
    all_series_list = ["All Series"] + list(df["series"].drop_duplicates())
    selected_series = st.selectbox("Series", all_series_list)
    show_status = st.radio(
        "Display Status",
        ["All", "Collected Only", "Missing Only"],
        horizontal=True,
    )

    st.markdown("---")
    st.markdown("### 📊 Progress Tracker")
    for _, row in series_stats.iterrows():
        pct = row["percent"] / 100
        st.write(f"**{row['series']}** ({row['collected']}/{row['total']})")
        st.progress(pct)

    st.markdown("---")
    st.caption("✨ Secret figures are not represented.")
    st.caption("Destiny Brewington • [GitHub](https://github.com/destinykb)")

# dash
st.markdown('<div class="main-title">Destiny\'s Smiski Collection</div>', unsafe_allow_html=True)

# Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{owned} <span style="font-size:0.85rem; color:#6b7d6c;">/ {total}</span></div><div class="metric-lbl">Collected</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{completion:.0%}</div><div class="metric-lbl">Progress</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{remaining}</div><div class="metric-lbl">Missing</div></div>',
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{series_complete}</div><div class="metric-lbl">Series Complete</div></div>',
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

# Display figures organized by series
series_order = (
    [selected_series]
    if selected_series != "All Series"
    else list(df["series"].drop_duplicates())
)

for series_name in series_order:
    series_group = display_df[display_df["series"] == series_name]
    if series_group.empty:
        continue

    # series headers
    clean_series_name = str(series_name).replace('"', '&quot;')
    st.markdown(f'<div class="series-heading">{clean_series_name}</div>', unsafe_allow_html=True)

    # cards
    card_html_list = []
    for _, row in series_group.iterrows():
        is_owned = bool(row["own"])
        img = row["image"] if pd.notna(row["image"]) else ""
        name = str(row["name"]).replace('"', '&quot;')

        opacity = "1.0" if is_owned else "0.22"
        grayscale = "grayscale(0%)" if is_owned else "grayscale(100%)"
        card_class = "smiski-chip" if is_owned else "smiski-chip missing"
        dot_class = "owned" if is_owned else "missing"
        status_text = "Owned" if is_owned else "Needed"

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