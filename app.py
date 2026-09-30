from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parent / "Netflix.csv"

st.set_page_config(
    page_title="Netflix | Viewing Intelligence",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #202326;
        --muted: #72777c;
        --line: #e6e7e8;
        --paper: #f7f7f5;
        --surface: #ffffff;
        --accent: #d52232;
        --accent-soft: #fff0f1;
        --teal: #197d78;
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--paper); }
    [data-testid="stSidebar"] {
        background: #202326;
        border-right: 1px solid #34383b;
    }
    [data-testid="stSidebar"] * { color: #f5f5f3; }
    [data-testid="stSidebar"] label { color: #d2d4d5 !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #2b2f32;
        border-color: #484c4f;
    }
    .brand-mark {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 4px 0 30px;
        font: 400 25px 'Bebas Neue', sans-serif;
        letter-spacing: 1px;
        color: #e50914;
    }
    .brand-icon {
        display: grid;
        place-items: center;
        width: 30px;
        height: 34px;
        border-radius: 3px;
        background: linear-gradient(110deg, #b20710 0%, #e50914 48%, #b20710 100%);
        color: #fff;
        font: 700 23px 'Bebas Neue', sans-serif;
    }
    .eyebrow {
        color: var(--accent);
        font: 700 11px 'DM Sans', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin: 2px 0 8px;
    }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
    h1 { font-size: 32px !important; margin: 0 0 4px !important; }
    .subtitle { color: var(--muted); font-size: 14px; margin-bottom: 24px; }
    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 7px;
        padding: 16px 18px;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif; }
    [data-testid="stMetricDelta"] { color: var(--teal); }
    [data-testid="stTabs"] button { font-weight: 600; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 7px; }
    .section-label {
        font: 600 17px 'Space Grotesk', sans-serif;
        margin: 8px 0 2px;
    }
    .section-note { color: var(--muted); font-size: 12px; margin: 0 0 10px; }
    .spotlight {
        display: grid;
        grid-template-columns: 1fr auto;
        align-items: center;
        gap: 24px;
        margin: 22px 0 18px;
        padding: 22px 26px;
        border-left: 5px solid var(--accent);
        background-color: #202326;
        background-image: repeating-linear-gradient(135deg, transparent 0, transparent 15px, rgba(255,255,255,.025) 15px, rgba(255,255,255,.025) 16px);
        color: #f7f7f5;
    }
    .spotlight-kicker {
        color: #ff777e;
        font: 700 10px 'DM Sans', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 7px;
    }
    .spotlight h2 {
        color: #fff !important;
        font: 400 42px 'Bebas Neue', sans-serif !important;
        line-height: 1 !important;
        margin: 0 0 6px !important;
    }
    .spotlight-meta { color: #c2c5c6; font-size: 12px; }
    .spotlight-stat {
        min-width: 135px;
        padding-left: 22px;
        border-left: 1px solid #4b4e50;
    }
    .spotlight-stat span, .spotlight-stat small { display: block; color: #c2c5c6; font-size: 11px; }
    .spotlight-stat strong {
        display: block;
        color: #fff;
        font: 600 27px 'Space Grotesk', sans-serif;
        line-height: 1.25;
    }
    @media (max-width: 640px) {
        .spotlight { grid-template-columns: 1fr; gap: 15px; padding: 18px; }
        .spotlight h2 { font-size: 36px !important; }
        .spotlight-stat { min-width: 0; padding: 12px 0 0; border-left: 0; border-top: 1px solid #4b4e50; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
    for column in ("Rating", "Watch_Count", "Watch_Time_Minutes", "Monthly_Revenue"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data


if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH.name}. Place it beside app.py and restart the app.")
    st.stop()

data = load_data(str(DATA_PATH))
valid_dates = data["Watch_Date"].dropna()
if data.empty or valid_dates.empty:
    st.error("The dataset has no usable viewing records.")
    st.stop()

with st.sidebar:
    st.markdown(
        '<div class="brand-mark"><span class="brand-icon">N</span> NETFLIX</div>',
        unsafe_allow_html=True,
    )
    st.markdown("**FILTER THE VIEW**")
    date_range = st.date_input(
        "Watch date",
        value=(valid_dates.min().date(), valid_dates.max().date()),
        min_value=valid_dates.min().date(),
        max_value=valid_dates.max().date(),
    )
    regions = st.multiselect("Region", sorted(data["Region"].dropna().unique()), default=sorted(data["Region"].dropna().unique()))
    plans = st.multiselect(
        "Subscription plan",
        sorted(data["Subscription_Plan"].dropna().unique()),
        default=sorted(data["Subscription_Plan"].dropna().unique()),
    )
    categories = st.multiselect(
        "Category",
        sorted(data["Category"].dropna().unique()),
        default=sorted(data["Category"].dropna().unique()),
    )
    st.caption(f"{len(data):,} viewing records in the source")

filtered = data[
    data["Region"].isin(regions)
    & data["Subscription_Plan"].isin(plans)
    & data["Category"].isin(categories)
].copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["Watch_Date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date) + pd.Timedelta(days=1))
    ]

st.markdown('<div class="eyebrow">Audience &amp; content analytics</div>', unsafe_allow_html=True)
st.title("Viewing intelligence")
st.markdown('<div class="subtitle">A clear view of what audiences watch, where they watch, and what it earns.</div>', unsafe_allow_html=True)

if filtered.empty:
    st.info("No records match these filters. Adjust the date range or selections in the sidebar.")
    st.stop()

title_summary = (
    filtered.groupby(["Title", "Category", "Type"], as_index=False)
    .agg(Watches=("Watch_Count", "sum"), Avg_Rating=("Rating", "mean"))
    .sort_values("Watches", ascending=False)
)
if not title_summary.empty:
    audience_pick = title_summary.iloc[0]
    spotlight_title = escape(str(audience_pick["Title"]))
    spotlight_category = escape(str(audience_pick["Category"]))
    spotlight_type = escape(str(audience_pick["Type"]))
    spotlight_watches = f"{audience_pick['Watches']:,.0f}"
    recommendations = title_summary[title_summary["Title"].ne(audience_pick["Title"])].copy()
    same_category = recommendations["Category"].eq(audience_pick["Category"])
    same_format = recommendations["Type"].eq(audience_pick["Type"])
    rating_similarity = (
        1 - (recommendations["Avg_Rating"] - audience_pick["Avg_Rating"]).abs().div(4)
    ).clip(lower=0).fillna(0)
    recommendations["Similarity"] = (
        same_category.astype(int) * 3 + same_format.astype(int) * 2 + rating_similarity
    )
    recommendations["Match"] = "Closest audience rating"
    recommendations.loc[same_format, "Match"] = f"Same format / {audience_pick['Type']}"
    recommendations.loc[same_category, "Match"] = f"Same category / {audience_pick['Category']}"
    recommendations = recommendations.sort_values(
        ["Similarity", "Watches", "Title"], ascending=[False, False, True]
    ).head(3)
else:
    spotlight_title = "No title data"
    spotlight_category = ""
    spotlight_type = ""
    spotlight_watches = "0"
    recommendations = title_summary.copy()

st.markdown(
    f'<div class="spotlight"><div><div class="spotlight-kicker">01 / Audience pick</div>'
    f'<h2>{spotlight_title}</h2><div class="spotlight-meta">{spotlight_category} / {spotlight_type}</div></div>'
    f'<div class="spotlight-stat"><span>Watch count</span><strong>{spotlight_watches}</strong>'
    f'<small>in the current view</small></div></div>',
    unsafe_allow_html=True,
)

total_revenue = filtered["Monthly_Revenue"].sum()
total_watch_hours = filtered["Watch_Time_Minutes"].sum() / 60
average_rating = filtered["Rating"].mean()
customer_count = filtered["Customer_ID"].nunique()

metric_columns = st.columns(4)
metric_columns[0].metric("Customers", f"{customer_count:,}")
metric_columns[1].metric("Monthly revenue", f"₹{total_revenue:,.0f}")
metric_columns[2].metric("Watch time", f"{total_watch_hours:,.0f} hrs")
metric_columns[3].metric("Average rating", f"{average_rating:.1f} / 5" if pd.notna(average_rating) else "N/A")

overview_tab, content_tab, audience_tab, records_tab = st.tabs(
    ["Overview", "Content", "Audience", "Records"]
)

with overview_tab:
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="section-label">Viewing activity</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-note">Recorded watches by month</div>', unsafe_allow_html=True)
        monthly_views = (
            filtered.dropna(subset=["Watch_Date"])
            .assign(Month=lambda frame: frame["Watch_Date"].dt.to_period("M").astype(str))
            .groupby("Month")["Watch_Count"]
            .sum()
            .rename("Watches")
        )
        st.line_chart(monthly_views, color="#d52232", height=300)
    with right:
        st.markdown('<div class="section-label">Revenue by region</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-note">Monthly revenue total</div>', unsafe_allow_html=True)
        revenue_region = filtered.groupby("Region")["Monthly_Revenue"].sum().sort_values(ascending=False)
        st.bar_chart(revenue_region, color="#197d78", horizontal=True, height=300)

    lower_left, lower_right = st.columns(2)
    with lower_left:
        st.markdown('<div class="section-label">Subscription mix</div>', unsafe_allow_html=True)
        plan_mix = filtered.groupby("Subscription_Plan")["Customer_ID"].nunique().sort_values(ascending=False)
        st.bar_chart(plan_mix, color="#d52232", horizontal=True, height=240)
    with lower_right:
        st.markdown('<div class="section-label">Category engagement</div>', unsafe_allow_html=True)
        category_views = filtered.groupby("Category")["Watch_Count"].sum().sort_values(ascending=False)
        st.bar_chart(category_views, color="#197d78", horizontal=True, height=240)

with content_tab:
    top_titles = title_summary[["Title", "Category", "Watches", "Avg_Rating"]].head(10)
    if not recommendations.empty:
        st.markdown('<div class="section-label">More like ' + escape(str(audience_pick["Title"])) + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-note">Picked from matching categories, formats, and audience ratings</div>', unsafe_allow_html=True)
        recommendation_columns = st.columns(min(3, len(recommendations)))
        for rank, (_, recommendation) in enumerate(recommendations.iterrows(), start=1):
            with recommendation_columns[rank - 1]:
                with st.container(border=True):
                    st.caption(f"MATCH 0{rank} / {recommendation['Match']}")
                    st.subheader(recommendation["Title"])
                    st.markdown(f"**{recommendation['Watches']:,.0f}** recorded watches")
                    st.caption(f"{recommendation['Category']} / {recommendation['Type']}")
    st.markdown('<div class="section-label">Most-watched titles</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-note">Top 10 by recorded watch count</div>', unsafe_allow_html=True)
    st.bar_chart(top_titles.set_index("Title")["Watches"], color="#d52232", horizontal=True, height=360)
    st.dataframe(
        top_titles.assign(Avg_Rating=top_titles["Avg_Rating"].round(1)),
        hide_index=True,
        width="stretch",
    )

with audience_tab:
    device_column, language_column, payment_column = st.columns(3)
    with device_column:
        st.markdown('<div class="section-label">Devices</div>', unsafe_allow_html=True)
        st.bar_chart(filtered["Device"].value_counts(), color="#197d78", horizontal=True, height=280)
    with language_column:
        st.markdown('<div class="section-label">Audio languages</div>', unsafe_allow_html=True)
        st.bar_chart(filtered["Language"].value_counts().head(8), color="#d52232", horizontal=True, height=280)
    with payment_column:
        st.markdown('<div class="section-label">Payment methods</div>', unsafe_allow_html=True)
        st.bar_chart(filtered["Payment_Method"].value_counts(), color="#197d78", horizontal=True, height=280)

with records_tab:
    st.markdown('<div class="section-label">Filtered viewing records</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-note">{len(filtered):,} records match the selected filters</div>', unsafe_allow_html=True)
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button(
        "Download filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="viewing_records.csv",
        mime="text/csv",
        icon="⬇️",
    )