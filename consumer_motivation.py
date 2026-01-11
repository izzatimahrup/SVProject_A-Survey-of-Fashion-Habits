import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Config
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")

# 2. Load Data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv"
    return pd.read_csv(url)

try:
    df = load_data()
    st.title("📊 Fashion Brand Motivation Dashboard")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 3. Define Questions (DO THIS BEFORE TABS)
motivation_questions = [
    'follow_for_updates_promotions',
    'follow_because_like_products',
    'follow_because_entertaining',
    'follow_because_discounts_contests',
    'follow_because_express_personality',
    'follow_because_online_community',
    'follow_because_support_loyalty'
]
# Filter to ensure they exist in the CSV
existing_cols = [c for c in motivation_questions if c in df.columns]

# 4. Define ALL Tabs at once
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Distribution", 
    "Mean Scores", 
    "Correlations", 
    "Relationship Analysis",
    "Summary & Trends"
])

# 5. Fill the Tabs
with tab1:
    st.header("Distribution of Responses")
    if existing_cols:
        fig, axes = plt.subplots(nrows=len(existing_cols), ncols=1, figsize=(10, 5 * len(existing_cols)))
        if len(existing_cols) == 1: axes = [axes]
        for i, col in enumerate(existing_cols):
            counts = df[col].value_counts().sort_index()
            sns.barplot(x=counts.index, y=counts.values, ax=axes[i], palette='viridis')
            axes[i].set_title(col.replace('_', ' ').title())
        plt.tight_layout()
        st.pyplot(fig)

with tab2:
    st.header("Mean Agreement Scores")
    if existing_cols:
        means = df[existing_cols].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=means.values, y=means.index, palette='viridis', ax=ax)
        st.pyplot(fig)

with tab3:
    st.header("Correlation Heatmap")
    if len(existing_cols) > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

with tab4:
    st.header("Relationship Analysis")
    if len(existing_cols) >= 2:
        c1, c2 = st.columns(2)
        x_axis = c1.selectbox("X-axis", existing_cols, index=0)
        y_axis = c2.selectbox("Y-axis", existing_cols, index=1)
        fig, ax = plt.subplots()
        sns.regplot(data=df, x=x_axis, y=y_axis, ax=ax)
        st.pyplot(fig)

with tab5:
    st.header("Summary of Key Motivations and Trends")
    if existing_cols:
        means = df[existing_cols].mean().sort_values(ascending=False)
        m1, m2 = st.columns(2)
        m1.metric("Top Driver", means.index[0], f"{means.iloc[0]:.2f}")
        m2.metric("Weakest Driver", means.index[-1], f"{means.iloc[-1]:.2f}")
        
        st.subheader("General Trends")
        st.info("Primary Drivers: Product style and promotional updates.")
