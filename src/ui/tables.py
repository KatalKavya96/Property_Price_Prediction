import streamlit as st
import pandas as pd

def render_history_table(history):
    """Renders the prediction history table, or a placeholder row if empty."""
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

    if not history:
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
        hist_df = pd.DataFrame(history)
        out = hist_df[show_cols].copy()
        out["PredictedPriceUSD"] = out["PredictedPriceUSD"].map(lambda x: f"${x:,.0f}")
        st.dataframe(out, use_container_width=True, hide_index=True)
