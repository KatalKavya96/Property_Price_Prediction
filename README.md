# Property Price Prediction System

## Overview
This project predicts residential property prices using Machine Learning models such as Linear Regression and Decision Tree Regression.

The goal is to analyse housing features and estimate accurate property prices through data driven modeling.

## Dataset
Dataset Source:
https://www.kaggle.com/datasets/yasserh/housing-prices-dataset

Features include:
- Area
- Bedrooms
- Bathrooms
- Stories
- Parking
- Air Conditioning
- Furnishing Status

Target Variable:
- Price

## Project Structure

data/ → Dataset files  
notebooks/ → Model development and EDA  
models/ → Saved trained models  
app/ → Deployment UI  
reports/ → Final project report  

## Team
- Kavya Katal
- Aabir Sarkar
- Kushagra Maheswari
- Pratyush Chouksey

# Project Log

---

## Step 1 — Dataset Audit

The dataset was loaded and inspected using a Kaggle Notebook environment.

Tasks Performed:
- Verified dataset shape and structure.
- Reviewed column names and feature types.
- Checked for missing values.
- Checked for duplicate records.

Result:
- No missing values detected.
- No duplicate rows found.
- Dataset confirmed clean and ready for analysis.

---

## Step 2 — Exploratory Data Analysis (EDA)

### Price Distribution Analysis

Property price distribution was analyzed to understand overall pricing trends and detect anomalies.

Observation:
Property prices show a slightly right-skewed distribution, indicating the presence of higher-valued properties within the dataset.

Generated Visualization:
- Price Distribution Histogram

---

### Correlation Analysis

Correlation analysis was performed to identify numerical features strongly associated with property prices.

Key Insights:
- Area shows the strongest positive correlation with price (~0.54).
- Bathrooms significantly influence property valuation.
- Number of stories also contributes to higher pricing.
- Multiple independent predictors exist, supporting effective model learning.

Generated Visualization:
- Feature Correlation Heatmap

---

## Step 3 — Feature Encoding and Model Preparation

Machine learning models require numerical inputs; therefore categorical variables were converted into numerical representations.

Encoding Strategy:
- Binary categorical features were mapped using:
  - Yes → 1
  - No → 0
- Furnishing status was ordinally encoded to preserve logical ranking:
  - Unfurnished → 0
  - Semi-Furnished → 1
  - Furnished → 2

Reasoning:
Binary and ordinal encoding were preferred over one-hot encoding to maintain feature interpretability while avoiding unnecessary dimensional expansion.

Outcome:
The dataset is now fully numeric and prepared for machine learning model training.

---

## Step 4 — Train Test Split

The dataset was divided into training and testing subsets to evaluate
model performance on unseen data.

Configuration:
- Training Data: 80%
- Testing Data: 20%
- Random State: 42 (ensures reproducibility)

This step prevents overfitting and enables reliable performance evaluation.

---

## Step 5 — Feature Scaling

Feature scaling was applied to normalize input feature magnitudes before training the Linear Regression model.

Reason:
Housing attributes such as area contain significantly larger numerical values compared to binary features like parking or air conditioning. Scaling ensures that all features contribute proportionally during model learning.

Implementation:
- StandardScaler from Scikit-learn was used.
- Scaling parameters were learned only from the training dataset.
- The same transformation was applied to testing data to prevent data leakage.

Outcome:
Feature distributions were standardized while maintaining dataset consistency for model training.

---

## Step 6 — Linear Regression Model Training

A Linear Regression model was implemented as the baseline prediction model to estimate property prices.

Objective:
To model the linear relationship between housing characteristics and property price.

Process:
- Model trained using scaled training data.
- Predictions generated on unseen test data.

Evaluation Metrics Used:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

Results:
- MAE ≈ 979,679
- RMSE ≈ 1,331,071
- R² Score ≈ 0.65

Insight:
The model successfully captured major pricing trends within the dataset and demonstrated stable generalization performance.

---

## Step 7 — Decision Tree Regression

To capture potential non-linear relationships between housing features and price, a Decision Tree Regressor was implemented.

Motivation:
Decision Trees can model conditional feature relationships that Linear Regression may not capture effectively.

Initial Results:
- MAE ≈ 1,270,788
- RMSE ≈ 1,718,102
- R² Score ≈ 0.41

Observation:
The default Decision Tree showed signs of overfitting and weaker generalization compared to Linear Regression.

---

## Step 8 — Decision Tree Optimization

Hyperparameter tuning was performed to improve Decision Tree performance and reduce overfitting.

Parameters Adjusted:
- Maximum Tree Depth
- Minimum Samples per Split
- Minimum Samples per Leaf

Optimized Results:
- MAE ≈ 1,216,327
- RMSE ≈ 1,610,145
- R² Score ≈ 0.48

Insight:
Although optimization improved performance slightly, Linear Regression continued to outperform Decision Tree Regression for this dataset.

Conclusion:
The housing dataset demonstrates predominantly linear feature relationships.

---

## Step 9 — Model Selection and Final Evaluation

Based on comparative evaluation, Linear Regression was selected as the final prediction model.

Reasoning:
- Higher R² Score.
- Better generalization capability.
- Stable prediction behavior across unseen data.

Additional Evaluation:
Prediction accuracy was analyzed using percentage-based error metrics.

Result:
- Overall Prediction Accuracy ≈ 78%

This indicates that predicted property prices remain close to actual market values within a reasonable deviation range.

---

## Step 10 — Manual Prediction Testing

Manual inference testing was conducted to validate real-world usability of the trained model.

Procedure:
- Custom housing feature values were manually provided as model input.
- Inputs were transformed using the same scaling pipeline used during training.
- Predictions were generated using the trained Linear Regression model.

Example Output:
Predicted Property Price ≈ 6,740,317

Observation:
Model predictions responded logically to feature variations such as area size and available amenities, confirming correct model behavior.

---

## Step 11 — Key Learning and Insights

Key observations from experimentation include:

- Property prices demonstrate strong linear dependence on core housing attributes such as area and number of bathrooms.
- Simpler interpretable models such as Linear Regression can outperform more complex models when dataset relationships are primarily linear.
- Proper preprocessing and evaluation play a critical role in achieving reliable prediction performance.
