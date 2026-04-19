import pandas as pd

def get_comparables(user_input, df):
    """
    Find similar properties from dataset
    """
    filtered = df.copy()

    filtered = filtered[
        (abs(filtered["GrLivArea"] - user_input["GrLivArea"]) < 500) &
        (abs(filtered["OverallQual"] - user_input["OverallQual"]) <= 1)
    ]

    if filtered.empty:
        return "No strong comparable properties found."

    avg_price = filtered["SalePrice"].mean()
    min_price = filtered["SalePrice"].min()
    max_price = filtered["SalePrice"].max()

    return f"""
    Based on similar properties:
    - Avg Price: ${avg_price:,.0f}
    - Range: ${min_price:,.0f} - ${max_price:,.0f}
    """