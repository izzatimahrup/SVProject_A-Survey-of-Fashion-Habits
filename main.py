# =========================================================
# STREAMLIT APP: Fashion Demographic & Behavioural Analysis
# ONE PAGE ONLY (NO TABS)
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# Page Configuration (THIS DOES NOT CREATE A NEW TAB)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fashion Trends Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# Page Title & Description (TOP OF SAME PAGE)
# ---------------------------------------------------------
st.title("📊 Fashion Demographic & Behavioural Analysis")
st.markdown(
    "This dashboard presents an exploratory visual analysis of consumer demographics, "
    "fashion awareness, spending behaviour, and shopping influences on social media."
)

# ---------------------------------------------------------
# DATA LOADING (STILL SAME PAGE)
# ---------------------------------------------------------
df = pd.read_csv(
    "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
)

sns.set(style="whitegrid")

# =========================================================
# SECTION 8: DEMOGRAPHIC & BEHAVIOURAL DATA VISUALISATION
# =========================================================
st.header("Section 8: Demographic & Behavioural Data Visualisation")

# ---------------------------------------------------------
# 1️⃣ Gender × Awareness of Fashion Trends
# Stacked Bar Chart (Likert-style)
# ---------------------------------------------------------
st.subheader("Gender vs Awareness of Fashion Trends")

awareness_gender = (
    df.groupby(["Gender", "Awareness of Fashion Trends"])
      .size()
      .reset_index(name="Count")
)

awareness_gender_pivot = awareness_gender.pivot(
    index="Gender",
    columns="Awareness of Fashion Trends",
    values="Count"
).fillna(0)

fig, ax = plt.subplots(figsize=(9,6))
awareness_gender_pivot.plot(kind="bar", stacked=True, ax=ax)

ax.set_title("Awareness of Fashion Trends by Gender")
ax.set_xlabel("Gender")
ax.set_ylabel("Number of Responses")
ax.legend(title="Awareness Level (1 = Low, 5 = High)", bbox_to_anchor=(1.05, 1))

st.pyplot(fig)

# ---------------------------------------------------------
# 2️⃣ Employment Status × Average Monthly Expenses
# Grouped Bar Chart
# ---------------------------------------------------------
st.subheader("Employment Status vs Average Monthly Fashion Expenses")

expense_order = ["<500", "500-1000", "1000-3000", ">3000"]

emp_expense = (
    df.groupby(["Employment Status", "Average Monthly Expenses (RM)"])
      .size()
      .reset_index(name="Count")
)

emp_expense["Average Monthly Expenses (RM)"] = pd.Categorical(
    emp_expense["Average Monthly Expenses (RM)"],
    categories=expense_order,
    ordered=True
)

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    data=emp_expense,
    x="Employment Status",
    y="Count",
    hue="Average Monthly Expenses (RM)",
    ax=ax
)

ax.set_title("Average Monthly Fashion Expenses by Employment Status")
ax.set_xlabel("Employment Status")
ax.set_ylabel("Number of Responses")
ax.legend(title="Monthly Expense Range (RM)")

st.pyplot(fig)

# ---------------------------------------------------------
# 3️⃣ Influence on Shopping Recommendations (Standalone)
# Ranked Horizontal Bar Chart
# ---------------------------------------------------------
st.subheader("Influence on Shopping Recommendations")

influence_counts = df["Influence on Shopping"].value_counts()

fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(
    x=influence_counts.values,
    y=influence_counts.index,
    ax=ax
)

ax.set_title("Factors Influencing Shopping Decisions on Social Media")
ax.set_xlabel("Number of Responses")
ax.set_ylabel("Influence Source")

for i, v in enumerate(influence_counts.values):
    ax.text(v + 0.5, i, str(v), va="center")

st.pyplot(fig)

# ---------------------------------------------------------
# 4️⃣ Gender × Influence on Shopping Recommendations
# Horizontal Grouped Bar Chart
# ---------------------------------------------------------
st.subheader("Gender vs Influence on Shopping Recommendations")

gender_influence = (
    df.groupby(["Gender", "Influence on Shopping"])
      .size()
      .reset_index(name="Count")
)

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    data=gender_influence,
    x="Count",
    y="Influence on Shopping",
    hue="Gender",
    ax=ax
)

ax.set_title("Influence on Shopping Recommendations by Gender")
ax.set_xlabel("Number of Responses")
ax.set_ylabel("Influence Source")
ax.legend(title="Gender")

st.pyplot(fig)
