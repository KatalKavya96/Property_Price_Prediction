import streamlit as st
from src.config import PAGE_TITLE, LAYOUT, MODEL_PATH, UNIT_LABEL, PRESETS
from src.assets.styles import inject_styles
from src.core.model import load_artifacts, build_input_df, predict_usd
from src.core.state import init_state, clear_state, append_history
from src.ui.layout import render_navbar, spacer
from src.ui.inputs import render_inputs
from src.ui.charts import render_chart
from src.ui.tables import render_history_table

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

# -------------------------------------------------
# LOAD MODEL ARTIFACTS
# -------------------------------------------------
pipe, target_transform, train_columns = load_artifacts(MODEL_PATH)

# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------
left, right = st.columns([1.05, 1.4], gap="large")

with left:
    # Latest Prediction Box
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

    spacer()

    # Inputs Section Header
    st.markdown(
        """
<div class="card">
  <div class="h1">Inputs</div>
  <div class="sub">Adjust values on the main page (no sidebar).</div>
</div>
""",
        unsafe_allow_html=True,
    )

    spacer()

    # Input Widgets
    input_values = render_inputs(PRESETS)

    spacer()

    # Action Buttons
    c1, c2 = st.columns([1, 1], gap="small")
    with c1:
        predict_clicked = st.button("Predict")
    with c2:
        clear_clicked = st.button("Clear chart")

    if clear_clicked:
        clear_state()
        st.rerun()

    if predict_clicked:
        try:
            input_df = build_input_df(input_values, train_columns)
            pred = predict_usd(pipe, input_df, target_transform)
            append_history(input_values, pred)
            st.rerun()
        except Exception as e:
            st.error(f"Prediction failed: {e}")

with right:
    # Chart Section
    render_chart(st.session_state.history)

    spacer()

    # History Table Section
    render_history_table(st.session_state.history)
