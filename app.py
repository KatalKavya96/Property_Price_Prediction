import math
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Property Valuation Dashboard", layout="wide")

# -------------------------------------------------
# LOAD MODEL ARTIFACTS
# -------------------------------------------------
artifacts = joblib.load("model/house_price_lr_pipeline.joblib")
pipe = artifacts["pipeline"]
target_transform = artifacts.get("target_transform", None)
train_columns = artifacts.get("train_columns", None)
metrics = artifacts.get("metrics", {})  # optional: {"R2":..., "RMSE":..., "MAE":...}

if train_columns is None:
    st.error("Artifact missing 'train_columns'. Re-save the model with train_columns included.")
    st.stop()

# -------------------------------------------------
# STYLE (keep the same dashboard vibe)
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

.tab{
  padding: 7px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--pill);
  color: rgba(255,255,255,.78);
  font-size:12px;
}
.tab.active{
  background: rgba(59,130,246,.18);
  border-color: rgba(59,130,246,.35);
  color: rgba(255,255,255,.92);
}

.card{
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 18px 55px rgba(0,0,0,.32);
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

.small-row{
  display:flex; gap:14px; flex-wrap:wrap; margin-top: 12px;
}
.metric{
  border: 1px solid var(--border);
  background: var(--panel2);
  border-radius: 12px;
  padding: 10px 12px;
  min-width: 200px;
}
.metric .label{ font-size:12px; color: var(--muted); }
.metric .value{ font-size:14px; font-weight:850; margin-top:4px; }

.range-pills{
  display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end;
}
.range-pills span{
  font-size:12px;
  padding: 6px 10px;
  border: 1px solid var(--border);
  background: var(--pill);
  border-radius: 999px;
  color: rgba(255,255,255,.78);
}
.range-pills span.active{
  background: rgba(59,130,246,.18);
  border-color: rgba(59,130,246,.35);
  color: rgba(255,255,255,.92);
}

.table-wrap{
  border: 1px solid var(--border);
  background: var(--panel2);
  border-radius: 14px;
  overflow:hidden;
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

.kv{
  display:grid; grid-template-columns: 1fr 1fr;
  gap:10px; margin-top: 12px;
}
.kv .item{
  border: 1px solid var(--border);
  background: var(--panel2);
  border-radius: 12px;
  padding: 10px 12px;
}
.kv .k{ font-size:12px; color: var(--muted); }
.kv .v{ font-size:13px; font-weight:900; margin-top:3px; }

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
# NAV (kept for structure, not fake actions)
# -------------------------------------------------
st.markdown(
    """
<div class="container">
  <div class="navbar">
    <div class="brand">
      <div class="brand-dot"></div>
      <div>Property Valuation</div>
    </div>
    <div style="display:flex; gap:8px; align-items:center;">
      <div class="tab active">Dashboard</div>
      <div class="tab">Model</div>
      <div class="tab">Insights</div>
    </div>
    <div style="color: rgba(255,255,255,.65); font-size:12px;">
      Unit: USD
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# -------------------------------------------------
# SIDEBAR INPUTS (descending impact)
# -------------------------------------------------
with st.sidebar:
    st.subheader("Inputs")
    st.caption("Ordered by influence on prediction (typical Ames drivers).")

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

    st.markdown("---")
    sensitivity_feature = st.selectbox("Sensitivity feature", ["GrLivArea", "OverallQual", "YearBuilt", "TotalBsmtSF"])
    run = st.button("Run valuation")

# -------------------------------------------------
# Prediction helpers
# -------------------------------------------------
def build_input_df() -> pd.DataFrame:
    df = pd.DataFrame([{col: 0 for col in train_columns}])

    def safe_fill(col, val):
        if col in df.columns:
            df.loc[0, col] = val

    safe_fill("OverallQual", OverallQual)
    safe_fill("GrLivArea", GrLivArea)
    safe_fill("GarageCars", GarageCars)
    safe_fill("TotalBsmtSF", TotalBsmtSF)
    safe_fill("YearBuilt", YearBuilt)
    safe_fill("FullBath", FullBath)
    safe_fill("Fireplaces", Fireplaces)
    safe_fill("LotArea", LotArea)

    return df

def predict_usd(df: pd.DataFrame) -> float:
    pred_log = float(pipe.predict(df)[0])
    pred = float(np.expm1(pred_log)) if target_transform == "log1p" else pred_log
    if not math.isfinite(pred) or pred < 0:
        raise ValueError("Invalid prediction")
    return pred

# session caching
if "pred_usd" not in st.session_state:
    st.session_state.pred_usd = None

if run or st.session_state.pred_usd is None:
    try:
        st.session_state.pred_usd = predict_usd(build_input_df())
    except Exception:
        st.session_state.pred_usd = None

pred_value = st.session_state.pred_usd

# -------------------------------------------------
# TOP SECTION: KPI + Sensitivity chart (both model-driven)
# -------------------------------------------------
top_left, top_right = st.columns([1.05, 1.4], gap="large")

with top_left:
    st.markdown(
        f"""
<div class="card">
  <div class="h1">Valuation Summary</div>
  <div class="sub">Prediction generated from your saved pipeline (USD output).</div>
  <div class="sub" style="margin-top:14px;">Estimated Price</div>
  <div class="big-number">{("$" + format(pred_value, ",.0f")) if pred_value is not None else "—"}</div>

  <div class="small-row">
    <div class="metric">
      <div class="label">Model MAE (USD)</div>
      <div class="value">{("$" + format(metrics.get("MAE"), ",.0f")) if metrics.get("MAE") is not None else "Not available"}</div>
    </div>
    <div class="metric">
      <div class="label">Model RMSE (USD)</div>
      <div class="value">{("$" + format(metrics.get("RMSE"), ",.0f")) if metrics.get("RMSE") is not None else "Not available"}</div>
    </div>
    <div class="metric">
      <div class="label">Approx range (±RMSE)</div>
      <div class="value">
        {(
          "$" + format(max(0, pred_value - metrics.get("RMSE")), ",.0f") + "  to  " + "$" + format(pred_value + metrics.get("RMSE"), ",.0f")
        ) if (pred_value is not None and metrics.get("RMSE") is not None) else "Not available"}
      </div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

with top_right:
    st.markdown(
        f"""
<div class="card">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
    <div>
      <div style="font-weight:900; letter-spacing:-0.02em;">Sensitivity curve</div>
      <div class="sub">How predicted price changes when <b>{sensitivity_feature}</b> varies (others fixed).</div>
    </div>
    <div class="range-pills">
      <span class="active">Model-based</span>
    </div>
  </div>
  <hr class="sep" />
</div>
""",
        unsafe_allow_html=True,
    )

    if pred_value is None:
        st.info("Run valuation to generate the sensitivity curve.")
    else:
        base_df = build_input_df()

        # choose sweep range per feature
        if sensitivity_feature == "GrLivArea":
            xs = np.linspace(max(300, GrLivArea * 0.7), min(6000, GrLivArea * 1.3), 40)
        elif sensitivity_feature == "OverallQual":
            xs = np.arange(1, 11)
        elif sensitivity_feature == "YearBuilt":
            lo = max(1900, YearBuilt - 25)
            hi = min(2026, YearBuilt + 25)
            xs = np.linspace(lo, hi, 40)
        else:  # TotalBsmtSF
            xs = np.linspace(max(0, TotalBsmtSF * 0.6), min(5000, TotalBsmtSF * 1.4), 40)

        ys = []
        for x in xs:
            tmp = base_df.copy()
            if sensitivity_feature in tmp.columns:
                tmp.loc[0, sensitivity_feature] = float(x)
            ys.append(predict_usd(tmp))

        chart_df = pd.DataFrame({sensitivity_feature: xs, "Predicted Price (USD)": ys}).set_index(sensitivity_feature)
        st.line_chart(chart_df, height=280, use_container_width=True)

# -------------------------------------------------
# BOTTOM SECTION: Marginal impacts table + Model panel
# -------------------------------------------------
st.write("")
bottom_left, bottom_right = st.columns([1.65, 0.85], gap="large")

def marginal_impacts(base_df: pd.DataFrame, base_pred: float) -> pd.DataFrame:
    # Small perturbations to estimate marginal effect (model-agnostic)
    steps = {
        "OverallQual": 1,
        "GrLivArea": 100,
        "GarageCars": 1,
        "TotalBsmtSF": 100,
        "YearBuilt": 5,
        "FullBath": 1,
        "Fireplaces": 1,
        "LotArea": 1000,
    }

    rows = []
    for feat, step in steps.items():
        if feat not in base_df.columns:
            continue

        tmp = base_df.copy()
        tmp.loc[0, feat] = float(tmp.loc[0, feat]) + float(step)
        new_pred = predict_usd(tmp)
        delta = new_pred - base_pred

        rows.append({
            "Feature": feat,
            "Current": float(base_df.loc[0, feat]),
            "Step": f"+{step}",
            "Δ Price (USD)": delta,
        })

    out = pd.DataFrame(rows)
    out = out.sort_values(by="Δ Price (USD)", ascending=False)
    out["Δ Price (USD)"] = out["Δ Price (USD)"].map(lambda v: f"${v:,.0f}")
    return out

with bottom_left:
    st.markdown(
        """
<div class="table-wrap">
  <div class="table-header">
    <div class="table-title">Marginal impact (local sensitivity)</div>
    <div class="sub">Estimated price change from small increases in each feature.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if pred_value is None:
        st.warning("No valuation available yet.")
    else:
        base_df = build_input_df()
        st.dataframe(
            marginal_impacts(base_df, pred_value),
            use_container_width=True,
            hide_index=True,
        )

with bottom_right:
    r2 = metrics.get("R2")
    rmse = metrics.get("RMSE")
    mae = metrics.get("MAE")

    st.markdown(
        f"""
<div class="card">
  <div style="font-weight:900; letter-spacing:-0.02em;">Model details</div>
  <div class="sub">Transparency panel for deployment and evaluation.</div>

  <div class="kv">
    <div class="item">
      <div class="k">Model</div>
      <div class="v">Linear Regression</div>
    </div>
    <div class="item">
      <div class="k">Target transform</div>
      <div class="v">{target_transform if target_transform else "none"}</div>
    </div>
    <div class="item">
      <div class="k">Unit</div>
      <div class="v">USD</div>
    </div>
    <div class="item">
      <div class="k">Inputs used</div>
      <div class="v">8 primary drivers</div>
    </div>
    <div class="item">
      <div class="k">R² (val)</div>
      <div class="v">{f"{r2:.3f}" if isinstance(r2, (int, float)) else "Not available"}</div>
    </div>
    <div class="item">
      <div class="k">RMSE (val)</div>
      <div class="v">{f"${rmse:,.0f}" if isinstance(rmse, (int, float)) else "Not available"}</div>
    </div>
    <div class="item">
      <div class="k">MAE (val)</div>
      <div class="v">{f"${mae:,.0f}" if isinstance(mae, (int, float)) else "Not available"}</div>
    </div>
    <div class="item">
      <div class="k">Artifact</div>
      <div class="v">joblib pipeline</div>
    </div>
  </div>

  <hr class="sep" />

  <div class="sub">Input snapshot</div>
  <div style="margin-top:8px; color: rgba(255,255,255,.78); font-size:12px; line-height:1.6;">
    OverallQual: {OverallQual}<br/>
    GrLivArea: {GrLivArea} sq ft<br/>
    GarageCars: {GarageCars}<br/>
    TotalBsmtSF: {TotalBsmtSF} sq ft<br/>
    YearBuilt: {YearBuilt}<br/>
    FullBath: {FullBath}<br/>
    Fireplaces: {Fireplaces}<br/>
    LotArea: {LotArea} sq ft
  </div>
</div>
""",
        unsafe_allow_html=True,
    )