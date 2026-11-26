import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Union

DEFAULT_DB_PATH = "DB/Sales_data.db"


def inference_to_main(data_dict: dict, db_path: Union[Path, str] = DEFAULT_DB_PATH) -> dict:
    """
    Transfers prediction feature data from the `inference_results` table along with the
    actual Sales and Customers numbers into the primary `Sales_Data` SQLite database table.

    data_dict structure:
        {
            "Store": int,
            "Date": str or date,
            "Sales": int,
            "Customers": int
        }
    """
    db_path = str(db_path)
    store = data_dict.get("Store")
    date_val = str(data_dict.get("Date"))
    actual_sales = data_dict.get("Sales")
    actual_customers = data_dict.get("Customers")

    with closing(sqlite3.connect(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query inference_results for precomputed features matching Store and Date
        select_query = """
            SELECT * FROM inference_results
            WHERE Store = ? AND (Date = ? OR DATE(Date) = DATE(?));
        """
        cursor.execute(select_query, (store, date_val, date_val))
        row = cursor.fetchone()

        if not row:
            return {"message": f"No inference record found for Store {store} on Date {date_val}."}

        row_dict = dict(row)

        insert_query = """
            INSERT INTO Sales_Data (
                Sales_date, Store, DayOfWeek, Sales, Customers, Promo, SchoolHoliday, month, day,
                StoreType, Assortment, CompetitionDistance, Promo2, consecutive_promo_days,
                days_since_last_refurb, "7th_lag", "14th_lag", "21st_lag", "28th_lag", avg_last_3_weeks,
                ma_3d_lag7, std_3d_lag7, ma_7d_lag7, ma_15d_lag7, ma_30d_lag7, "7_8_lag_dif",
                Is_Promo2_Active, consecutive_promo2_days, promo_x_dayofweek,
                promo_x_storetype, promo2_x_dayofweek, promo2_x_storetype,
                days_till_next_holiday, days_after_holiday
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?
            );
        """

        sales_date = date_val
        store_val = str(row_dict.get("Store"))
        day_of_week = str(row_dict.get("DayOfWeek"))
        promo = row_dict.get("Promo")
        school_holiday = row_dict.get("SchoolHoliday")
        month = row_dict.get("month")
        day = row_dict.get("day")
        store_type = row_dict.get("StoreType")
        assortment = row_dict.get("Assortment")
        competition_dist = row_dict.get("CompetitionDistance")
        promo2 = row_dict.get("Is_Promo2_Active")
        consecutive_promo_days = row_dict.get("consecutive_promo_days")
        days_since_last_refurb = row_dict.get("days_since_last_refurb")
        lag_7 = row_dict.get("7th_lag")
        lag_14 = row_dict.get("14th_lag")
        lag_21 = row_dict.get("21st_lag")
        lag_28 = row_dict.get("28th_lag")
        avg_last_3_weeks = row_dict.get("avg_last_3_weeks")
        ma_3d_lag7 = row_dict.get("ma_3d_lag7")
        std_3d_lag7 = row_dict.get("std_3d_lag7")
        ma_7d_lag7 = row_dict.get("ma_7d_lag7")
        ma_15d_lag7 = row_dict.get("ma_15d_lag7")
        ma_30d_lag7 = row_dict.get("ma_30d_lag7")
        lag_diff = row_dict.get("7_8_lag_dif")
        is_promo2_active = row_dict.get("Is_Promo2_Active")
        consecutive_promo2_days = row_dict.get("consecutive_promo2_days")
        promo_x_dayofweek = row_dict.get("promo_x_dayofweek")
        promo_x_storetype = row_dict.get("promo_x_storetype")
        promo2_x_dayofweek = row_dict.get("promo2_x_dayofweek")
        promo2_x_storetype = row_dict.get("promo2_x_storetype")
        days_till_next_holiday = row_dict.get("days_till_next_holiday")
        days_after_holiday = row_dict.get("days_after_holiday")

        cursor.execute(
            insert_query,
            (
                sales_date,
                store_val,
                day_of_week,
                actual_sales,
                actual_customers,
                promo,
                school_holiday,
                month,
                day,
                store_type,
                assortment,
                competition_dist,
                promo2,
                consecutive_promo_days,
                days_since_last_refurb,
                lag_7,
                lag_14,
                lag_21,
                lag_28,
                avg_last_3_weeks,
                ma_3d_lag7,
                std_3d_lag7,
                ma_7d_lag7,
                ma_15d_lag7,
                ma_30d_lag7,
                lag_diff,
                is_promo2_active,
                consecutive_promo2_days,
                promo_x_dayofweek,
                promo_x_storetype,
                promo2_x_dayofweek,
                promo2_x_storetype,
                days_till_next_holiday,
                days_after_holiday,
            ),
        )
        conn.commit()

        return {
            "message": f"Successfully inserted actual sales ({actual_sales}) and customers ({actual_customers}) for Store {store} on {date_val} into main database."
        }
