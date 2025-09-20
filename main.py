import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
from os import path

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Flight Price Prediction & Recommendation",
    page_icon="✈️",
    layout="wide",
)

# -------------------------------
# Load Model & Dataset
# -------------------------------
model_path = path.join("model", "flight_price_model.pkl")
flight_model = joblib.load(model_path)

data_path = path.join("data", "Flight_Dataset.csv")
dataset = pd.read_csv(data_path)

# -------------------------------
# Sidebar - User Input
# -------------------------------
st.sidebar.title("🔧 Flight Details")



airline = st.sidebar.selectbox("✈️ Airline", dataset["airline"].unique())
source_city = st.sidebar.selectbox("🛫 Source City", dataset["source_city"].unique())
destination_city = st.sidebar.selectbox("🛬 Destination City", dataset["destination_city"].unique())
departure_time = st.sidebar.selectbox("🕒 Departure Time", dataset["departure_time"].unique())
arrival_time = st.sidebar.selectbox("🕓 Arrival Time", dataset["arrival_time"].unique())
stops = st.sidebar.selectbox("⏸ Stops", sorted(dataset["stops"].unique()))
travel_class = st.sidebar.selectbox("💺 Class", dataset["class"].unique())
duration = st.sidebar.number_input("⏱ Duration (hours)", min_value=1.0, max_value=50.0, value=2.0)
days_left = st.sidebar.slider("📅 Days Left to Travel", min_value=1, max_value=60, value=10)


# -------------------------------
# Prepare Input Data
# -------------------------------
input_dict = {
    "airline": airline,
    "source_city": source_city,
    "destination_city": destination_city,
    "departure_time": departure_time,
    "arrival_time": arrival_time,
    "stops": stops,
    "class": travel_class,
    "duration": duration,
    "days_left": days_left,
}

input_df = pd.DataFrame([input_dict])


# -------------------------------
# Main Layout
# -------------------------------
st.title("✈️ Flight Price Prediction & Recommendation")
st.markdown(
    """
    This app helps you **predict flight ticket prices** and get **best recommendations** 
    based on your journey details.  
    """
)

tab1, tab2 = st.tabs(["💰 Price Prediction", "⭐ Recommendations"])

# -------------------------------
# Tab 1: Prediction
# -------------------------------
with tab1:
    st.subheader("Your Flight Details")
    st.dataframe(input_df)

    if st.button("🔮 Predict Price"):
        prediction = flight_model.predict(input_df)[0]
        st.success(f"Estimated Ticket Price: ₹ {round(prediction, 2)}")

# -------------------------------
# Tab 2: Recommendations
# -------------------------------
with tab2:
    st.subheader("Recommended Cheapest Flights")

    # Filter dataset using updated column names
    recs = dataset[
        (dataset["source_city"] == source_city) &
        (dataset["destination_city"] == destination_city)
    ].sort_values(by="price").head(5)

    if not recs.empty:
        st.write("Here are the **top cheapest flights** for your route:")
        st.dataframe(recs[[
            "airline", "source_city", "destination_city", "stops", "class", "price"
        ]])
    else:
        st.warning("⚠️ No matching flights found in dataset.")
