import streamlit as st
import joblib
import pandas as pd
import numpy as np


# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------
st.set_page_config(
    page_title="AI Property Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# ----------------------------------------
# CUSTOM CSS (EXTREME UI)
# ----------------------------------------
st.markdown("""
<style>

body {
background: linear-gradient(135deg,#0f172a,#020617);
color:white;
}

.main-title{
font-size:48px;
font-weight:700;
text-align:center;
margin-bottom:10px;
}

.sub{
text-align:center;
color:#94a3b8;
margin-bottom:40px;
}

.card{
background: rgba(255,255,255,0.05);
padding:25px;
border-radius:15px;
backdrop-filter: blur(12px);
box-shadow:0px 0px 25px rgba(0,0,0,0.4);
}

.predict-btn{
background:linear-gradient(90deg,#6366f1,#22c55e);
color:white;
padding:12px;
border-radius:10px;
font-size:18px;
}

.price-box{
font-size:40px;
font-weight:bold;
text-align:center;
padding:25px;
border-radius:15px;
background:linear-gradient(90deg,#22c55e,#4ade80);
color:black;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------
# TITLE
# ----------------------------------------
st.markdown(
'<div class="main-title">🏠 AI Property Price Prediction</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="sub">Powered by Random Forest • Ames Housing Dataset</div>',
unsafe_allow_html=True
)

# ----------------------------------------
# LOAD MODEL
# ----------------------------------------
artifacts = joblib.load("model/ames_rf_model.joblib")

model = artifacts["model"]
feature_columns = artifacts["feature_columns"]

# ----------------------------------------
# INPUT SECTION
# ----------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Property Dimensions")

    OverallQual = st.slider("Overall Quality",1,10,5)
    GrLivArea = st.number_input("Living Area (sq ft)",500,6000,1500)
    GarageCars = st.slider("Garage Capacity",0,4,2)
    TotalBsmtSF = st.number_input("Basement Area",0,3000,800)

with col2:
    st.markdown("### Property Details")

    FullBath = st.slider("Full Bathrooms",0,4,2)
    YearBuilt = st.number_input("Year Built",1900,2024,2000)
    Fireplaces = st.slider("Fireplaces",0,3,1)
    LotArea = st.number_input("Lot Area",1000,50000,8000)


# ----------------------------------------
# PREDICTION
# ----------------------------------------

if st.button("🚀 Predict Property Price"):

    # create empty dataframe
    input_df = pd.DataFrame(
        np.zeros((1,len(feature_columns))),
        columns=feature_columns
    )

    # fill important numeric columns
    def safe_fill(col,value):
        if col in input_df.columns:
            input_df[col] = value

    safe_fill("OverallQual",OverallQual)
    safe_fill("GrLivArea",GrLivArea)
    safe_fill("GarageCars",GarageCars)
    safe_fill("TotalBsmtSF",TotalBsmtSF)
    safe_fill("FullBath",FullBath)
    safe_fill("YearBuilt",YearBuilt)
    safe_fill("Fireplaces",Fireplaces)
    safe_fill("LotArea",LotArea)

    # prediction
    prediction = model.predict(input_df)[0]

    st.markdown(
        f"""
        <div class="price-box">
        Estimated Price 💰 <br>
        ₹ {prediction:,.0f}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.balloons()
