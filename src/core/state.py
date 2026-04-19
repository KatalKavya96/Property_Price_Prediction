import streamlit as st


def init_state():
    """Initialize session state variables"""
    if "history" not in st.session_state:
        st.session_state.history = []

    if "latest_pred" not in st.session_state:
        st.session_state.latest_pred = None


def clear_state():
    """Clear history and latest prediction"""
    st.session_state.history = []
    st.session_state.latest_pred = None


def append_history(values, pred):
    """Append prediction to history"""
    run_id = len(st.session_state.history) + 1

    new_entry = {
        "Run": run_id,
        **values,
        "PredictedPriceUSD": pred,
    }

    st.session_state.history.append(new_entry)
    st.session_state.latest_pred = pred