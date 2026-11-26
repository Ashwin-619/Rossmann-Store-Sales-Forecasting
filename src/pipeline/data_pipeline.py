from pathlib import Path
from typing import Union
import pandas as pd
import numpy as np

from src.schema.input_data import InputFeatures
from src.database.fetch_past_values import fetch_last_30d_sales, fetch_day_metrics
from src.pipeline.create_lag_rolling_features import create_rolling_and_lags

DEFAULT_DB_PATH = "DB/Sales_data.db"


class FeaturePipeline:
    def __init__(self, db_path: Union[Path, str] = DEFAULT_DB_PATH):
        self.db_path = str(db_path)

    def transform(self, raw_payload: InputFeatures) -> pd.DataFrame:
        # 1. Base payload features
        base_features = raw_payload.model_dump(mode="python")

        # 2. Fetch history and build time-series features
        sales_history = fetch_last_30d_sales(
            present_date=raw_payload.Date.isoformat(),
            store=raw_payload.Store,
            db_path=self.db_path,
        )
        time_series_features = create_rolling_and_lags(last_30d_sales=sales_history,present_date=raw_payload.Date.isoformat())


        # Safe fetch for day metrics
        day_metrics = fetch_day_metrics(
            present_date=raw_payload.Date.isoformat(),
            store=raw_payload.Store,
            db_path=self.db_path,
        )

         # conditional day metrics fetch 

        if day_metrics is not None:
         
            if base_features["Is_Promo_Active"] == 0 :
                day_metrics["consecutive_promo_days"] = 0
            else:
                day_metrics["consecutive_promo_days"] +=1

            if base_features["Is_Promo2_Active"] == 0 :
                day_metrics["consecutive_promo2_days"] = 0
            else:
                day_metrics["consecutive_promo2_days"] +=1

            if base_features["School_holiday"] == 1 :
                day_metrics["days_till_next_holiday"] = 0
                day_metrics["days_after_holiday"] = 0
            else:                
                day_metrics["days_after_holiday"] += 1                    

        # 3. Combine into single-row DataFrame
        full_feature_dict = {
            **base_features, 
            **day_metrics, 
            **time_series_features
        }
        df = pd.DataFrame([full_feature_dict])

        # 4. Extract calendar features before dropping Date
        if "Date" in df.columns:
            df = df.drop(columns=["Date"])
        if "Next_holiday" in df.columns:
            df = df.drop(columns=["Next_holiday"])

        # 5. Map feature names to training signatures
        column_mapping = {
            "Is_Promo_Active": "Promo",
            "School_holiday": "SchoolHoliday",
            "Storetype": "StoreType",
            "Competition_Distance": "CompetitionDistance",
            "lag_7": "7th_lag",
            "lag_14": "14th_lag",
            "lag_21": "21st_lag",
            "lag_28": "28th_lag",
            "lag_diff": "7_8_lag_dif",
            "ma_3d": "ma_3d_lag7",
            "std_3d": "std_3d_lag7",
            "ma_7d": "ma_7d_lag7",
            "ma_15d": "ma_15d_lag7",
            "ma_30d": "ma_30d_lag7",
        }
        df = df.rename(columns=column_mapping)

        if "Promo2" in df.columns:
            df["Is_Promo2_Active"] = df["Promo2"]

        # 6. Categorical Handling: Convert floats (1.0) to clean int/string categories
        # Force uniform string categories across all categorical columns
        categorical_cols = [
            'Store', 'DayOfWeek', 'month', 'StoreType', 'Assortment',
            'promo_x_dayofweek', 'promo_x_storetype', 'promo2_x_dayofweek', 'promo2_x_storetype'
        ]

        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).astype("category")

        # 7. Quantitative Handling: Force standard numpy float64/int64 (no Float64/Int64)
        float_cols = [
            'CompetitionDistance', 'days_since_last_refurb', '7th_lag', '14th_lag',
            '21st_lag', '28th_lag', 'avg_last_3_weeks', 'ma_3d_lag7', 'std_3d_lag7',
            'ma_7d_lag7', 'ma_15d_lag7', 'ma_30d_lag7', '7_8_lag_dif', 'days_till_next_holiday',
            'days_after_holiday'
        ]
        for col in float_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).astype(float)

        int_cols = [
            'Sales', 'Customers', 'SchoolHoliday', 'day', 'consecutive_promo_days','Promo',
            'Is_Promo2_Active', 'consecutive_promo2_days'
        ]
        for col in int_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)      

        return df

