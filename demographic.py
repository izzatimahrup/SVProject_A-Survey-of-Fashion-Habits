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

# Custom Sort Orders
age_order = ["<25 Years Old", "26-34 Years Old", "35-45 Years Old", "46-55 Years Old", ">55 Years Old"]
education_order = ["Lower Secondary Education", "Secondary Education", "Post-Secondary Education", "Bachelor’S Degree", "Master’S Degree", "Doctoral Degree"]
expense_order = ["<500", "500-1000", "1000-3000", ">3000"]

# ---------------------------------------------------------
# Page Title & Description
# ---------------------------------------------------------
st.title("📊 Fashion Demographic & Behavioural Analysis")
st.markdown("Interact with the charts by hovering over them or using the legend to filter data.")

st.subheader("Objective")

st.markdown(
    "To examine how demographic factors relate to consumers’ fashion awareness, "
    "spending behaviour, and shopping influences on social media."
)
# =========================================================
# SUMMARY BOX: RESPONDENT PROFILE OVERVIEW
# =========================================================

st.subheader("Respondent Profile Overview")

col1, col2, col3 = st.columns(3)

# -------------------------
# Total Respondents
# -------------------------
total_respondents = len(df)

col1.metric(
    label="Total Respondents",
    value=f"{total_respondents}",
    help="Total number of valid survey responses"
)

# -------------------------
# Gender Distribution
# -------------------------
gender_counts = df["Gender"].value_counts()
gender_summary = " | ".join(
    [f"{g}: {(c/total_respondents)*100:.1f}%" for g, c in gender_counts.items()]
)

col2.metric(
    label="Gender Distribution",
    value=gender_summary,
    help="Percentage distribution by gender"
)

# -------------------------
# Region Distribution
# -------------------------
region_counts = df["Region"].value_counts()
region_summary = " | ".join(
    [f"{r}: {(c/total_respondents)*100:.1f}%" for r, c in region_counts.items()]
)

col3.metric(
    label="Region Distribution",
    value=region_summary,
    help="Percentage distribution by region"
)
# =========================================================
# SECTION A: DEMOGRAPHIC DATA VISUALISATION
# =========================================================
st.header("Section A: Demographic Data Visualisation")

col1, col2 = st.columns(2)

with col1:
    # 1️⃣ Gender Distribution — Donut Chart
    gender_counts = df["Gender"].value_counts().reset_index()
    fig1 = px.pie(gender_counts, values='count', names='Gender', hole=0.4,
                 title="Gender Distribution of Respondents")
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Age Group — Ordered Vertical Bar Chart
    age_counts = df["Age"].value_counts().reindex(age_order).reset_index()
    fig2 = px.bar(age_counts, x='Age', y='count', text_auto=True,
                 title="Age Group Distribution",
                 category_orders={"Age": age_order})
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    # 5️⃣ Employment Status — Pie Chart
    employment_counts = df["Employment Status"].value_counts().reset_index()
    fig5 = px.pie(employment_counts, values='count', names='Employment Status',
                 title="Employment Status Distribution")
    st.plotly_chart(fig5, use_container_width=True)

    # 3️⃣ Region — Bar Chart
    region_counts = df["Region"].value_counts().reset_index()
    fig3 = px.bar(region_counts, x='Region', y='count', text_auto=True,
                 title="Regional Distribution")
    st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Education Level — Horizontal Ordered Bar Chart
edu_counts = df["Education Level"].value_counts().reindex(education_order).reset_index()
fig4 = px.bar(edu_counts, x='count', y='Education Level', orientation='h', text_auto=True,
             title="Education Level of Respondents",
             category_orders={"Education Level": education_order})
st.plotly_chart(fig4, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    # 6️⃣ Average Monthly Expenses — Ordered Percentage Bar Chart
    expense_counts = df["Average Monthly Expenses (RM)"].value_counts().reindex(expense_order).reset_index()
    expense_counts['percentage'] = (expense_counts['count'] / expense_counts['count'].sum()) * 100
    fig6 = px.bar(expense_counts, x='Average Monthly Expenses (RM)', y='percentage', 
                 text=expense_counts['percentage'].apply(lambda x: f'{x:.1f}%'),
                 title="Distribution of Monthly Fashion Expenses (%)",
                 category_orders={"Average Monthly Expenses (RM)": expense_order})
    st.plotly_chart(fig6, use_container_width=True)

with col4:
    # 7️⃣ Awareness of Fashion Trends — Likert Bar Chart
    awareness_counts = df["Awareness of Fashion Trends"].value_counts().sort_index().reset_index()
    awareness_counts['percentage'] = (awareness_counts['count'] / awareness_counts['count'].sum()) * 100
    fig7 = px.bar(awareness_counts, x='Awareness of Fashion Trends', y='percentage',
                 text=awareness_counts['percentage'].apply(lambda x: f'{x:.1f}%'),
                 title="Awareness of Current Fashion Trends (%)")
    st.plotly_chart(fig7, use_container_width=True)

# 8️⃣ Influence on Shopping Recommendations — Ranked Bar
influence_counts = df["Influence on Shopping"].value_counts().reset_index()
fig8 = px.bar(influence_counts, x='count', y='Influence on Shopping', orientation='h', text_auto=True,
             title="Factors Influencing Shopping Decisions")
fig8.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig8, use_container_width=True)

# =========================================================
# SECTION B: COMPARATIVE & BEHAVIOURAL ANALYSIS
# =========================================================
st.divider()
st.header("Section B: Comparative & Behavioural Analysis")

# 9️⃣ Gender × Awareness of Fashion Trends (Stacked)
awareness_gender = df.groupby(["Gender", "Awareness of Fashion Trends"]).size().reset_index(name="Count")
fig9 = px.bar(awareness_gender, x="Gender", y="Count", color="Awareness of Fashion Trends", 
             title="Awareness of Fashion Trends by Gender (Stacked)",
             barmode="stack")
st.plotly_chart(fig9, use_container_width=True)

# 🔟 Employment Status × Average Monthly Expenses (Grouped)
emp_expense = df.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
fig10 = px.bar(emp_expense, x="Employment Status", y="Count", color="Average Monthly Expenses (RM)",
              title="Monthly Fashion Expenses by Employment Status",
              barmode="group", category_orders={"Average Monthly Expenses (RM)": expense_order})
st.plotly_chart(fig10, use_container_width=True)

# 1️⃣1️⃣ Gender × Influence (Grouped Horizontal)
gender_influence = df.groupby(["Gender", "Influence on Shopping"]).size().reset_index(name="Count")
fig11 = px.bar(gender_influence, x="Count", y="Influence on Shopping", color="Gender",
              orientation='h', barmode='group', title="Influence on Shopping by Gender")
st.plotly_chart(fig11, use_container_width=True)

# 1️⃣2️⃣ Gender × Average Monthly Expenses
gender_expense = df.groupby(["Gender", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
fig12 = px.bar(gender_expense, x="Gender", y="Count", color="Average Monthly Expenses (RM)",
              title="Average Monthly Fashion Expenses by Gender", barmode='group',
              category_orders={"Average Monthly Expenses (RM)": expense_order})
st.plotly_chart(fig12, use_container_width=True)

# 1️⃣3️⃣ Average Monthly Expenses × Influence
expense_influence = df.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count")
fig13 = px.bar(expense_influence, x="Count", y="Influence on Shopping", color="Average Monthly Expenses (RM)",
              orientation='h', barmode='group', title="Influence by Monthly Expense Level",
              category_orders={"Average Monthly Expenses (RM)": expense_order})
st.plotly_chart(fig13, use_container_width=True)
