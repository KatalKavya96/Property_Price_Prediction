# Property Price Prediction System

## Overview
This project predicts residential property prices using Machine Learning.

We trained and compared models, selected the best performer, and deployed it using a Streamlit web app that predicts prices in **USD**.

## Dataset
**Dataset:** Ames Housing (Kaggle “House Prices: Advanced Regression Techniques”)  
**Typical features in the dataset include:**
- Overall quality score
- Living area (square feet)
- Basement area
- Garage capacity
- Year built
- Bathrooms, fireplaces, lot area
- Many categorical features (neighborhood, exterior, heating, etc.)

**Target variable:** SalePrice (USD)

---

## Tech Stack

### Core Language
- Python 3.10+

### Data Processing
- Pandas
- NumPy

### Machine Learning
- Scikit-learn
- Joblib (model serialization)

### Visualization
- Matplotlib / Seaborn (EDA & model comparison plots)

### Deployment
- Streamlit (UI)
- Streamlit Cloud (Hosting)

### Version Control
- Git
- GitHub

---

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/KatalKavya96/Property_Price_Prediction.git
cd Property_Price_Prediction
```

### 2. Create Virtual Environment
python -m venv .venv
source .venv/bin/activate      # Mac/Linux

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run the Streamlit App
streamlit run app.py

## Project Structure
data/ → dataset files (train.csv)  
notebooks/ → training + evaluation notebook  
model/ → saved model artifact (.joblib)  
app.py → Streamlit UI  
requirements.txt → pinned libraries (important for joblib compatibility)  

---

## Team
- Kavya Katal
- Aabir Sarkar
- Kushagra Maheswari
- Pratyush Chouksey

---

# Project Log

## Step 1 — Dataset Audit
We loaded the dataset and checked basic data quality.

Tasks performed:
- Checked dataset shape and column types
- Checked missing values
- Verified target column (SalePrice) exists
- Confirmed numeric + categorical columns are present

Result:
- Missing values exist in several columns (common in Ames Housing).
- We handled missing values inside the preprocessing pipeline.

---

## Step 2 — Train/Validation Split
We split the dataset into:
- Training set (used for learning)
- Validation set (used for evaluation)

Reason:
- Measures generalization on unseen data
- Helps prevent overfitting decisions

---

## Step 3 — Preprocessing Pipeline
Ames Housing has both numeric and categorical data, so we used a **pipeline** to make preprocessing consistent for training and deployment.

Pipeline steps:
- **Numeric columns**
  - Missing value handling (imputation)
  - Scaling (StandardScaler)
- **Categorical columns**
  - Missing value handling
  - One-hot encoding (converts categories into numbers)

Why pipeline?
- Same transformations run during training and Streamlit inference
- Prevents “train vs deploy mismatch”

---

## Step 4 — Target Transformation (log1p)
SalePrice is right-skewed (few very expensive houses).

We trained on:
- `log1p(SalePrice)`

At prediction time, we convert back using:
- `expm1(prediction)`

Why?
- Improves stability
- Reduces impact of outliers
- Often improves accuracy for price prediction

---

## Step 5 — Baseline Model: Linear Regression
We trained **Linear Regression** on processed features with the log target.

Evaluation metrics used:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score

Observation:
- Linear Regression performed best in our comparison (example: R² ≈ 0.93 on validation).
- It generalized better than the more complex model.

---

## Step 6 — Comparison Model: Random Forest
We also trained a Random Forest regressor.

Observation:
- Random Forest performed lower than Linear Regression in our run (example: R² ≈ 0.88).
- This suggests the dataset behaves strongly linear after preprocessing + log transform.

Conclusion:
- Complex model ≠ better model by default.

---

## Step 7 — Final Model Selection
We selected **Linear Regression** because:
- Higher validation R²
- Stable, logical predictions
- Fast inference for UI

---

## Step 8 — Saving the Model (Joblib Artifact)
We saved the complete pipeline (preprocessing + model) using joblib.

Saved artifact contains:
- `pipeline` (ColumnTransformer + LinearRegression)
- `target_transform` = "log1p"
- `train_columns` (to build correct input dataframe in Streamlit)
- (optional) evaluation metrics like MAE/RMSE/R²

Important:
Joblib files require **matching scikit-learn versions** between training and deployment.

Training environment versions:
- scikit-learn: 1.6.1
- joblib: 1.5.3
- numpy: 2.0.2
- pandas: 2.3.3

---

## Step 9 — Streamlit Deployment (USD Output)
We built a dashboard-style Streamlit UI to:
- Collect user inputs (highest impact features first)
- Run inference using the saved pipeline
- Display predicted price in **USD**
- Show useful insights:
  - Sensitivity curve (how price changes when one feature varies)
  - Marginal impact table (how much price changes for a small step)

Deployment logic:
1. Create a 1-row dataframe with training columns
2. Fill available input columns safely
3. Predict using `pipeline.predict()`
4. Convert from log scale back to USD using `expm1()`

---

## Step 10 — Key Learnings
- Pipelines matter more than the model alone.
- Log-transforming the target can improve price prediction.
- Simpler models can outperform complex ones if relationships are linear.
- Deployment needs correct version management (sklearn/joblib compatibility).

---

## Future Improvements (Optional)
- Add more user inputs (Neighborhood, HouseStyle, KitchenQual, etc.)
- Compute a real uncertainty band using validation residuals
- Add explainability (SHAP or coefficient-based breakdown)
- Add input validation and realistic range warnings
