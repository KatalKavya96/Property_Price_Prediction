import streamlit as st

def render_navbar(unit_label):
    """Renders the top navigation bar."""
    st.markdown(
        f"""
<div class="container">
  <div class="navbar">
    <div class="brand">
      <div class="brand-dot"></div>
      <div>Property Price Prediction </div>
    </div>
    <div style="color: rgba(255,255,255,.65); font-size:12px;">
      Unit: {unit_label}
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

def spacer():
    """Helper to inject a vertical spacer."""
    st.markdown('<div class="vspace"></div>', unsafe_allow_html=True)
