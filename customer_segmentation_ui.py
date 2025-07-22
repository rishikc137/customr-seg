import streamlit as st
import pandas as pd
import plotly.express as px
from joblib import load

# Load preprocessed data
copy_df = load('customer_data_df.joblib')  # Make sure this file exists

st.title("🧑‍🤝‍🧑 Customer Segmentation Dashboard")

st.sidebar.header("Filters")

# Age Group Filter
age_groups = copy_df['age_group'].dropna().unique()
age_filter = st.sidebar.multiselect("Select Age Group:", options=age_groups, default=age_groups)

# Gender Filter
genders = copy_df['gender'].dropna().unique()
gender_filter = st.sidebar.multiselect("Select Gender:", options=genders, default=genders)

# Income Bracket Filter
income_brackets = copy_df['income_bracket'].dropna().unique()
income_filter = st.sidebar.multiselect("Select Income Bracket:", options=income_brackets, default=income_brackets)

# Filter the data
filtered_df = copy_df[
    (copy_df['age_group'].isin(age_filter)) &
    (copy_df['gender'].isin(gender_filter)) &
    (copy_df['income_bracket'].isin(income_filter))
]

st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("👥 Customers", f"{len(filtered_df):,}")
col2.metric("💸 Total Spending", f"${filtered_df['total_spent'].sum():,.2f}")
col3.metric("🛒 Avg Order", f"${filtered_df['total_spent'].mean():,.2f}")

# Visualizations
st.subheader("📈 Customer Segmentation Visuals")

# Age Group Distribution
age_counts = filtered_df['age_group'].value_counts().reset_index()
age_counts.columns = ['Age Group', 'Customer Count']

fig_age = px.bar(age_counts, x='Age Group', y='Customer Count',
                 color='Age Group', title='Age Group Distribution')
st.plotly_chart(fig_age, use_container_width=True)

# Gender Distribution
gender_counts = filtered_df['gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Customer Count']

fig_gender = px.pie(gender_counts, names='Gender', values='Customer Count',
                    title='Gender Distribution', hole=0.4)
st.plotly_chart(fig_gender, use_container_width=True)

# Income Bracket Distribution
income_counts = filtered_df['income_bracket'].value_counts().reset_index()
income_counts.columns = ['Income Bracket', 'Customer Count']

fig_income = px.bar(income_counts, x='Income Bracket', y='Customer Count',
                    color='Income Bracket', title='Income Bracket Distribution')
st.plotly_chart(fig_income, use_container_width=True)

# Show Data
st.subheader("🔍 View Data (Filtered)")
st.dataframe(filtered_df)

