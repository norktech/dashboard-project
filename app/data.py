import sqlite3
import pandas as pd
from loguru import logger
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "../scraper-project/books.db")

def get_connection() -> sqlite3.Connection:
    db_path = Path(DATABASE_PATH)
    if not db_path.exists():
        logger.error(f"Database not found at: {db_path.resolve()}")
        raise FileNotFoundError(f"Database not found: {db_path.resolve()}")
    try:
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to database: {db_path.resolve()}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def load_books() -> pd.DataFrame:
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM books", conn)
        conn.close()

        if df.empty:
            logger.warning("No data found in books table")
            return pd.DataFrame()

        # Sanitize data
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["rating"] = df["rating"].astype(str).str.strip()
        df["title"] = df["title"].astype(str).str.strip()
        df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")

        # Drop invalid rows
        before = len(df)
        df = df.dropna(subset=["price", "scraped_at"])
        after = len(df)

        if before != after:
            logger.warning(f"Dropped {before - after} invalid rows")

        logger.success(f"Loaded {len(df)} valid books from database")
        return df

    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error loading books: {e}")
        raise