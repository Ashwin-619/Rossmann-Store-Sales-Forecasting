from contextlib import closing
import sqlite3
import numpy as np
import pandas as pd

DB_PATH = r"DB\Sales_data.db"


def _format_date(dt: str | pd.Timestamp) -> str:
    """Helper to convert inputs into YYYY-MM-DD string format."""
    return pd.to_datetime(dt).strftime("%Y-%m-%d")


def fetch_last_30d_sales(
    present_date: str | pd.Timestamp, store: int | str, db_path: str = DB_PATH
) -> dict:
    dt = pd.to_datetime(present_date)
    start_date = _format_date(dt - pd.Timedelta(days=36))
    end_date = _format_date(dt - pd.Timedelta(days=6))

    query = """
        SELECT Sales_date,Sales
        FROM Sales_Data
        WHERE Store = ?
          AND DATE(Sales_date) < ?
          AND DATE(Sales_date) >= ?
        ORDER BY Sales_date DESC;
    """
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (str(store), end_date, start_date))
        return dict((row[0].split()[0], row[1]) for row in cursor.fetchall())


def fetch_day_metrics(
    present_date: str | pd.Timestamp, store: int | str, db_path: str = DB_PATH
) -> dict :
    """Consolidates consecutive promo and holiday queries into one call."""
    dt = pd.to_datetime(present_date)
    yesterday = _format_date(dt - pd.Timedelta(days=1))
    query = """
        SELECT 
            consecutive_promo_days,
            consecutive_promo2_days,
            days_after_holiday,
            days_since_last_refurb
        FROM Sales_Data
        WHERE Store = ? AND DATE(Sales_date) = ?;
    """
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (str(store), yesterday))
        row = cursor.fetchone()

    if row is None:
        return {
            "consecutive_promo_days": np.nan,
            "consecutive_promo2_days": np.nan,
            "days_since_last_refurb": np.nan,
            "days_after_holiday":np.nan
            }

    return {
        "consecutive_promo_days": row[0],
        "consecutive_promo2_days": row[1],
        "days_after_holiday": row[2],
        "days_since_last_refurb": row[3]
    } 
        