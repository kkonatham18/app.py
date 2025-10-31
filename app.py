import streamlit as st
import pandas as pd

st.set_page_config(page_title="Transaction Data Analysis", layout="wide")

st.title("Transaction Data Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader("📤 Upload your transactions CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Convert date column if exists
    if 't_date' in df.columns:
        df['t_date'] = pd.to_datetime(df['t_date'], errors='coerce')

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # Dropdown for selecting report
    report_options = [
        "Select Report",
        "Total Sales Amount",
        "Month with Highest Total Sales",
        "Average Transaction Amount per Customer",
        "Trend of Total Sales Over Months",
        "Highest Single Transaction Amount",
        "Top Revenue Service Category",
        "Top Revenue Product",
        "Average Transaction Amount per Service",
        "Unique Customers Count",
        "Top Spending Customers",
        "Average Number of Transactions per Customer",
        "Customers in Multiple Service Categories",
        "Percentage of Repeat Buyers",
        "Product Category with Highest Total Sales",
        "Most Popular Services (by Transaction Count)",
        "Most Purchased Product per Service",
        "Average Transaction per Product Type",
        "High-Spend Services (Above Avg)",
        "State with Highest Total Sales",
        "City with Highest Transactions",
        "Average Spending per State",
        "Popular Services by State",
        "States Buying Most Outdoor Recreation Products",
        "Compare Spending: California vs Texas",
        "Quarter with Highest Sales",
        "Month-wise Total Sales Variation",
        "Total Transactions per Month",
        "Sports Equipment Seasonal Trend",
        "Transactions Done Using Credit",
        "Revenue from Credit Transactions",
        "Credit vs Debit Avg Spending",
        "Top States/Cities for High-Value Marketing",
        "Exercise & Fitness Inventory Check",
        "High Sales but Low Avg Value Categories",
        "Underperforming Service Categories"
    ]

    selected_report = st.selectbox("📈 Choose a report to generate:", report_options)

    # Define each report
    if selected_report == "Total Sales Amount":
        total_sales = df['t_amt'].sum()
        st.metric("💵 Total Sales", f"{total_sales:,.2f}")

    elif selected_report == "Month with Highest Total Sales":
        monthly_sales = df.groupby(df['t_date'].dt.to_period('M'))['t_amt'].sum()
        top_month = monthly_sales.idxmax()
        st.write(f"📅 *Highest Sales Month:* {top_month}")

    elif selected_report == "Average Transaction Amount per Customer":
        avg_per_cust = df.groupby('cust_id')['t_amt'].mean().mean()
        st.metric("Average Transaction per Customer", f"{avg_per_cust:,.2f}")

    elif selected_report == "Trend of Total Sales Over Months":
        monthly_sales = df.groupby(df['t_date'].dt.to_period('M'))['t_amt'].sum().reset_index()
        monthly_sales['t_date'] = monthly_sales['t_date'].astype(str)
        st.line_chart(monthly_sales, x='t_date', y='t_amt')

    elif selected_report == "Highest Single Transaction Amount":
        st.metric("💰 Highest Transaction", f"{df['t_amt'].max():,.2f}")

    elif selected_report == "Top Revenue Service Category":
        top_service = df.groupby('services')['t_amt'].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_service)

    elif selected_report == "Top Revenue Product":
        top_product = df.groupby('products_used')['t_amt'].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_product)

    elif selected_report == "Average Transaction Amount per Service":
        avg_service = df.groupby('services')['t_amt'].mean().sort_values(ascending=False)
        st.bar_chart(avg_service)

    elif selected_report == "Unique Customers Count":
        st.metric("🧍 Unique Customers", df['cust_id'].nunique())

    elif selected_report == "Top Spending Customers":
        top_cust = df.groupby('cust_id')['t_amt'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_cust)

    elif selected_report == "Average Number of Transactions per Customer":
        avg_txn = df.groupby('cust_id').size().mean()
        st.metric("📦 Avg Transactions per Customer", round(avg_txn, 2))

    elif selected_report == "Customers in Multiple Service Categories":
        multi_service = df.groupby('cust_id')['services'].nunique().gt(1).sum()
        st.write(f"👥 Customers in multiple categories: {multi_service}")

    elif selected_report == "Percentage of Repeat Buyers":
        repeat = (df.groupby('cust_id').size() > 1).sum()
        pct = (repeat / df['cust_id'].nunique()) * 100
        st.metric("Repeat Buyers (%)", f"{pct:.2f}")

    elif selected_report == "Product Category with Highest Total Sales":
        top_product = df.groupby('products_used')['t_amt'].sum().sort_values(ascending=False).head(1)
        st.bar_chart(top_product)

    elif selected_report == "Most Popular Services (by Transaction Count)":
        st.bar_chart(df['services'].value_counts().head(10))

    elif selected_report == "Most Purchased Product per Service":
        result = df.groupby('services')['products_used'].agg(lambda x: x.value_counts().idxmax())
        st.write(result)

    elif selected_report == "Average Transaction per Product Type":
        avg_prod = df.groupby('products_used')['t_amt'].mean().sort_values(ascending=False)
        st.bar_chart(avg_prod)

    elif selected_report == "High-Spend Services (Above Avg)":
        avg_amt = df['t_amt'].mean()
        high_spend = df.groupby('services')['t_amt'].mean()
        st.write(high_spend[high_spend > avg_amt])

    elif selected_report == "State with Highest Total Sales":
        top_state = df.groupby('state')['t_amt'].sum().sort_values(ascending=False).head(1)
        st.bar_chart(top_state)

    elif selected_report == "City with Highest Transactions":
        st.bar_chart(df['city'].value_counts().head(1))

    elif selected_report == "Average Spending per State":
        avg_state = df.groupby('state')['t_amt'].mean()
        st.bar_chart(avg_state)

    elif selected_report == "Popular Services by State":
        combo = df.groupby(['state', 'services']).size().reset_index(name='count')
        st.dataframe(combo.sort_values('count', ascending=False).head(10))

    elif selected_report == "States Buying Most Outdoor Recreation Products":
        outdoor = df[df['products_used'].str.contains('Outdoor', case=False, na=False)]
        outdoor_state = outdoor.groupby('state')['t_amt'].sum().sort_values(ascending=False)
        st.bar_chart(outdoor_state.head(5))

    elif selected_report == "Compare Spending: California vs Texas":
        avg_CA = df[df['state'].str.contains('CA|California', case=False, na=False)]['t_amt'].mean()
        avg_TX = df[df['state'].str.contains('TX|Texas', case=False, na=False)]['t_amt'].mean()
        compare = pd.DataFrame({'State': ['California', 'Texas'], 'Avg_Spending': [avg_CA, avg_TX]})
        st.bar_chart(compare.set_index('State'))

    elif selected_report == "Quarter with Highest Sales":
        quarter_sales = df.groupby(df['t_date'].dt.to_period('Q'))['t_amt'].sum()
        st.write(f"📆 Highest Sales Quarter: {quarter_sales.idxmax()}")

    elif selected_report == "Month-wise Total Sales Variation":
        monthly = df.groupby(df['t_date'].dt.month)['t_amt'].sum()
        st.bar_chart(monthly)

    elif selected_report == "Total Transactions per Month":
        monthly_txn = df.groupby(df['t_date'].dt.month).size()
        st.bar_chart(monthly_txn)

    elif selected_report == "Sports Equipment Seasonal Trend":
        sports = df[df['products_used'].str.contains('Sport|Equipment', case=False, na=False)]
        sports_month = sports.groupby(sports['t_date'].dt.month)['t_amt'].sum()
        st.bar_chart(sports_month)

    elif selected_report == "Transactions Done Using Credit":
        credit = df[df['t_details'].str.contains('credit', case=False, na=False)]
        st.metric("Credit Transactions", len(credit))

    elif selected_report == "Revenue from Credit Transactions":
        credit = df[df['t_details'].str.contains('credit', case=False, na=False)]
        st.metric("Credit Revenue", f"{credit['t_amt'].sum():,.2f}")

    elif selected_report == "Credit vs Debit Avg Spending":
        credit_avg = df[df['t_details'].str.contains('credit', case=False, na=False)]['t_amt'].mean()
        debit_avg = df[df['t_details'].str.contains('debit', case=False, na=False)]['t_amt'].mean()
        comp = pd.DataFrame({'Type': ['Credit', 'Debit'], 'Average': [credit_avg, debit_avg]})
        st.bar_chart(comp.set_index('Type'))

    elif selected_report == "Top States/Cities for High-Value Marketing":
        top_state = df.groupby('state')['t_amt'].mean().sort_values(ascending=False).head(5)
        st.bar_chart(top_state)

    elif selected_report == "Exercise & Fitness Inventory Check":
        ex_sales = df[df['services'].str.contains('Exercise', case=False, na=False)]['t_amt'].sum()
        st.metric("Exercise & Fitness Sales", f"{ex_sales:,.2f}")

    elif selected_report == "High Sales but Low Avg Value Categories":
        sales = df.groupby('products_used')['t_amt'].sum()
        avg = df.groupby('products_used')['t_amt'].mean()
        overall_avg = df['t_amt'].mean()
        high_sales = sales[sales > sales.quantile(0.75)]
        low_avg = avg[avg < overall_avg]
        result = high_sales.index.intersection(low_avg.index)
        st.write(result)

    elif selected_report == "Underperforming Service Categories":
        sales = df.groupby('services')['t_amt'].sum()
        count = df['services'].value_counts()
        low_sales = sales[sales < sales.quantile(0.25)].index
        low_count = count[count < count.quantile(0.25)].index
        underperforming = list(set(low_sales) & set(low_count))
        st.write(underperforming)

else:
    st.info("👆 Please upload a CSV file to start the analysis.")
