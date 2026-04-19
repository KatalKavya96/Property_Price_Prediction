import streamlit as st
import pandas as pd

from src.config import PAGE_TITLE, LAYOUT, MODEL_PATH, UNIT_LABEL, PRESETS
from src.assets.styles import inject_styles
from src.core.model import load_artifacts, build_input_df, predict_usd
from src.core.state import init_state, clear_state, append_history
from src.core.comparable import get_comparables
from src.agent.nodes import run_agent
from src.ui.layout import render_navbar, spacer
from src.ui.inputs import render_inputs
from src.ui.charts import render_chart
from src.ui.tables import render_history_table
from src.ui.advisory import render_advisory

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)

# -------------------------------------------------
# INITIALIZATION
# -------------------------------------------------
inject_styles()
render_navbar(UNIT_LABEL)
init_state()

if "agent_report" not in st.session_state:
    st.session_state.agent_report = None

if "agent_error" not in st.session_state:
    st.session_state.agent_error = None

if "evidence_context" not in st.session_state:
    st.session_state.evidence_context = []

if "evidence_comparables" not in st.session_state:
    st.session_state.evidence_comparables = None

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
pipe, target_transform, train_columns = load_artifacts(MODEL_PATH)

# -------------------------------------------------
# LOAD DATASET
# -------------------------------------------------
try:
    housing_df = pd.read_csv("data/BigHousing.csv")
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

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
  <div class="sub">Click <b>Predict</b> to generate value and advisory.</div>
  <div class="big-number">{("$" + format(latest, ",.0f")) if latest is not None else "—"}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    spacer()

    st.markdown(
        """
<div class="card">
  <div class="h1">Inputs</div>
  <div class="sub">Adjust property features below</div>
</div>
""",
        unsafe_allow_html=True,
    )

    spacer()

    input_values = render_inputs(PRESETS)

    spacer()

    c1, c2 = st.columns([1, 1], gap="small")
    with c1:
        predict_clicked = st.button("Predict")
    with c2:
        clear_clicked = st.button("Clear")

    if clear_clicked:
        clear_state()
        st.session_state.agent_report = None
        st.session_state.agent_error = None
        st.session_state.evidence_context = []
        st.session_state.evidence_comparables = None
        st.rerun()

    if predict_clicked:
        st.session_state.agent_report = None
        st.session_state.agent_error = None
        st.session_state.evidence_context = []
        st.session_state.evidence_comparables = None

        progress = st.progress(0, text="Starting analysis...")

        # -------------------------------
        # STEP 1: MODEL PREDICTION
        # -------------------------------
        try:
            progress.progress(15, text="Preparing property features...")
            input_df = build_input_df(input_values, train_columns)

            progress.progress(35, text="Running ML price prediction...")
            pred = predict_usd(pipe, input_df, target_transform)
            append_history(input_values, pred)

        except Exception as e:
            progress.empty()
            st.error(f"Prediction failed: {e}")
            st.stop()

        # -------------------------------
        # STEP 2: COMPARABLE ANALYSIS
        # -------------------------------
        try:
            progress.progress(55, text="Finding comparable properties...")
            comps = get_comparables(input_values, housing_df)
            st.session_state.evidence_comparables = comps
        except Exception as e:
            comps = f"Comparable analysis unavailable: {e}"
            st.session_state.evidence_comparables = comps

        # -------------------------------
        # STEP 3: AGENT REPORT
        # -------------------------------
        try:
            progress.progress(80, text="Generating advisory report...")
            agent_state = {
                "user_input": input_values,
                "predicted_price": pred,
                "comparable_summary": comps,
                "market_context": [],
                "regulation_context": [],
                "investment_goal": "investment",
                "risk_level": "medium",
                "reasoning": "",
                "recommendation": "",
                "final_report": "",
            }

            agent_state = run_agent(agent_state, housing_df)
            st.session_state.agent_report = agent_state.get("final_report")
            st.session_state.evidence_context = agent_state.get("market_context", [])

            progress.progress(100, text="Analysis complete.")
        except Exception as e:
            st.session_state.agent_error = str(e)
            progress.empty()

        spacer()

with right:
    render_chart(st.session_state.history)

    spacer()

    if st.session_state.agent_error:
        st.error(f"Advisory Error: {st.session_state.agent_error}")

    if st.session_state.agent_report:
        render_advisory(
            report=st.session_state.agent_report,
            comparables=st.session_state.evidence_comparables,
            context_points=st.session_state.evidence_context,
            latest_price=st.session_state.latest_pred,
        )
        spacer()

    render_history_table(st.session_state.history)