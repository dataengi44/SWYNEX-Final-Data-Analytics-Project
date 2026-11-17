
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SWYNEX | Retail Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# DASHBOARD STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .main-header {
        font-size: 32px;
        font-weight: 700;
        color: #2563EB;
    }
    .sub-header {
        color: #64748B;
        font-size: 15px;
    }
    div[data-testid="stMetric"] {
        background-color: #F1F5F9;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD CLEANED DATASET
# --------------------------------------------------

DATA_URL = (
    "https://raw.githubusercontent.com/dataengi44/"
    "SWYNEX-Data-Cleaning-Preparation/main/"
    "output/cleaned_online_retail.csv"
)

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)

    data["InvoiceDate"] = pd.to_datetime(
        data["InvoiceDate"], errors="coerce"
    )

    for col in ["Quantity", "UnitPrice", "TotalAmount", "CustomerID"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    return data

st.title("📊 SWYNEX | Online Retail Analytics Dashboard")
st.markdown(
    '<p class="sub-header">Interactive sales performance and customer analytics</p>',
    unsafe_allow_html=True
)

try:
    df = load_data()
except Exception as error:
    st.warning("Could not load the dataset from GitHub. Upload your cleaned CSV below.")
    uploaded_file = st.file_uploader(
        "Upload cleaned_online_retail.csv",
        type=["csv"]
    )

    if uploaded_file is None:
        st.stop()

    df = pd.read_csv(uploaded_file)
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    for col in ["Quantity", "UnitPrice", "TotalAmount", "CustomerID"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select invoice date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

countries = sorted(df["Country"].dropna().unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=countries,
    default=countries
)

transaction_types = sorted(
    df["TransactionType"].dropna().unique().tolist()
)

selected_types = st.sidebar.multiselect(
    "Transaction types for transaction analysis",
    options=transaction_types,
    default=transaction_types
)

# --------------------------------------------------
# APPLY DATE AND COUNTRY FILTERS
# --------------------------------------------------

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = date_range
    end_date = date_range

filtered_df = df[
    (df["InvoiceDate"].dt.date >= start_date) &
    (df["InvoiceDate"].dt.date <= end_date) &
    (df["Country"].isin(selected_countries))
].copy()

# Sales-only data for sales KPIs and charts
sales_df = filtered_df[
    (filtered_df["TransactionType"] == "Sale") &
    (filtered_df["Quantity"] > 0) &
    (filtered_df["UnitPrice"] > 0)
].copy()

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

revenue = sales_df["TotalAmount"].sum()
quantity = sales_df["Quantity"].sum()
orders = sales_df["InvoiceNo"].nunique()
customers = sales_df["CustomerID"].nunique()

aov = revenue / orders if orders > 0 else 0

st.caption(
    f"Showing sales performance from {start_date} to {end_date}. "
    "Sales KPIs include Sale transactions with positive quantities and prices."
)

st.subheader("Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Revenue", f"£{revenue:,.2f}")
c2.metric("Total Orders", f"{orders:,}")
c3.metric("Units Sold", f"{quantity:,.0f}")
c4.metric("Customers", f"{customers:,}")
c5.metric("Average Order Value", f"£{aov:,.2f}")

st.divider()

# --------------------------------------------------
# TAB LAYOUT
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Sales Overview",
    "📦 Products & Countries",
    "👥 Customer Analysis",
    "🔍 Transactions & Quality"
])

# --------------------------------------------------
# TAB 1: SALES OVERVIEW
# --------------------------------------------------

