import numpy as np
import pandas as pd
from src.database.fetch_past_values import _format_date

def create_rolling_and_lags(
    last_30d_sales: dict,present_date: str | pd.Timestamp = "2015-08-01"
) -> dict | pd.DataFrame:
    """Calculates lag, rolling, and momentum metrics from a DESC-ordered array.
    Index 0 is the most recent historical day.
    """

    present_date = pd.to_datetime(present_date)
    if last_30d_sales is None or len(last_30d_sales) == 0:
        return {}

    arr_len = len(last_30d_sales)

    # Safe indexing helper to avoid IndexError
    def safe_get(lag_idx: int) -> float:
        lag_date=  _format_date(present_date - pd.Timedelta(days=lag_idx))
        return float(last_30d_sales.get(lag_date, np.nan))

    # Safe mean helper
    def safe_mean(n):
        if n <= arr_len:
            return np.round(np.mean(list(last_30d_sales.values())[:n]), 2)
        else:
            return np.round(np.mean(list(last_30d_sales.values())), 2)
       

    # 1. Lags (Targeting exact offset days)
    lag_7 = safe_get(7)  # 7th day back
    lag_14 = safe_get(14)  # 14th day back
    lag_21 = safe_get(21)  # 21st day back
    lag_28 = safe_get(28)  # 28th day back

    # 2. Lag Difference (Day 7 vs Day 8)
    lag_8 = safe_get(8)
    lag_diff = (
        np.round(lag_7 - lag_8, 2)
        if not (np.isnan(lag_7) or np.isnan(lag_8))
        else np.nan
    )

    # 3. Weekly Average (7-day intervals)
    weekly_lags = [lag_7, lag_14, lag_21]
    avg_last_3_weeks = (
        np.round(np.nanmean(weekly_lags), 2)
        if not all(np.isnan(weekly_lags))
        else np.nan
    )

    # 4. Moving Averages & Volatility
    features = {
        "lag_7": lag_7,
        "lag_14": lag_14,
        "lag_21": lag_21,
        "lag_28": lag_28,
        "lag_diff": lag_diff,
        "avg_last_3_weeks": avg_last_3_weeks,
        "std_3d": (
            np.round(np.std(list(last_30d_sales.values())[:3], ddof=1), 2)
        ),
        "ma_3d": safe_mean(3),
        "ma_7d": safe_mean(7),
        "ma_15d": safe_mean(15),
        "ma_30d": safe_mean(30),
    }

    return features