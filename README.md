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

## Project Log

### Step 1 — Dataset Audit
- Loaded dataset into Kaggle Notebook successfully.
- Verified shape, column names, data types, missing values, and duplicates.

### Step 2 - Price Distribution Analysis

We analyze how property prices are distributed across the dataset.
This helps identify skewness and potential outliers.

Observation:
Property prices show a slightly right-skewed distribution,
indicating the presence of high-value properties.

### Step 3 - Correlation Analysis

Correlation helps identify which numerical features strongly influence property prices.

Observation:
Area shows the strongest positive correlation with price.
Bathrooms and number of stories also contribute significantly.