import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Motivation Analysis Dashboard", layout="wide")

st.title("📊 Motivation Questions Analysis Dashboard")
st.markdown("This dashboard visualizes survey response distributions, mean scores, and correlations.")

# --- MOCK DATA LOADER (Replace this with your actual data loading) ---
# df = pd.read_csv("your_data.csv")
# For the sake of the example, I'm assuming 'df' and 'df_motivation_pct' are already defined.
# If you are running this from scratch, ensure your DataFrame 'df' is loaded here.

motivation_questions = [
    'follow_for_updates_promotions',
    'follow_because_like_products',
    'follow_because_entertaining',
    'follow_because_discounts_contests',
    'follow_because_express_personality',
    'follow_because_online_community',
    'follow_because_support_loyalty'
]

# --- Sidebar Filters (Example) ---
st.sidebar.header("Filter Options")
selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
filtered_df = df[df['Gender'].isin(selected_gender)]

# --- Row 1: Distribution and Means ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Percentage Distribution")
    # Preparation for Stacked Bar
    df_motivation_pct_positive = df_motivation_pct.copy()
    for col in ['Strongly Disagree', 'Disagree']:
        if col in df_motivation_pct_positive.columns:
            df_motivation_pct_positive[col] = df_motivation_pct_positive[col].abs()

    plot_columns_positive = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    colors_positive = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

    fig1, ax1 = plt.subplots(figsize=(10, 8))
    df_motivation_pct_positive[plot_columns_positive].plot(
        kind='barh', stacked=True, color=colors_positive, ax=ax1, width=0.8
    )
    ax1.set_xlim(0, 100)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig1)

with col2:
    st.subheader("Mean Agreement Scores")
    motivation_means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
    
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax2)
    ax2.set_xlim(0, 5)
    for index, value in enumerate(motivation_means.values):
        ax2.text(value + 0.05, index, f'{value:.2f}', va='center')
    st.pyplot(fig2)

# --- Row 2: Gender Comparison (Dumbbell Plot) ---
st.divider()
st.subheader("Gender Comparison: Motivation Scores")

# Re-calculating means for the dumbbell plot based on filtered data
gender_means = filtered_df.groupby('Gender')[motivation_questions].mean().T.reset_index()
df_melted_means = gender_means.melt(id_vars='index', var_name='Gender', value_name='Mean Score')
df_melted_means.rename(columns={'index': 'Motivation Question'}, inplace=True)

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.pointplot(
    data=df_melted_means, x='Mean Score', y='Motivation Question',
    hue='Gender', join=True, palette={'Female': 'red', 'Male': 'blue'},
    markers='o', scale=0.8, ax=ax3
)
ax3.set_xlim(2.5, 4.5)
ax3.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig3)

# --- Row 3: Correlations and Regression ---
st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("Correlation Heatmap")
    corr_matrix = filtered_df[motivation_questions].corr()
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax4)
    st.pyplot(fig4)

with col4:
    st.subheader("Regression Analysis")
    # Dynamic selection for regression
    x_axis = st.selectbox("Select X-axis variable", motivation_questions, index=1)
    y_axis = st.selectbox("Select Y-axis variable", motivation_questions, index=5)
    
    fig5, ax5 = plt.subplots(figsize=(10, 8))
    sns.regplot(data=filtered_df, x=x_axis, y=y_axis, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax5)
    st.pyplot(fig5)
