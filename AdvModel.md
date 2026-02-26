### LOGS

## Step 1 — Ames Dataset Selection

To improve model performance and demonstrate advanced
data preprocessing techniques, the Ames Housing Dataset
was selected.

The dataset contains 81 property-related features and
requires significant missing value handling and encoding,
making it suitable for real-world machine learning analysis.

---

## Step 2 — Dataset Audit and Missing Value Analysis

The dataset was loaded into a Kaggle Notebook and inspected
to understand its structure and data quality.

Tasks Performed:
- Verified dataset shape, column names, and data types.
- Identified missing values across all columns.
- Calculated missing value counts and missing value percentages.

Key Findings:
- Several columns contained very high missing percentages.
- Many missing values represent absence of amenities/features
  (e.g., no pool, no alley access) rather than data errors.

Outcome:
The dataset required a structured missing value strategy
before model training.

---

## Step 3 — Dropping Highly Sparse Columns

Columns with extremely high missing percentages (nearly all values missing)
were removed to reduce noise and unnecessary preprocessing complexity.

Dropped Columns:
- PoolQC
- MiscFeature
- Alley
- Fence

Reasoning:
These columns contained insufficient information for reliable learning
and could negatively impact model stability and generalization.

Outcome:
Dataset dimensionality was reduced while preserving useful predictive features.

---

## Step 4 — Missing Value Imputation (Median & Mode)

After removing sparse features, remaining missing values were filled
based on feature data type.

Imputation Strategy:
- Numerical columns → Median imputation (robust to outliers)
- Categorical columns → Mode imputation (preserves most frequent category)

Reasoning:
Median imputation prevents distortion from extreme property values,
while mode imputation maintains dominant category distributions.

Outcome:
All remaining missing values were handled successfully, resulting in a
fully clean dataset ready for encoding and model training.

## Step 5 — Feature Encoding

Categorical attributes were transformed using One-Hot Encoding
to convert non-numeric property characteristics into numerical form.

The first category level was dropped during encoding to avoid
multicollinearity and improve regression model stability.

The dataset is now fully numerical and suitable for machine
learning model training.

## Step 6 — Target Variable Transformation

The target variable SalePrice showed right-skewed
distribution due to the presence of high-value properties.

Logarithmic transformation was applied to normalize
the distribution and improve regression model performance.

## Step 7 — Linear Regression Training

A Linear Regression model was trained as a baseline
prediction model.

Performance evaluation was conducted using MAE,
RMSE, and R² metrics to measure prediction accuracy
on unseen test data.