import streamlit as st
from loguru import logger
from dotenv import load_dotenv
import os

from app.data import load_books
from app.transform import (
    filter_books, get_kpis,
    get_rating_distribution, get_top_expensive,
    get_price_trend, get_price_histogram_data
)
from app.charts import (
    price_histogram, rating_pie,
    top_expensive_bar, price_trend_line
)

load_dotenv()

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title=os.getenv("APP_TITLE", "NorkTech Analytics"),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data(ttl=int(os.getenv("CACHE_TTL", 60)))
def get_data():
    return load_books()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("NorkTech")
st.sidebar.caption(f"v{os.getenv('APP_VERSION', '2.0.0')} — Book Price Analytics")
st.sidebar.divider()

try:
    df = get_data()

    if df.empty:
        st.error("No data found. Run the scraper first.")
        st.stop()

    # Filters
    st.sidebar.subheader("Filters")

    ratings = ["All"] + sorted(df["rating"].dropna().unique().tolist())
    selected_rating = st.sidebar.selectbox("Rating", ratings)

    min_price = float(df["price"].min())
    max_price = float(df["price"].max())
    price_range = st.sidebar.slider(
        "Price range (£)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=0.5
    )

    if st.sidebar.button("Refresh data"):
        st.cache_data.clear()
        st.rerun()

    # Apply filters
    filtered = filter_books(
        df,
        rating=selected_rating,
        min_price=price_range[0],
        max_price=price_range[1]
    )

    st.sidebar.divider()

    if filtered.empty:
        st.sidebar.warning("No books match the current filters.")
    else:
        st.sidebar.metric("Books found", len(filtered))
        st.sidebar.metric(
            "Last update",
            df["scraped_at"].max().strftime("%d/%m/%Y %H:%M")
        )

    # ── Header ────────────────────────────────────────────────
    st.title("NorkTech — Book Price Analytics")
    st.caption(f"Source: books.toscrape.com | {len(filtered)} books matching filters")
    st.divider()

    if filtered.empty:
        st.warning("No data matches the selected filters. Adjust the filters to see results.")
        st.stop()

    # ── KPIs ──────────────────────────────────────────────────
    kpis = get_kpis(filtered)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Books", kpis["total"])
    col2.metric("Average Price", f"£{kpis['average']}")
    col3.metric("Min Price", f"£{kpis['min']}")
    col4.metric("Max Price", f"£{kpis['max']}")

    st.divider()

    # ── Charts row 1 ──────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Price Distribution")
        st.plotly_chart(
            price_histogram(get_price_histogram_data(filtered)),
          
           )

    with col_right:
        st.subheader("Books by Rating")
        st.plotly_chart(
            rating_pie(get_rating_distribution(filtered)),
            use_container_width=True
        )

    # ── Charts row 2 ──────────────────────────────────────────
    st.subheader("Top 10 Most Expensive Books")
    st.plotly_chart(
        top_expensive_bar(get_top_expensive(filtered)),
        use_container_width=True
    )

    # ── Price trend ───────────────────────────────────────────
    st.subheader("Price Trend Over Time")
    trend_data = get_price_trend(filtered)
    if trend_data.empty:
        st.info("Not enough historical data for trend analysis. Run the scraper multiple times.")
    else:
        st.plotly_chart(
            price_trend_line(trend_data),
            use_container_width=True
        )

    # ── Raw data ──────────────────────────────────────────────
    st.subheader("Raw Data")
    with st.expander("Show raw data table"):
        st.dataframe(
            filtered[["title", "price", "rating", "scraped_at"]]
            .sort_values("price", ascending=False)
            .reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )

except FileNotFoundError as e:
    st.error(str(e))
    st.info("Make sure the scraper has been run at least once to generate the database.")
    logger.error(f"FileNotFoundError: {e}")

except Exception as e:
    st.error(f"Unexpected error: {e}")
    logger.exception(f"Unexpected error in dashboard: {e}")