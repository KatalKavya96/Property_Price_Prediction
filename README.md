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
