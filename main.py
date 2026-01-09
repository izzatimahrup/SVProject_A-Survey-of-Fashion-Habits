import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="Fashion Trends Dashboard", layout="wide")

st.title("📊 Fashion Demographic & Behavioral Analysis")
st.markdown("This dashboard visualizes demographic data and consumer shopping influences.")

# --- DATA LOADING ---
# Ensure 'df' is loaded here. 

df = pd.read_csv("https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv")
# For this script to work, df must be defined.

# Create Tabs for Organization
tab1, tab2 = st.tabs(["📋 Demographic Data", "🔄 Cross-Analysis (Bivariate)"])

with tab1:
    st.header("Section A: Demographic Data Visualisation")
    
    # 1. Gender and Employment (Row 1)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1️⃣ Gender Distribution")
        gender_counts = df["Gender"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", 
               startangle=90, wedgeprops={"width": 0.4})
        st.pyplot(fig)

    with col2:
        st.subheader("5️⃣ Employment Status")
        employment_counts = df["Employment Status"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(employment_counts, labels=employment_counts.index, autopct="%1.1f%%", startangle=90)
        st.pyplot(fig)

    # 2. Age Group
    st.subheader("2️⃣ Age Group Distribution")
    age_order = ["<25 Years Old", "26-34 Years Old", "35-45 Years Old", "46-55 Years Old", ">55 Years Old"]
    age_counts = df["Age"].value_counts().reindex(age_order)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=age_counts.index, y=age_counts.values, ax=ax)
    plt.xticks(rotation=20)
    for p in ax.patches:
        ax.annotate(int(p.get_height()), (p.get_x() + p.get_width()/2, p.get_height()), ha="center", va="bottom")
    st.pyplot(fig)

    # 3. Education Level
    st.subheader("4️⃣ Education Level")
    education_order = ["Lower Secondary Education", "Secondary Education", "Post-Secondary Education", 
                       "Bachelor’S Degree", "Master’S Degree", "Doctoral Degree"]
    edu_counts = df["Education Level"].value_counts().reindex(education_order)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=edu_counts.index, x=edu_counts.values, ax=ax)
    for p in ax.patches:
        ax.annotate(int(p.get_width()), (p.get_width(), p.get_y() + p.get_height()/2), va="center")
    st.pyplot(fig)

    # 4. Monthly Expenses & Awareness (Row 3)
    col3, col4 = st.columns(2)
    
    expense_order = ["<500", "500-1000", "1000-3000", ">3000"]
    
    with col3:
        st.subheader("6️⃣ Monthly Fashion Expenses")
        expense_counts = df["Average Monthly Expenses (RM)"].value_counts().reindex(expense_order)
        expense_pct = expense_counts / expense_counts.sum() * 100
        fig, ax = plt.subplots()
        sns.barplot(x=expense_pct.index, y=expense_pct.values, ax=ax)
        for i, v in enumerate(expense_pct.values):
            ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")
        st.pyplot(fig)

    with col4:
        st.subheader("7️⃣ Awareness of Trends")
        awareness_counts = df["Awareness of Fashion Trends"].value_counts().sort_index()
        awareness_pct = awareness_counts / awareness_counts.sum() * 100
        fig, ax = plt.subplots()
        sns.barplot(x=awareness_pct.index, y=awareness_pct.values, ax=ax)
        for i, v in enumerate(awareness_pct.values):
            ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")
        st.pyplot(fig)

with tab2:
    st.header("Section B: Bivariate & Influence Analysis")

    # 1. Gender x Awareness
    st.subheader("Gender × Awareness of Fashion Trends")
    awareness_gender = df.groupby(["Gender", "Awareness of Fashion Trends"]).size().reset_index(name="Count")
    awareness_gender_pivot = awareness_gender.pivot(index="Gender", columns="Awareness of Fashion Trends", values="Count").fillna(0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    awareness_gender_pivot.plot(kind="bar", stacked=True, ax=ax)
    plt.legend(title="Awareness (1-5)", bbox_to_anchor=(1.05, 1))
    st.pyplot(fig)

    # 2. Employment x Expenses
    st.subheader("Employment Status × Monthly Expenses")
    emp_expense = df.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
    emp_expense["Average Monthly Expenses (RM)"] = pd.Categorical(emp_expense["Average Monthly Expenses (RM)"], 
                                                                  categories=expense_order, ordered=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=emp_expense, x="Employment Status", y="Count", hue="Average Monthly Expenses (RM)", ax=ax)
    st.pyplot(fig)

    # 3. Shopping Influences
    st.subheader("Factors Influencing Shopping Decisions")
    influence_counts = df["Influence on Shopping"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=influence_counts.values, y=influence_counts.index, ax=ax)
    for i, v in enumerate(influence_counts.values):
        ax.text(v + 0.5, i, str(v), va="center")
    st.pyplot(fig)
