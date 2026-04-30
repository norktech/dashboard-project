import pandas as pd
from loguru import logger
from typing import Optional

def filter_books(
    df: pd.DataFrame,
    rating: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> pd.DataFrame:
    if df.empty:
        logger.warning("Empty dataframe received for filtering")
        return df

    filtered = df.copy()

    if rating and rating != "All":
        filtered = filtered[filtered["rating"] == rating]
        logger.info(f"Filter by rating '{rating}': {len(filtered)} books")

    if min_price is not None:
        filtered = filtered[filtered["price"] >= min_price]

    if max_price is not None:
        filtered = filtered[filtered["price"] <= max_price]

    logger.info(f"Price filter [{min_price}, {max_price}]: {len(filtered)} books")

    if filtered.empty:
        logger.warning("No books match the current filters")

    return filtered

def get_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total": 0,
            "average": 0.0,
            "min": 0.0,
            "max": 0.0,
            "last_scraped": "N/A"
        }

    avg = df["price"].mean()
    global_avg = df["price"].mean()

    return {
        "total": len(df),
        "average": round(avg, 2),
        "min": round(df["price"].min(), 2),
        "max": round(df["price"].max(), 2),
        "last_scraped": df["scraped_at"].max().strftime("%d/%m/%Y %H:%M"),
        "price_delta": round(avg - global_avg, 2)
    }

def get_rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["Rating", "Count"])
    return df["rating"].value_counts().reset_index().rename(
        columns={"rating": "Rating", "count": "Count"}
    )

def get_top_expensive(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return df.nlargest(n, "price")[["title", "price", "rating"]].reset_index(drop=True)

def get_price_trend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or len(df["scraped_at"].dt.date.unique()) < 2:
        logger.warning("Not enough data points for trend analysis")
        return pd.DataFrame(columns=["Date", "Average Price"])
    trend = df.groupby(df["scraped_at"].dt.date)["price"].mean().reset_index()
    trend.columns = ["Date", "Average Price"]
    trend["Average Price"] = trend["Average Price"].round(2)
    return trend

def get_price_histogram_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return df[["price"]].copy()