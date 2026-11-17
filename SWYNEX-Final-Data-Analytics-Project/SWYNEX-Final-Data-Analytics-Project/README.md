# SWYNEX Final Data Analytics Project

## End-to-End Online Retail Business Analysis

This project combines data cleaning, exploratory analysis and interactive
dashboard development into one end-to-end retail analytics case study.

## Objectives

- Clean and validate retail transaction data.
- Analyze revenue and sales trends.
- Identify high-performing products and countries.
- Understand customer purchasing behaviour.
- Examine transaction quality.
- Provide business recommendations.

## Tools

Python, Pandas, NumPy, Matplotlib, Plotly, Streamlit and Google Colab.

## Dataset

- 536,641 records
- 11 columns
- December 1, 2010 to December 9, 2011
- Compressed cleaned file: `data/cleaned_online_retail.csv.gz`

## Key Metrics

| Metric | Result |
|---|---:|
| Valid sales records | 524,877 |
| Revenue | £10,631,048.74 |
| Orders | 19,959 |
| Identified customers | 4,338 |
| Products | 3,920 |
| Quantity sold | 5,572,419 |
| Average order value | £532.64 |

## Key Findings

- November 2011 recorded the highest monthly revenue.
- The United Kingdom contributed approximately 84.57% of total revenue.
- Approximately 65.58% of identified customers placed repeat orders.
- PAPER CRAFT, LITTLE BIRDIE recorded the highest quantity sold,
  associated with one order.
- Cancellations, returns and zero-price transactions require separate review.

## Project Structure

```text
SWYNEX-Final-Data-Analytics-Project/
├── data/
│   └── cleaned_online_retail.csv.gz
├── notebooks/
│   ├── 01_Data_Cleaning.ipynb
│   ├── 02_Exploratory_Data_Analysis.ipynb
│   └── 03_Final_Case_Study.ipynb
├── dashboard/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── reports/
│   ├── cleaning_summary.csv
│   └── final_project_metrics.csv
├── visuals/
│   └── charts/
└── README.md
```

## Visualizations

- Monthly Revenue Trend
- Top 10 Countries by Revenue
- Top 10 Products by Revenue
- Customer Purchase Frequency
- Revenue by Weekday
- Revenue by Hour of Day

## Run the Final Case Study

Open `notebooks/03_Final_Case_Study.ipynb` in Google Colab or Jupyter.
Keep the `data` folder in the project directory and execute the cells.

## Run the Streamlit Dashboard

Install dependencies:

```bash
pip install -r dashboard/requirements.txt
```

Launch:

```bash
cd dashboard
streamlit run app.py
```

**Live Dashboard:** Add your verified Streamlit Community Cloud URL here.

## Business Recommendations

- Introduce loyalty programs to encourage repeat purchases.
- Explore markets beyond the United Kingdom.
- Improve inventory planning using historical product demand.
- Prepare campaigns for high-revenue periods.
- Monitor cancellations and unusual transaction quantities.
- Improve completeness of customer information.

## Limitations

- Historical data covers December 2010 to December 2011.
- December 2011 is a partial month.
- Customer analysis excludes missing CustomerID records.
- Return records have zero TotalAmount, so monetary return value cannot
  be determined from this dataset.
- Large orders can affect quantity-based product rankings.

## Conclusion

The project demonstrates the complete analytics workflow, transforming
retail transaction data into meaningful business insights and recommendations.

**Completed as part of the SWYNEX Data Analytics Internship.**
