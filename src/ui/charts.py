import streamlit as st
import pandas as pd
import numpy as np

def render_chart(history):
    """Renders the line chart of prediction history, or a placeholder if empty."""
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

    if not history:
        empty_chart = pd.DataFrame({"PredictedPriceUSD": [np.nan, np.nan]}, index=[1, 2])
        st.line_chart(empty_chart, height=280, use_container_width=True)
        st.caption("No points yet — click **Predict** to plot values.")
    else:
        hist_df = pd.DataFrame(history)
        chart_df = hist_df[["Run", "PredictedPriceUSD"]].set_index("Run")
        st.line_chart(chart_df, height=280, use_container_width=True)
