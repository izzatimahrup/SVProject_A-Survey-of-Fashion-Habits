# =========================================================
# STREAMLIT APP: Fashion Demographic & Behavioural Analysis
# ONE PAGE ONLY (NO TABS)
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fashion Trends Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# Page Title & Description
# ---------------------------------------------------------
st.title("📊 Fashion Demographic & Behavioural Analysis")
st.markdown(
    "This dashboard presents an exploratory visual analysis of consumer demographics, "
    "fashion awareness, spending behaviour, and shopping influences on social media."
)

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
df = pd.read_csv(
    "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
)

sns.set(style="whitegrid")

# =========================================================
# SECTION A: DEMOGRAPHIC DATA VISUALISATION
# =========================================================
st.header("Section A: Demographic Data Visualisation")

# ---------------------------------------------------------
# 1️⃣ Gender Distribution — Donut Chart
# ---------------------------------------------------------
st.subheader("Gender Distribution")

gender_counts = df["Gender"].value_counts()

fig, ax = plt.subplots(figsize=(7,7))
ax.pie(
    gender_counts,
    labels=gender_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"width": 0.4}
)
ax.set_title("Gender Distribution of Respondents")
st.pyplot(fig)

# ---------------------------------------------------------
# 2️⃣ Age Group — Ordered Vertical Bar Chart
# ---------------------------------------------------------
st.subheader("Age Group Distribution")

age_order = [
    "<25 Years Old",
    "26-34 Years Old",
    "35-45 Years Old",
    "46-55 Years Old",
    ">55 Years Old"
]

age_counts = df["Age"].value_counts().reindex(age_order)

fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(x=age_counts.index, y=age_counts.values, ax=ax)

ax.set_title("Age Group Distribution of Respondents")
ax.set_xlabel("Age Group")
ax.set_ylabel("Number of Responses")
ax.set_xticklabels(ax.get_xticklabels(), rotation=20)

for p in ax.patches:
    ax.annotate(
        int(p.get_height()),
        (p.get_x() + p.get_width()/2, p.get_height()),
        ha="center", va="bottom"
    )

st.pyplot(fig)

# ---------------------------------------------------------
# 3️⃣ Region — Bar Chart
# ---------------------------------------------------------
st.subheader("Regional Distribution")

region_counts = df["Region"].value_counts()

fig, ax = plt.subplots(figsize=(7,5))
sns.barplot(x=region_counts.index, y=region_counts.values, ax=ax)

ax.set_title("Regional Distribution of Respondents")
ax.set_xlabel("Region")
ax.set_ylabel("Number of Responses")

for p in ax.patches:
    ax.annotate(
        int(p.get_height()),
        (p.get_x() + p.get_width()/2, p.get_height()),
        ha="center", va="bottom"
    )

st.pyplot(fig)

# ---------------------------------------------------------
# 4️⃣ Education Level — Horizontal Ordered Bar Chart
# ---------------------------------------------------------
st.subheader("Education Level Distribution")

education_order = [
    "Lower Secondary Education",
    "Secondary Education",
    "Post-Secondary Education",
    "Bachelor’S Degree",
    "Master’S Degree",
    "Doctoral Degree"
]

edu_counts = df["Education Level"].value_counts().reindex(education_order)

fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(y=edu_counts.index, x=edu_counts.values, ax=ax)

ax.set_title("Education Level of Respondents")
ax.set_xlabel("Number of Responses")
ax.set_ylabel("Education Level")

for p in ax.patches:
    ax.annotate(
        int(p.get_width()),
        (p.get_width(), p.get_y() + p.get_height()/2),
        va="center"
    )

st.pyplot(fig)

# ---------------------------------------------------------
# 5️⃣ Employment Status — Pie Chart
# ---------------------------------------------------------
st.subheader("Employment Status Distribution")

employment_counts = df["Employment Status"].value_counts()

fig, ax = plt.subplots(figsize=(7,7))
ax.pie(
    employment_counts,
    labels=employment_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
ax.set_title("Employment Status of Respondents")
st.pyplot(fig)

# ---------------------------------------------------------
# 6️⃣ Average Monthly Expenses — Ordered Percentage Bar Chart
# ---------------------------------------------------------
st.subheader("Average Monthly Fashion Expenses")

expense_order = ["<500", "500-1000", "1000-3000", ">3000"]

expense_counts = df["Average Monthly Expenses (RM)"].value_counts().reindex(expense_order)
expense_pct = expense_counts / expense_counts.sum() * 100

fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(x=expense_pct.index, y=expense_pct.values, ax=ax)

ax.set_title("Distribution of Monthly Fashion Expenses")
ax.set_xlabel("Expense Range (RM)")
ax.set_ylabel("Percentage of Respondents")

for i, v in enumerate(expense_pct.values):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")

ax.set_ylim(0, expense_pct.max() + 10)
st.pyplot(fig)

# ---------------------------------------------------------
# 7️⃣ Awareness of Fashion Trends — Likert Bar Chart
# ---------------------------------------------------------
st.subheader("Awareness of Fashion Trends")

awareness_counts = df["Awareness of Fashion Trends"].value_counts().sort_index()
awareness_pct = awareness_counts / awareness_counts.sum() * 100

fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(x=awareness_pct.index, y=awareness_pct.values, ax=ax)

ax.set_title("Awareness of Current Fashion Trends")
ax.set_xlabel("Awareness Level (1 = Not Aware, 5 = Extremely Aware)")
ax.set_ylabel("Percentage of Respondents")

for i, v in enumerate(awareness_pct.values):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")

ax.set_ylim(0, awareness_pct.max() + 10)
st.pyplot(fig)

# ---------------------------------------------------------
# 8️⃣ Influence on Shopping Recommendations — Ranked Bar
# ---------------------------------------------------------
st.subheader("Influence on Shopping Recommendations")

influence_counts = df["Influence on Shopping"].value_counts()

fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(x=influence_counts.values, y=influence_counts.index, ax=ax)

ax.set_title("Factors Influencing Shopping Decisions on Social Media")
ax.set_xlabel("Number of Responses")
ax.set_ylabel("Influence Source")

for p in ax.patches:
    ax.annotate(
        int(p.get_width()),
        (p.get_width(), p.get_y() + p.get_height()/2),
        va="center"
    )

st.pyplot(fig)

# =========================================================
# SECTION B: COMPARATIVE & BEHAVIOURAL ANALYSIS
# =========================================================
st.header("Section B: Comparative & Behavioural Analysis")

# ---------------------------------------------------------
# 9️⃣ Gender × Awareness of Fashion Trends
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
ax.legend(title="Awareness Level", bbox_to_anchor=(1.05, 1))

st.pyplot(fig)

# ---------------------------------------------------------
# 🔟 Employment Status × Average Monthly Expenses
# ---------------------------------------------------------
st.subheader("Employment Status vs Average Monthly Expenses")

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
# 1️⃣1️⃣ Gender × Influence on Shopping Recommendations
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
