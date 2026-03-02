import streamlit as st

def render_inputs(presets):
    """Renders the preset selector and all input widgets, returns the numeric values."""
    preset_name = st.selectbox("Preset", list(presets.keys()), index=0)
    d = presets[preset_name]

    overall_qual = st.slider("Overall Quality", 1, 10, int(d["OverallQual"]))
    gr_liv_area = st.number_input("Living Area (sq ft)", 300, 6000, int(d["GrLivArea"]), step=25)
    garage_cars = st.slider("Garage Capacity", 0, 4, int(d["GarageCars"]))
    total_bsmt_sf = st.number_input("Basement Area (sq ft)", 0, 5000, int(d["TotalBsmtSF"]), step=25)
    year_built = st.number_input("Year Built", 1900, 2026, int(d["YearBuilt"]))
    full_bath = st.select_slider("Full Bathrooms", options=[0, 1, 2, 3, 4], value=int(d["FullBath"]))
    fireplaces = st.select_slider("Fireplaces", options=[0, 1, 2, 3], value=int(d["Fireplaces"]))
    lot_area = st.number_input("Lot Area (sq ft)", 1000, 50000, int(d["LotArea"]), step=100)

    values = {
        "OverallQual": float(overall_qual),
        "GrLivArea": float(gr_liv_area),
        "GarageCars": float(garage_cars),
        "TotalBsmtSF": float(total_bsmt_sf),
        "YearBuilt": float(year_built),
        "FullBath": float(full_bath),
        "Fireplaces": float(fireplaces),
        "LotArea": float(lot_area),
    }
    
    return values
