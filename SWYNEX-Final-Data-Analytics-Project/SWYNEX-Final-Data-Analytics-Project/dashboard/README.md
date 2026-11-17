
# SWYNEX - Interactive Retail Analytics Dashboard

## Project Overview

This project is an interactive retail analytics dashboard developed as part of Task 3 of the SWYNEX internship.

The dashboard analyzes the Online Retail dataset and presents key business metrics, sales trends, product performance, customer purchasing behaviour, and transaction patterns through interactive visualizations.

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Google Colab

## Dataset

The dashboard uses the cleaned Online Retail dataset prepared during Task 1.

- Total records: 536,641
- Total columns: 11
- Date range: December 2010 – December 2011
- Source: SWYNEX Data Cleaning and Preparation repository

## Dashboard Features

### 1. Key Performance Indicators
- Total Revenue
- Total Orders
- Units Sold
- Identified Customers
- Average Order Value

### 2. Interactive Filters
- Invoice date range
- Country selection
- Transaction type selection

### 3. Sales Overview
- Monthly revenue trend
- Weekday revenue distribution
- Hourly revenue analysis

### 4. Product and Country Analysis
- Top 10 products by revenue
- Top 10 countries by revenue
- Product performance summary

### 5. Customer Analysis
- Top customers by revenue
- Customer purchase frequency
- Customer performance details

### 6. Transaction and Data Quality Analysis
- Transaction type distribution
- Data quality classification
- Transaction summary

## Installation

Install the required libraries:

    pip install -r requirements.txt

Run the dashboard locally:

    streamlit run app.py

## Repository Structure

    SWYNEX-Interactive-Dashboard/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    └── .gitignore

## Task Information

- Internship: SWYNEX Technologies
- Task: Task 3 - Interactive Dashboard
- Domain: Data Analytics
- Dashboard Framework: Streamlit

## Previous Tasks

- Task 1: Data Cleaning and Preparation
- Task 2: Exploratory Data Analysis

## Conclusion

This dashboard transforms retail transaction data into an interactive business analytics tool, helping users explore revenue trends, product performance, customer activity, and transaction quality.
