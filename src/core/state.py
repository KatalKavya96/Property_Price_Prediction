import streamlit as st

def init_state():
    """Initializes the session state for history and latest prediction."""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "latest_pred" not in st.session_state:
        st.session_state.latest_pred = None

def clear_state():
    """Clears the session state history and latest prediction."""
    st.session_state.history = []
    st.session_state.latest_pred = None

def append_history(values, pred):
    """Appends a new prediction to the history."""
    run_id = len(st.session_state.history) + 1
    new_entry = {"Run": run_id, **values, "PredictedPriceUSD": pred}
    st.session_state.history.append(new_entry)
    st.session_state.latest_pred = pred
