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

# layout
st.markdown(
    """
    <style>
    /* Reduce Streamlit container padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 0.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    header[data-testid="stHeader"] {
        display: none;
    }

    /* Header Bar */
    .dash-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid rgba(0,0,0,0.06);
        padding-bottom: 0.4rem;
    }
    .dash-title {
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #2b3a2f;
        margin: 0;
    }
    .dash-subtitle {
        color: #7b8e7e;
        font-size: 0.85rem;
    }

    /* Metric pill cards */
    .metric-container {
        background: #f4f7ee;
        border: 1px solid #dce8ca;
        border-radius: 10px;
        padding: 0.45rem 0.8rem;
        text-align: center;
        transition: transform 0.15s ease-in-out;
    }
    .metric-container:hover {
        transform: translateY(-2px);
    }
    .metric-val {
        font-size: 1.35rem;
        font-weight: 800;
        color: #3b503d;
        line-height: 1.1;
    }
    .metric-lbl {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #718873;
        margin-top: 2px;
    }

    /* Grid Display */
    .figure-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(88px, 1fr));
        gap: 0.5rem;
        margin-top: 0.6rem;
        max-height: 72vh;
        overflow-y: auto;
        padding-right: 4px;
    }

    /* Compact Figure Card */
    .smiski-chip {
        position: relative;
        background: #ffffff;
        border: 1px solid #e7ede2;
        border-radius: 8px;
        padding: 0.35rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        text-align: center;
        transition: all 0.2s ease;
    }
    .smiski-chip:hover {
        box-shadow: 0 4px 12px rgba(186, 219, 114, 0.25);
        border-color: #badb72;
        transform: translateY(-1px);
        z-index: 2;
    }
    .smiski-chip.missing {
        background: #fbfbfb;
        border-color: #ededed;
    }
    .smiski-thumb {
        width: 100%;
        height: 70px;
        object-fit: contain;
        transition: filter 0.2s ease, opacity 0.2s ease;
    }
    .figure-caption {
        font-size: 0.65rem;
        font-weight: 600;
        line-height: 1.1;
        margin-top: 0.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
        color: #333;
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
        box-shadow: 0 0 5px #a6df74;
    }
    .badge-dot.missing {
        background-color: #d1d5db;
    }
    .badge-row {
        display: flex;
        align-items: center;
        font-size: 0.6rem;
        font-weight: 600;
        color: #777;
        margin-top: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# filters
with st.sidebar:
    st.markdown("### Filters")
    all_series_list = ["All Series"] + list(df["series"].drop_duplicates())
    selected_series = st.selectbox("Series", all_series_list)
    show_status = st.radio("Display Status", ["All", "Collected Only", "Missing Only"], horizontal=True)

    st.markdown("---")
    st.markdown("### Series Breakdown")
    for _, row in series_stats.iterrows():
        pct = row["percent"] / 100
        st.write(f"**{row['series']}** ({row['collected']}/{row['total']})")
        st.progress(pct)

    st.markdown("---")
    st.caption("Secret figures are excluded.")
    st.caption("Destiny Brewington • [GitHub](https://github.com/destinykb)")

# dash
st.markdown(
    """
    <div class="dash-header">
        <div>
            <span class="dash-title">SMISKI COLLECTION</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Top KPI row (compact)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        f'<div class="metric-container"><div class="metric-val">{owned} <span style="font-size:0.9rem; color:#888;">/ {total}</span></div><div class="metric-lbl">Collected</div></div>',
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
        f'<div class="metric-container"><div class="metric-val">{series_complete}</div><div class="metric-lbl">Series Completed</div></div>',
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

# Render compact grid
card_html_list = []
for _, row in display_df.iterrows():
    is_owned = bool(row["own"])
    img = row["image"] if pd.notna(row["image"]) else ""
    name = str(row["name"]).replace('"', '&quot;')
    series = str(row["series"]).replace('"', '&quot;')

    opacity = "1.0" if is_owned else "0.22"
    grayscale = "grayscale(0%)" if is_owned else "grayscale(100%)"
    card_class = "smiski-chip" if is_owned else "smiski-chip missing"
    dot_class = "owned" if is_owned else "missing"
    status_text = "Owned" if is_owned else "Needed"

    # Single-line string prevents Streamlit from interpreting indentation as a code block
    card_html = (
        f'<div class="{card_class}" title="{name} ({series})">'
        f'<img class="smiski-thumb" src="{img}" style="opacity:{opacity}; filter:{grayscale};" loading="lazy" />'
        f'<div class="figure-caption">{name}</div>'
        f'<div class="badge-row"><span class="badge-dot {dot_class}"></span>{status_text}</div>'
        f'</div>'
    )
    card_html_list.append(card_html)

grid_wrapper = f'<div class="figure-grid">{"".join(card_html_list)}</div>'
st.markdown(grid_wrapper, unsafe_allow_html=True)

# app is deployed on following link
# https://destinys-smiski-collection.streamlit.app/