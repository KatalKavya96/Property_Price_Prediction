import math
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Property Price Prediction Dashboard", layout="wide")

# -------------------------------------------------
# LOAD MODEL ARTIFACTS
# -------------------------------------------------
artifacts = joblib.load("model/house_price_lr_pipeline.joblib")
pipe = artifacts["pipeline"]
target_transform = artifacts.get("target_transform", None)
train_columns = artifacts.get("train_columns", None)

if train_columns is None:
    st.error("Artifact missing 'train_columns'. Re-save the model with train_columns included.")
    st.stop()

# -------------------------------------------------
# STYLE
# -------------------------------------------------
st.markdown(
    """
<style>
:root{
  --bg:#070a12;
  --panel:rgba(255,255,255,.03);
  --panel2:rgba(255,255,255,.02);
  --border:rgba(255,255,255,.08);
  --muted:rgba(255,255,255,.62);
  --text:rgba(255,255,255,.92);
  --pill:rgba(255,255,255,.06);
  --blue:#3b82f6;
  --green:#22c55e;
}

/* ✅ Add global page padding so nothing hugs edges */
div.block-container{
  padding-top: 1.4rem !important;
  padding-bottom: 2.0rem !important;
}

/* ✅ Simple reusable spacer */
.vspace{ height: 14px; }

.stApp{
  background:
    radial-gradient(900px 500px at 15% 15%, rgba(59,130,246,.10), transparent 55%),
    radial-gradient(700px 450px at 85% 25%, rgba(34,197,94,.08), transparent 55%),
    linear-gradient(180deg, var(--bg) 0%, #05060c 100%);
  color: var(--text);
}
header, footer, #MainMenu { visibility:hidden; }

.container { max-width: 1400px; margin: 0 auto; }

.navbar{
  display:flex; align-items:center; justify-content:space-between;
  gap:16px;
  padding: 12px 14px;
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 14px;
  box-shadow: 0 18px 55px rgba(0,0,0,.35);
  margin-bottom: 16px; /* ✅ space under navbar */
}
.brand{
  display:flex; align-items:center; gap:10px;
  font-weight:850; letter-spacing:-0.02em;
}
.brand-dot{
  width:10px; height:10px; border-radius:999px;
  background: linear-gradient(135deg, var(--blue), var(--green));
  box-shadow: 0 0 0 6px rgba(59,130,246,.08);
}

.card{
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 18px 55px rgba(0,0,0,.32);
  margin-bottom: 14px; /* ✅ prevents “card-on-card” touching */
}

.h1{
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.03em;
  margin: 0;
}
.sub{
  color: var(--muted);
  font-size: 13px;
  margin-top: 6px;
}
.big-number{
  font-size: 54px;
  font-weight: 950;
  letter-spacing: -0.03em;
  margin: 10px 0 0 0;
}

.table-wrap{
  border: 1px solid var(--border);
  background: var(--panel2);
  border-radius: 14px;
  overflow:hidden;
  margin-top: 10px;      /* ✅ spacing above table */
  margin-bottom: 14px;   /* ✅ spacing below table */
}
.table-header{
  display:flex; align-items:center; justify-content:space-between;
  padding: 12px 14px;
  background: var(--panel);
  border-bottom: 1px solid var(--border);
}
.table-title{
  font-weight:900; letter-spacing:-0.02em;
}

hr.sep{
  border:0; height:1px; background: rgba(255,255,255,.08);
  margin: 14px 0;
}

/* Streamlit widget polish */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input{
  background: rgba(255,255,255,.03) !important;
  border: 1px solid var(--border) !important;
  color: rgba(255,255,255,.85) !important;
  border-radius: 10px !important;
}
div[data-testid="stSlider"] > div{
  padding-top: 6px;
}
div.stButton > button{
  width:100%;
  border-radius: 12px !important;
  height: 44px;
  border: 1px solid rgba(255,255,255,.10) !important;
  background: rgba(255,255,255,.07) !important;
  color: rgba(255,255,255,.92) !important;
  font-weight: 900 !important;
}
div.stButton > button:hover{
  background: rgba(255,255,255,.10) !important;
  transform: translateY(-1px);
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# NAVBAR
# -------------------------------------------------
st.markdown(
    """
<div class="container">
  <div class="navbar">
    <div class="brand">
      <div class="brand-dot"></div>
      <div>Property Price Prediction </div>
    </div>
    <div style="color: rgba(255,255,255,.65); font-size:12px;">
      Unit: USD
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "latest_pred" not in st.session_state:
    st.session_state.latest_pred = None

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def build_input_df(values: dict) -> pd.DataFrame:
    df = pd.DataFrame([{col: 0 for col in train_columns}])
    for k, v in values.items():
        if k in df.columns:
            df.loc[0, k] = v
    return df

def predict_usd(df: pd.DataFrame) -> float:
    pred_raw = float(pipe.predict(df)[0])
    pred = float(np.expm1(pred_raw)) if target_transform == "log1p" else pred_raw
    if not math.isfinite(pred) or pred < 0:
        raise ValueError("Invalid prediction")
    return pred

# -------------------------------------------------
# LAYOUT
# -------------------------------------------------
left, right = st.columns([1.05, 1.4], gap="large")

with left:
    latest = st.session_state.latest_pred
    st.markdown(
        f"""
<div class="card">
  <div class="h1">Latest Prediction</div>
  <div class="sub">Click <b>Predict</b> to generate a value and build the chart.</div>
  <div class="big-number">{("$" + format(latest, ",.0f")) if latest is not None else "—"}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="vspace"></div>', unsafe_allow_html=True)

    st.markdown(
        """
<div class="card">
  <div class="h1">Inputs</div>
  <div class="sub">Adjust values on the main page (no sidebar).</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="vspace"></div>', unsafe_allow_html=True)

    preset = st.selectbox("Preset", ["Custom", "Starter", "Family", "Premium"], index=0)
    presets = {
        "Custom":  dict(OverallQual=5, GrLivArea=1500, GarageCars=2, TotalBsmtSF=800, YearBuilt=2000, FullBath=2, Fireplaces=1, LotArea=8000),
        "Starter": dict(OverallQual=4, GrLivArea=1100, GarageCars=1, TotalBsmtSF=650, YearBuilt=1978, FullBath=1, Fireplaces=0, LotArea=7000),
        "Family":  dict(OverallQual=6, GrLivArea=1850, GarageCars=2, TotalBsmtSF=950, YearBuilt=2004, FullBath=2, Fireplaces=1, LotArea=9000),
        "Premium": dict(OverallQual=8, GrLivArea=2850, GarageCars=3, TotalBsmtSF=1400, YearBuilt=2016, FullBath=3, Fireplaces=2, LotArea=12000),
    }
    d = presets[preset]

    OverallQual = st.slider("Overall Quality", 1, 10, int(d["OverallQual"]))
    GrLivArea = st.number_input("Living Area (sq ft)", 300, 6000, int(d["GrLivArea"]), step=25)
    GarageCars = st.slider("Garage Capacity", 0, 4, int(d["GarageCars"]))
    TotalBsmtSF = st.number_input("Basement Area (sq ft)", 0, 5000, int(d["TotalBsmtSF"]), step=25)
    YearBuilt = st.number_input("Year Built", 1900, 2026, int(d["YearBuilt"]))
    FullBath = st.select_slider("Full Bathrooms", options=[0, 1, 2, 3, 4], value=int(d["FullBath"]))
    Fireplaces = st.select_slider("Fireplaces", options=[0, 1, 2, 3], value=int(d["Fireplaces"]))
    LotArea = st.number_input("Lot Area (sq ft)", 1000, 50000, int(d["LotArea"]), step=100)

    st.markdown('<div class="vspace"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="small")
    with c1:
        add_point = st.button("Predict")
    with c2:
        clear = st.button("Clear chart")

    if clear:
        st.session_state.history = []
        st.session_state.latest_pred = None

    if add_point:
        values = {
            "OverallQual": float(OverallQual),
            "GrLivArea": float(GrLivArea),
            "GarageCars": float(GarageCars),
            "TotalBsmtSF": float(TotalBsmtSF),
            "YearBuilt": float(YearBuilt),
            "FullBath": float(FullBath),
            "Fireplaces": float(Fireplaces),
            "LotArea": float(LotArea),
        }
        try:
            pred = predict_usd(build_input_df(values))
            st.session_state.latest_pred = pred
            run_id = len(st.session_state.history) + 1
            st.session_state.history.append({"Run": run_id, **values, "PredictedPriceUSD": pred})
        except Exception as e:
            st.error(f"Prediction failed: {e}")

with right:
    st.markdown(
        """
<div class="card">
  <div style="font-weight:900; letter-spacing:-0.02em;">Prediction points chart</div>
  <div class="sub">Points appear as you add predictions. The chart stays visible even when empty.</div>
  <hr class="sep" />
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="vspace"></div>', unsafe_allow_html=True)

    if len(st.session_state.history) == 0:
        empty_chart = pd.DataFrame({"PredictedPriceUSD": [np.nan, np.nan]}, index=[1, 2])
        st.line_chart(empty_chart, height=280, use_container_width=True)
        st.caption("No points yet — click **Predict** to plot values.")
    else:
        hist = pd.DataFrame(st.session_state.history)
        chart_df = hist[["Run", "PredictedPriceUSD"]].set_index("Run")
        st.line_chart(chart_df, height=280, use_container_width=True)

    st.markdown('<div class="vspace"></div>', unsafe_allow_html=True)

    st.markdown(
        """
<div class="table-wrap">
  <div class="table-header">
    <div class="table-title">Prediction History</div>
    <div class="sub">Each row = one prediction point.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    show_cols = ["Run", "PredictedPriceUSD", "OverallQual", "GrLivArea", "GarageCars", "TotalBsmtSF", "YearBuilt", "FullBath", "Fireplaces", "LotArea"]

    if len(st.session_state.history) == 0:
        placeholder = pd.DataFrame([{
            "Run": "—",
            "PredictedPriceUSD": "—",
            "OverallQual": "—",
            "GrLivArea": "—",
            "GarageCars": "—",
            "TotalBsmtSF": "—",
            "YearBuilt": "—",
            "FullBath": "—",
            "Fireplaces": "—",
            "LotArea": "—",
        }])
        st.dataframe(placeholder[show_cols], use_container_width=True, hide_index=True)
    else:
        hist = pd.DataFrame(st.session_state.history)
        out = hist[show_cols].copy()
        out["PredictedPriceUSD"] = out["PredictedPriceUSD"].map(lambda x: f"${x:,.0f}")
        st.dataframe(out, use_container_width=True, hide_index=True)