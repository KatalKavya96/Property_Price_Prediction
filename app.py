import streamlit as st
import joblib
import pandas as pd

st.title("🏠 Property Price Prediction")

# Load Model
artifacts = joblib.load("model/house_price_model.joblib")

model = artifacts["model"]
scaler = artifacts["scaler"]
columns = artifacts["columns"]

st.write("Enter Property Details")

# Inputs
area = st.number_input("Area", 500, 10000, 3000)
bedrooms = st.number_input("Bedrooms", 1, 10, 3)
bathrooms = st.number_input("Bathrooms", 1, 5, 2)
stories = st.number_input("Stories", 1, 5, 2)
parking = st.number_input("Parking", 0, 5, 1)

mainroad = st.selectbox("Main Road Access", ["Yes","No"])
guestroom = st.selectbox("Guest Room", ["Yes","No"])
basement = st.selectbox("Basement", ["Yes","No"])
hotwaterheating = st.selectbox("Hot Water Heating", ["Yes","No"])
airconditioning = st.selectbox("Air Conditioning", ["Yes","No"])
prefarea = st.selectbox("Preferred Area", ["Yes","No"])

furnishingstatus = st.selectbox(
    "Furnishing Status",
    ["Unfurnished","Semi-Furnished","Furnished"]
)

# Encoding
yes_no = lambda x: 1 if x == "Yes" else 0

furnishing_map = {
    "Unfurnished":0,
    "Semi-Furnished":1,
    "Furnished":2
}

if st.button("Predict Price"):

    input_data = pd.DataFrame([[
        area,
        bedrooms,
        bathrooms,
        stories,
        parking,
        yes_no(mainroad),
        yes_no(guestroom),
        yes_no(basement),
        yes_no(hotwaterheating),
        yes_no(airconditioning),
        yes_no(prefarea),
        furnishing_map[furnishingstatus]
    ]], columns=columns)

    # Scale same as training
    scaled_data = scaler.transform(input_data)

    prediction = model.predict(scaled_data)

    st.success(f"Estimated Property Price: ₹ {prediction[0]:,.0f}")