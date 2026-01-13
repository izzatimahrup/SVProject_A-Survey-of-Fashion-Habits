import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. SETUP
st.set_page_config(page_title="Motivation Analysis Dashboard", layout="wide")
sns.set_style("whitegrid")

@st.cache_data
def load_and_prepare_data():
    # --- CHANGE THIS TO YOUR ACTUAL FILE NAME ---
    file_path = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv" 
    df = pd.read_csv(file_path)
    
    # 2. CLEANING: Remove any hidden spaces from column names
    df.columns = df.columns.str.strip()
    
    # 3. DEFINE QUESTIONS (Must match CSV columns exactly after stripping spaces)
    # If your CSV uses different names, update this list:
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]
    
    # Check if all columns exist; if not, show a helpful list of what IS there
    missing = [q for q in motivation_questions if q not in df.columns]
    if missing:
        st.error(f"Columns not found in CSV: {missing}")
        st.write("Available columns in your file are:", list(df.columns))
        st.stop()

    # 4. PRE-CALCULATE DISTRIBUTION
    # This creates the 'df_motivation_pct' you need for the stacked bar
    df_pct = (
        df[motivation_questions]
        .apply(lambda x: x.value_counts(normalize=True))
        .T.mul(100)
        .fillna(0)
    )
    
    # Ensure 5 columns exist for Likert (1-5)
    for i in range(1, 6):
        if i not in df_pct.columns:
            df_pct[i] = 0
    df_pct = df_pct[[1, 2, 3, 4, 5]] # Sort columns 1 to 5
    df_pct.columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    
    return df, df_pct, motivation_questions

# Initialize Data
df, df_motivation_pct, motivation_questions = load_and_prepare_data()

# 5. DASHBOARD UI
st.title("📊 Motivation Analysis Dashboard")

# Sidebar Filter
if 'Gender' in df.columns:
    df['Gender'] = df['Gender'].astype(str).str.strip()
    selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
    filtered_df = df[df['Gender'].isin(selected_gender)]
else:
    st.sidebar.warning("'Gender' column not found. Showing all data.")
    filtered_df = df

# --- ROW 1: DISTRIBUTION & MEANS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Percentage Distribution")
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    df_motivation_pct.plot(kind='barh', stacked=True, color=colors, ax=ax1, width=0.8)
    ax1.set_xlim(0, 100)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig1)

with col2:
    st.subheader("Mean Agreement Scores")
    means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    sns.barplot(x=means.values, y=means.index, palette='viridis', ax=ax2)
    ax2.set_xlim(0, 5)
    for i, v in enumerate(means.values):
        ax2.text(v + 0.05, i, f'{v:.2f}', va='center')
    st.pyplot(fig2)

# --- ROW 2: GENDER COMPARISON ---
st.divider()
st.subheader("Gender Comparison (Mean Scores)")

if 'Gender' in df.columns and not filtered_df.empty:
    gender_means = filtered_df.groupby('Gender')[motivation_questions].mean().T.reset_index()
    melted = gender_means.melt(id_vars='index', var_name='Gender', value_name='Score')
    
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.pointplot(data=melted, x='Score', y='index', hue='Gender', join=True, 
                  palette={'Female': 'red', 'Male': 'blue'}, ax=ax3)
    ax3.set_xlim(1, 5)
    st.pyplot(fig3)

# --- ROW 3: HEATMAP ---
st.divider()
st.subheader("Correlation Heatmap")
fig4, ax4 = plt.subplots(figsize=(10, 8))
sns.heatmap(filtered_df[motivation_questions].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax4)
st.pyplot(fig4)
