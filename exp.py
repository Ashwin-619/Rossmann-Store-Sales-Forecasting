from contextlib import closing
from pathlib import Path
from sqlite3 import connect
from fastapi import FastAPI
# from Data_Schema.data_pipeline import FeaturePipeline
# from Data_Schema.input_data import InputFeatures
#from Data_Schema.fetch_past_values import fetch_last_30d_sales, fetch_day_metrics
import pickle
from datetime import date
import pandas as pd


# Sales_Data
# inference_results

# with closing(connect(r"DB\Sales_data.db")) as conn:
#     cursor = conn.cursor()
#     query = "DELETE FROM inference_results;"
#     cursor.execute(query)
#     conn.commit()


with closing(connect(r"DB\Sales_data.db")) as conn:
   
    query = "SELECT * FROM Sales_Data;"
    data_df = pd.read_sql_query(query, conn)

print("DataFrame info:", data_df)
#print("DataFrame info:", data_df.info())

#     #data_df = pd.DataFrame(cursor.fetchall())



# with closing(connect(r"DB\Sales_data.db")) as conn:
#     cursor = conn.cursor()
#     query = """CREATE TABLE inference_results (
#     "Store"                   INT,
#     "DayOfWeek"               INT,
#     "Promo"                   INT,
#     "SchoolHoliday"           INT,
#     "StoreType"               VARCHAR(10),
#     "Assortment"              VARCHAR(50),
#     "CompetitionDistance"     FLOAT,
#     "Is_Promo2_Active"        INT,
#     "days_till_next_holiday"  INT,
#     "month"                   INT,
#     "day"                     INT,
#     "promo_x_storetype"       VARCHAR(20),
#     "promo2_x_storetype"      VARCHAR(20),
#     "promo_x_dayofweek"       VARCHAR(20),
#     "promo2_x_dayofweek"      VARCHAR(20),
#     "consecutive_promo_days"  INT,
#     "consecutive_promo2_days" INT,
#     "days_after_holiday"      INT,
#     "days_since_last_refurb"  INT,
#     "7th_lag"                 INT,
#     "14th_lag"                INT,
#     "21st_lag"                INT,
#     "28th_lag"                INT,
#     "7_8_lag_dif"             INT,
#     "avg_last_3_weeks"        FLOAT,
#     "std_3d_lag7"             FLOAT,
#     "ma_3d_lag7"              FLOAT,
#     "ma_7d_lag7"              FLOAT,
#     "ma_15d_lag7"             FLOAT,
#     "ma_30d_lag7"             FLOAT,
#     "predicted_customers"     INT,
#     "predicted_sales"         INT,
#     "Date"                    DATE    
    
#     );"""
#     cursor.execute(query)
#     data_df = pd.DataFrame(cursor.fetchall())

# print("DataFrame info:", data_df)    
# #print("Customer model feature names:", customer_model.feature_names_in_)

# past_val=fetch_last_30d_sales(present_date='2015-08-01',store=44,db_path="DB/Sales_data.db")

# print("Past values:", past_val)
# print("Past values type:", type(past_val))
# print("Past values len:", len(past_val))
# print("Past values single type:", type(past_val['2015-07-10']))
# print("Past values single:", past_val['2015-07-10'])













# test_data={
#   "Store": 44,
#   "DayOfWeek": "1",
#   "Is_Promo_Active": 1,
#   "School_holiday": 0,
#   "Storetype": "b",
#   "Assortment": "Basic",
#   "Competition_Distance": 1100,
#   "Is_Promo2_Active": 0,
#   "Date": "2015-08-01"
# }


# model_pipeline = TwoStageModelPipeline(
#     customer_model_path="customer_final_model.pkl",
#     sales_model_path="sales_final_model.pkl",
#     customer_col_name="predicted_customers"  # Match column name used during training
# )

# data=InputFeatures(
#     Store=1,
#     DayOfWeek="1",
#     Is_Promo_Active=1,
#     School_holiday=0,
#     Storetype="a",
#     Assortment="Basic",
#     Competition_Distance=1000,
#     Is_Promo2_Active=0,
#     Date=date(2015, 8, 1)
# )
# # # # Step A: Transform raw payload into 1-row feature DataFrame#features_df = feature_pipeline.transform(data)
# features_df = features_df[data_df.columns].astype(data_df.dtypes)
# print("Features DataFrame:", features_df.to_dict())


# booster = customer_model.get_booster() if hasattr(customer_model, "get_booster") else customer_model
# for name, ftype in zip(booster.feature_names, booster.feature_types):
#     print(f"Feature: {name:<25} Expected XGB Type: {ftype}")

#print(customer_model.get_booster().feature_types)

# features_df = features_df[list(customer_model.feature_names_in_)]
# print("Features DataFrame:", features_df)
# print("Features DataFrame:", features_df.info())
#print("customer_model DataFrame:", pd.Series(customer_model.feature_names_in_))

# print(' ')
# print("Features DataFrame info:", features_df.info())
# print("Features DataFrame index:", features_df.index)
# print('')
# # Step B: Run sequential inference (Customer Model -> Sales Model)
# # results = model_pipeline.predict(features_df)


# # print("Features DataFrame:", features_df)
# # print(' ')
# # print("Features DataFrame info:", features_df.info())
# # print('')
# # print("Predictions:", results)