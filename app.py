import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Destiny's Smiski Collection",
    page_icon="💚",
    layout="wide",
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

owned = int(regular["own"].sum())
total = len(regular)
remaining = total - owned
completion = owned / total if total else 0

series_stats = (
    regular.groupby("series", sort=False)
    .agg(collected=("own", "sum"), total=("own", "size"))
    .reset_index()
)
series_stats["percent"] = series_stats["collected"] / series_stats["total"] * 100

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #777;
        margin-top: 0.25rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        text-align: center;
        padding: 1rem 0.5rem;
        border-radius: 14px;
        background: #dae586;
    }
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        color: #777;
        font-size: 0.9rem;
    }
    .smiski-card {
        text-align: center;
        padding: 0.6rem;
        border-radius: 14px;
        background: #fafafa;
        margin-bottom: 1rem;
    }
    .smiski-name {
        font-size: 0.9rem;
        min-height: 2.5rem;
        margin-top: 0.3rem;
    }
    .owned-label {
        color: #6c8b72;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .missing-label {
        color: #aaa;
        font-size: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">MY SMISKI COLLECTION</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A visual record of my current Smiski collection! </div>',
    unsafe_allow_html=True,
)

# Overview metrics
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-number">{owned} / {total}</div>'
        f'<div class="metric-label">COLLECTED</div></div>',
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-number">{completion:.0%}</div>'
        f'<div class="metric-label">COLLECTION COMPLETE</div></div>',
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-number">{remaining}</div>'
        f'<div class="metric-label">STILL MISSING</div></div>',
        unsafe_allow_html=True,
    )

with c4:
    half_or_more = int((series_stats["percent"] >= 50).sum())
    st.markdown(
        f'<div class="metric-card"><div class="metric-number">{half_or_more}</div>'
        f'<div class="metric-label">SERIES ≥ 50%</div></div>',
        unsafe_allow_html=True,
    )

st.divider()

# Filters
left, right = st.columns([2, 1])

with left:
    selected_series = st.selectbox(
        "View series",
        ["All Series"] + list(df["series"].drop_duplicates()),
    )

with right:
    show = st.selectbox(
        "Show",
        ["All", "Collected", "Missing"],
    )

display_df = regular.copy()

if selected_series != "All Series":
    display_df = display_df[display_df["series"] == selected_series]

if show == "Collected":
    display_df = display_df[display_df["own"]]
elif show == "Missing":
    display_df = display_df[~display_df["own"]]

# Figurine gallery
current_series = (
    [selected_series]
    if selected_series != "All Series"
    else list(df["series"].drop_duplicates())
)

for series in current_series:
    series_df = display_df[display_df["series"] == series]

    if series_df.empty:
        continue

    st.subheader(series)

    cols = st.columns(6)

    for i, (_, row) in enumerate(series_df.iterrows()):
        with cols[i % 6]:
            image_url = row["image"]

            if pd.notna(image_url) and image_url:
                # dim missing figures.
                opacity = "1" if row["own"] else "0.25"
                grayscale = "grayscale(0%)" if row["own"] else "grayscale(100%)"

                st.markdown(
                    f"""
                    <div class="smiski-card">
                        <img src="{image_url}"
                             style="width:100%; height:170px; object-fit:contain;
                                    opacity:{opacity}; filter:{grayscale};">
                        <div class="smiski-name">{row["name"]}</div>
                        <div class="{'owned-label' if row['own'] else 'missing-label'}">
                            {'✓ COLLECTED' if row['own'] else '○ MISSING'}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# Secrets
st.divider()
st.subheader("Notes")
st.caption(
    "Secret figures are not represented."
)

st.caption(
    "Image sources: Smiski official product image URLs."
)

st.caption(
    "Destiny Brewington"
)

st.caption(
    "https://github.com/destinykb"
)