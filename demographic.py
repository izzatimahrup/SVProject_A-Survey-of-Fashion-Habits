# =========================================================
# STREAMLIT APP: Interactive Fashion Analysis (Plotly)
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fashion Trends Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

df = load_data()

# ---------------------------------------------------------
# SAFETY CLEANING (CRITICAL)
# ---------------------------------------------------------
df["Age"] = df["Age"].astype(str).str.replace("–", "-", regex=False).str.strip()
df["Education Level"] = (
    df["Education Level"]
    .astype(str)
    .str.replace("’", "'", regex=False)
    .str.replace("–", "-", regex=False)
    .str.strip()
)

# ---------------------------------------------------------
# CATEGORY ORDERS
# ---------------------------------------------------------
age_order = [
    "<25 Years Old",
    "26-34 Years Old",
    "35-45 Years Old",
    "46-55 Years Old",
    ">55 Years Old"
]

education_order = [
    "Lower Secondary Education",
    "Secondary Education",
    "Post-Secondary Education",
    "Bachelor's Degree",
    "Master's Degree",
    "Doctoral Degree"
]

expense_order = ["<500", "500-1000", "1000-3000", ">3000"]

# ---------------------------------------------------------
# PAGE TITLE & DESCRIPTION
# ---------------------------------------------------------
st.title("📊 Fashion Demographic & Behavioural Analysis")
st.markdown("Interact with the charts by hovering over them or using the legend to filter data.")

st.subheader("Objective")
st.markdown(
    "To examine how demographic factors relate to consumers’ fashion awareness, "
    "spending behaviour, and shopping influences on social media."
)

# =========================================================
# SUMMARY BOX
# =========================================================
st.subheader("Key Demographic Summary")

c1, c2, c3 = st.columns(3)
total_respondents = len(df)

c1.metric("Total Respondents", total_respondents)
c2.metric("Majority Gender", df["Gender"].value_counts().idxmax())
c3.metric("Majority Region", df["Region"].value_counts().idxmax())

# =========================================================
# SECTION A: DEMOGRAPHIC DATA
# =========================================================
st.header("Section A: Demographic Data Visualisation")

col1, col2 = st.columns(2)

# -------------------------
# Gender Distribution
# -------------------------
gender_counts = (
    df["Gender"]
    .value_counts()
    .reset_index(name="count")
    .rename(columns={"index": "Gender"})
)
fig1 = px.pie(
    gender_counts,
    names="Gender",
    values="count",
    hole=0.4,
    title="Gender Distribution of Respondents"
)
col1.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Age Group Distribution (FIXED)
# -------------------------
age_counts = (
    df["Age"]
    .value_counts()
    .reindex(age_order, fill_value=0)
    .reset_index(name="count")
    .rename(columns={"index": "Age"})
)

fig2 = px.bar(
    age_counts,
    x="Age",
    y="count",
    text_auto=True,
    title="Age Group Distribution",
    category_orders={"Age": age_order}
)
col1.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Employment Status
# -------------------------
employment_counts = df["Employment Status"].value_counts().reset_index(name="count")
fig5 = px.pie(
    employment_counts,
    names="index",
    values="count",
    title="Employment Status Distribution"
)
col2.plotly_chart(fig5, use_container_width=True)

# -------------------------
# Region Distribution
# -------------------------
region_counts = df["Region"].value_counts().reset_index(name="count")
fig3 = px.bar(
    region_counts,
    x="index",
    y="count",
    text_auto=True,
    title="Regional Distribution"
)
col2.plotly_chart(fig3, use_container_width=True)

# -------------------------
# Education Level (FIXED)
# -------------------------
edu_counts = (
    df["Education Level"]
    .value_counts()
    .reindex(education_order, fill_value=0)
    .reset_index(name="count")
    .rename(columns={"index": "Education Level"})
)

fig4 = px.bar(
    edu_counts,
    x="count",
    y="Education Level",
    orientation="h",
    text_auto=True,
    title="Education Level of Respondents",
    category_orders={"Education Level": education_order}
)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# Monthly Expenses
# -------------------------
expense_counts = (
    df["Average Monthly Expenses (RM)"]
    .value_counts()
    .reindex(expense_order, fill_value=0)
    .reset_index(name="count")
    .rename(columns={"index": "Average Monthly Expenses (RM)"})
)

expense_counts["percentage"] = expense_counts["count"] / expense_counts["count"].sum() * 100

fig6 = px.bar(
    expense_counts,
    x="Average Monthly Expenses (RM)",
    y="percentage",
    text=expense_counts["percentage"].map(lambda x: f"{x:.1f}%"),
    title="Distribution of Monthly Fashion Expenses (%)",
    category_orders={"Average Monthly Expenses (RM)": expense_order}
)
st.plotly_chart(fig6, use_container_width=True)

# -------------------------
# Awareness of Fashion Trends
# -------------------------
awareness_counts = df["Awareness of Fashion Trends"].value_counts().sort_index().reset_index(name="count")
awareness_counts["percentage"] = awareness_counts["count"] / awareness_counts["count"].sum() * 100

fig7 = px.bar(
    awareness_counts,
    x="index",
    y="percentage",
    text=awareness_counts["percentage"].map(lambda x: f"{x:.1f}%"),
    title="Awareness of Current Fashion Trends (%)"
)
st.plotly_chart(fig7, use_container_width=True)

# -------------------------
# Influence on Shopping
# -------------------------
influence_counts = df["Influence on Shopping"].value_counts().reset_index(name="count")

fig8 = px.bar(
    influence_counts,
    x="count",
    y="index",
    orientation="h",
    text_auto=True,
    title="Factors Influencing Shopping Decisions"
)
fig8.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig8, use_container_width=True)

# =========================================================
# SECTION B: COMPARATIVE ANALYSIS
# =========================================================
st.divider()
st.header("Section B: Comparative & Behavioural Analysis")

# Gender × Awareness
awareness_gender = df.groupby(["Gender", "Awareness of Fashion Trends"]).size().reset_index(name="Count")
fig9 = px.bar(
    awareness_gender,
    x="Gender",
    y="Count",
    color="Awareness of Fashion Trends",
    barmode="stack",
    title="Awareness of Fashion Trends by Gender"
)
st.plotly_chart(fig9, use_container_width=True)

# Employment × Expenses
emp_expense = df.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
fig10 = px.bar(
    emp_expense,
    x="Employment Status",
    y="Count",
    color="Average Monthly Expenses (RM)",
    barmode="group",
    category_orders={"Average Monthly Expenses (RM)": expense_order},
    title="Monthly Fashion Expenses by Employment Status"
)
st.plotly_chart(fig10, use_container_width=True)

# Gender × Influence
gender_influence = df.groupby(["Gender", "Influence on Shopping"]).size().reset_index(name="Count")
fig11 = px.bar(
    gender_influence,
    x="Count",
    y="Influence on Shopping",
    color="Gender",
    orientation="h",
    barmode="group",
    title="Influence on Shopping by Gender"
)
st.plotly_chart(fig11, use_container_width=True)
