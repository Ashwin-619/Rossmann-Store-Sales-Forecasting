from datetime import date
import requests
import streamlit as st

st.title("Demand Forecasting for Rossmann Stores")

tab1, tab2 = st.tabs(["Predict Sales", "Insert Actual Data"])

# ==================== TAB 1: PREDICTION ====================
with tab1:
    st.subheader("Predict Sales for a Specific Store")

    Input_data = {}

    # Unique keys added to prevent DuplicateWidgetID errors
    Input_data["Store"] = st.number_input("Store Number", min_value=1, max_value=1115, value=1, key="pred_store")


    Is_Promo_Active_ = st.selectbox("Is there an ongoing promotion?", options=["Yes", "No"], index=1, key="pred_promo")
    Input_data["Is_Promo_Active"] = 1 if Is_Promo_Active_ == "Yes" else 0

    School_holiday_ = st.selectbox("Is it a school holiday?", options=["Yes", "No"], key="pred_school")
    Input_data["School_holiday"] = 1 if School_holiday_ == "Yes" else 0

    Storetype = st.selectbox("Type of Store", options=["a", "b", "c", "d"], key="pred_type")
    Input_data["Storetype"] = Storetype


    Input_data["Assortment"] = st.selectbox("Assortment of Store", options=["Basic", "Extended", "Extra"], key="pred_assortment")


    Competition_Distance = st.select_slider(
        "Distance to competition in meters", 
        options=[i for i in range(0, 11000, 100)], 
        value=1000,
        key="pred_dist"
    )
    Input_data["Competition_Distance"] = Competition_Distance

    Is_Promo2_Active_ = st.selectbox("Is Promo2 active?", options=["Yes", "No"], key="pred_promo2")
    Input_data["Is_Promo2_Active"] = 1 if Is_Promo2_Active_ == "Yes" else 0

    # Explicit default value added within min_value/max_value range
    Date = st.date_input(
        "Date for prediction (YYYY-MM-DD)", 
        value=date(2015, 7, 31),
        min_value=date(2015, 7, 31), 
        max_value=date(2017, 7, 31),
        key="pred_date"
    )
    Input_data["Date"] = Date.strftime("%Y-%m-%d")

    Next_holiday = st.date_input(
        "Date of next holiday (YYYY-MM-DD)", 
        value=date(2015, 7, 31),
        min_value=date(2015, 7, 31), 
        max_value=date(2017, 7, 31),
        key="pred_holiday"
    )
    Input_data["Next_holiday"] = Next_holiday.strftime("%Y-%m-%d")

    col1, col2 = st.columns(2)
    if col1.button("Show Input Data", key="btn_show_pred"):
        st.json(Input_data)

    if col2.button("Predict Sales", key="btn_submit_pred"):
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=Input_data)
            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Predicted Sales: {prediction.get('predictions_for_Sales')}")
                st.success(f"Predicted Customers: {prediction.get('predictions_for_Customers')}")
            else:
                st.error(f"Error in prediction request (Status Code: {response.status_code}).")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server at http://127.0.0.1:8000.")


# ==================== TAB 2: DATA INSERTION ====================
with tab2:
    st.subheader("Insert Actual Sales & Customer Data for a Specific Store")

    Insert_data = {}

    Insert_data["Store"] = st.number_input("Store Number", min_value=1, max_value=1115, value=1, key="insert_store")

    Date_insert = st.date_input(
        "Date of actual data (YYYY-MM-DD)", 
        value=date(2015, 7, 31),
        min_value=date(2015, 7, 31), 
        max_value=date(2017, 7, 31),
        key="insert_date"
    )
    Insert_data["Date"] = Date_insert.strftime("%Y-%m-%d")

    Sales = st.number_input("Actual Sales", min_value=0, value=0, key="insert_sales")
    Insert_data["Sales"] = Sales

    Customers = st.number_input("Actual Customers", min_value=0, value=0, key="insert_cust")
    Insert_data["Customers"] = Customers

    col3, col4 = st.columns(2)
    if col3.button("Show Input Data for Insertion", key="btn_show_insert"):
        st.json(Insert_data)

    if col4.button("Insert Data", key="btn_submit_insert"):
        try:
            response = requests.post("http://127.0.0.1:8000/insert_data", json=Insert_data)
            if response.status_code == 200:
                message = response.json()
                st.success(message.get('message', 'Data inserted successfully!'))
            else:
                st.error(f"Error in data insertion request (Status Code: {response.status_code}).")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server at http://127.0.0.1:8000.")