# house-price-prediction
A machine learning project that predicts house prices using the XGBoost Regressor on the King County housing dataset. The project includes end-to-end ML pipeline from data preprocessing to model training and deployment using a Streamlit web application.

🏠 House Price Prediction using XGBoost & Streamlit
📌 Overview

This project is a Machine Learning-based House Price Prediction System built using the King County housing dataset.
It uses an XGBoost Regressor model to predict house prices based on various features like number of bedrooms, bathrooms, square footage, location, and more.

A Streamlit web app is also built to provide a simple and interactive UI for real-time predictions.

🚀 Live Features
📊 End-to-end ML pipeline (data → training → prediction)
🤖 XGBoost Regressor for high accuracy predictions
🧹 Data preprocessing and feature handling
💾 Model saving using Joblib (.pkl files)
🖥️ Interactive Streamlit web application
📥 User input-based real-time price prediction


📂 Dataset
Name: King County House Sales Dataset
Source: Kaggle
Target Variable: price
Features include:
Bedrooms
Bathrooms
Sqft Living
Floors
Waterfront
Condition
Grade
Location (Latitude, Longitude, Zipcode)
And more...


🧠 Machine Learning Model
Algorithm: XGBoost Regressor
Why XGBoost?
High accuracy
Handles complex relationships
Works well with structured/tabular data


📊 Model Performance
Mean Absolute Error (MAE): ~Low error range after tuning
Root Mean Squared Error (RMSE): Optimized
R² Score: ~0.80 – 0.90 (varies based on tuning)
🛠️ Tech Stack
Python 🐍
Pandas & NumPy
Scikit-learn
XGBoost
Streamlit
Joblib