with tab1:

    st.subheader("Monthly Revenue Trend")

    if not sales_df.empty:
        monthly = (
            sales_df.set_index("InvoiceDate")
            .resample("MS")["TotalAmount"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly,
            x="InvoiceDate",
            y="TotalAmount",
            markers=True,
            title="Monthly Sales Revenue",
            labels={
                "InvoiceDate": "Month",
                "TotalAmount": "Revenue (£)"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Revenue by Weekday")

            sales_df["DayName"] = sales_df["InvoiceDate"].dt.day_name()

            day_order = [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ]

            weekday = (
                sales_df.groupby("DayName")["TotalAmount"]
                .sum()
                .reindex(day_order)
                .fillna(0)
                .reset_index()
            )

            fig = px.bar(
                weekday,
                x="DayName",
                y="TotalAmount",
                title="Revenue by Day of Week",
                labels={
                    "DayName": "Weekday",
                    "TotalAmount": "Revenue (£)"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Hourly Sales Distribution")

            sales_df["Hour"] = sales_df["InvoiceDate"].dt.hour

            hourly = (
                sales_df.groupby("Hour")["TotalAmount"]
                .sum()
                .reset_index()
            )

            fig = px.line(
                hourly,
                x="Hour",
                y="TotalAmount",
                markers=True,
                title="Revenue by Hour",
                labels={
                    "Hour": "Hour of Day",
                    "TotalAmount": "Revenue (£)"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No sales transactions match the selected filters.")

# --------------------------------------------------
# TAB 2: PRODUCTS AND COUNTRIES
# --------------------------------------------------

with tab2:

    if not sales_df.empty:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Top 10 Products by Revenue")

            products = (
                sales_df.groupby("Description")["TotalAmount"]
                .sum()
                .nlargest(10)
                .reset_index()
            )

            fig = px.bar(
                products.sort_values("TotalAmount"),
                x="TotalAmount",
                y="Description",
                orientation="h",
                title="Top Products by Revenue",
                labels={
                    "TotalAmount": "Revenue (£)",
                    "Description": "Product"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            st.subheader("Top 10 Countries by Revenue")

            country_sales = (
                sales_df.groupby("Country")["TotalAmount"]
                .sum()
                .nlargest(10)
                .reset_index()
            )

            fig = px.bar(
                country_sales.sort_values("TotalAmount"),
                x="TotalAmount",
                y="Country",
                orientation="h",
                title="Country-wise Revenue",
                labels={
                    "TotalAmount": "Revenue (£)",
                    "Country": "Country"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Product Performance Table")

        product_table = (
            sales_df.groupby("Description")
            .agg(
                Revenue=("TotalAmount", "sum"),
                Units_Sold=("Quantity", "sum"),
                Orders=("InvoiceNo", "nunique")
            )
            .sort_values("Revenue", ascending=False)
            .head(20)
            .reset_index()
        )

        st.dataframe(product_table, use_container_width=True)

    else:
        st.info("No sales transactions available for this selection.")

# --------------------------------------------------
# TAB 3: CUSTOMER ANALYSIS
# --------------------------------------------------

with tab3:

    customer_df = sales_df.dropna(subset=["CustomerID"]).copy()

    if not customer_df.empty:

        customer_summary = (
            customer_df.groupby("CustomerID")
            .agg(
                Revenue=("TotalAmount", "sum"),
                Orders=("InvoiceNo", "nunique"),
                Quantity=("Quantity", "sum")
            )
            .reset_index()
        )

        customer_summary["AverageOrderValue"] = (
            customer_summary["Revenue"] /
            customer_summary["Orders"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Top 10 Customers")

            top_customers = (
                customer_summary.nlargest(10, "Revenue")
            )

            fig = px.bar(
                top_customers.sort_values("Revenue"),
                x="Revenue",
                y=top_customers.sort_values("Revenue")["CustomerID"].astype(str),
                orientation="h",
                title="Highest Revenue Customers",
                labels={
                    "Revenue": "Revenue (£)",
                    "y": "Customer ID"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            st.subheader("Customer Purchase Frequency")

            customer_summary["PurchaseCategory"] = pd.cut(
                customer_summary["Orders"],
                bins=[0, 1, 5, 10, np.inf],
                labels=[
                    "One-time",
                    "2–5 Orders",
                    "6–10 Orders",
                    "Above 10 Orders"
                ]
            )

            frequency = (
                customer_summary["PurchaseCategory"]
                .value_counts()
                .reindex([
                    "One-time", "2–5 Orders",
                    "6–10 Orders", "Above 10 Orders"
                ])
                .fillna(0)
                .reset_index()
            )

            frequency.columns = ["Category", "Customers"]

            fig = px.pie(
                frequency,
                names="Category",
                values="Customers",
                title="Customer Purchase Frequency"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Customer Details")

        st.dataframe(
            customer_summary.nlargest(20, "Revenue"),
            use_container_width=True
        )

    else:
        st.info("No identified customers are available for this selection.")

# --------------------------------------------------
# TAB 4: TRANSACTIONS AND DATA QUALITY
# --------------------------------------------------

with tab4:

    analysis_df = filtered_df[
        filtered_df["TransactionType"].isin(selected_types)
    ]

    st.subheader("Transaction Type Distribution")

    if not analysis_df.empty:

        transaction_summary = (
            analysis_df["TransactionType"]
            .value_counts()
            .reset_index()
        )

        transaction_summary.columns = [
            "TransactionType", "Records"
        ]

        fig = px.bar(
            transaction_summary,
            x="TransactionType",
            y="Records",
            color="TransactionType",
            title="Transaction Type Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Data Quality Flags")

        quality = (
            analysis_df["DataQualityFlag"]
            .value_counts()
            .reset_index()
        )

        quality.columns = ["QualityFlag", "Records"]

        fig = px.pie(
            quality,
            names="QualityFlag",
            values="Records",
            title="Data Quality Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Transaction Summary")

        summary = (
            analysis_df.groupby("TransactionType")
            .agg(
                Records=("InvoiceNo", "count"),
                Orders=("InvoiceNo", "nunique"),
                Quantity=("Quantity", "sum"),
                Amount=("TotalAmount", "sum")
            )
            .reset_index()
        )

        st.dataframe(summary, use_container_width=True)

    else:
        st.info("No transactions match the selected transaction types.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
**SWYNEX Internship – Task 3: Interactive Dashboard**

Built with Python, Streamlit, Pandas and Plotly.

Dataset: Online Retail | Analysis period: 2010–2011
""")
