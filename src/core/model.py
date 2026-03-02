import math
import joblib
import numpy as np
import pandas as pd
import streamlit as st

def load_artifacts(model_path):
    """Loads the model pipeline, target transform, and training columns."""
    try:
        artifacts = joblib.load(model_path)
        pipe = artifacts.get("pipeline")
        target_transform = artifacts.get("target_transform", None)
        train_columns = artifacts.get("train_columns", None)

        if train_columns is None:
            st.error("Artifact missing 'train_columns'. Re-save the model with train_columns included.")
            st.stop()
            
        return pipe, target_transform, train_columns
    except Exception as e:
        st.error(f"Failed to load model artifacts: {e}")
        st.stop()

def build_input_df(values, train_columns):
    """Builds a DataFrame from input values, ensuring correct dtypes."""
    # Create a DataFrame with all training columns initialized to 0.0 (float)
    df = pd.DataFrame([{col: 0.0 for col in train_columns}], dtype=float)
    
    # Update values and ensure they are floats
    for k, v in values.items():
        if k in df.columns:
            df.loc[0, k] = float(v)
            
    return df

def predict_usd(pipe, df, target_transform):
    """Generates a prediction and handles inverse transformation if needed."""
    try:
        pred_raw = float(pipe.predict(df)[0])
        pred = float(np.expm1(pred_raw)) if target_transform == "log1p" else pred_raw
        
        if not math.isfinite(pred) or pred < 0:
            raise ValueError("Invalid prediction value generated")
            
        return pred
    except Exception as e:
        raise ValueError(f"Prediction logic failed: {e}")
