import sqlite3
from contextlib import closing


def save_inference_data(inference_data:dict,date:str,
    db_path: str ,predicted_customers:int,
    predicted_sales:int):

    #Saves the inference data into the SQLite database.    
    
    inference_data["predicted_customers"] = predicted_customers
    inference_data["predicted_sales"] = predicted_sales
    inference_data["Date"] = date

    query = """INSERT INTO inference_results (
        Store, DayOfWeek, Promo, SchoolHoliday, StoreType, Assortment,
        CompetitionDistance, Is_Promo2_Active,days_till_next_holiday,
        month, day, promo_x_storetype, promo2_x_storetype,
        promo_x_dayofweek, promo2_x_dayofweek,
        consecutive_promo_days, consecutive_promo2_days,
        days_after_holiday, days_since_last_refurb,
        '7th_lag', '14th_lag', '21st_lag', '28th_lag',
        '7_8_lag_dif', avg_last_3_weeks,
        std_3d_lag7, ma_3d_lag7, ma_7d_lag7,
        ma_15d_lag7, ma_30d_lag7,
            predicted_customers, predicted_sales, Date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(inference_data.values()))
        conn.commit()
