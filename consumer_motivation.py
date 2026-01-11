import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. MUST BE FIRST: Page Configuration
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")

# 2. Define the Data Loading Function
@st.cache_data
def load_data():
    # URL Encoding for the space and parentheses in your filename
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF%20(1).csv"
    # We use a more robust way to handle the special characters in the URL
    safe_url = url.replace(" ", "%20").replace("(", "%28").replace(")", "%29")
    
    try:
        data = pd.read_csv(safe_url)
        # Standardize columns to lowercase and underscores
        data.columns = (data.columns
                        .str.strip()
                        .str.lower()
                        .str.replace(' ', '_')
                        .str.replace('(', '')
                        .str.replace(')', '')
                        .str.replace('[', '')
                        .str.replace(']', '')
                        .str.replace('.', ''))
        return data
    except Exception as e:
        st.error(f"Failed to load data. Error: {e}")
        return None

# 3. Execution
df = load_data()

if df is not None:
    st.title("📊 Fashion Brand Motivation Dashboard")

    # Define the target names (standardized)
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Matching logic: Find actual columns that match our keywords
    existing_cols = []
    for q in motivation_questions:
        match = [col for col in df.columns if q in col]
        if match:
            existing_cols.append(match[0])

    if not existing_cols:
        st.error("🚨 No matching columns found. Please check your CSV headers.")
        with st.expander("See available columns"):
            st.write(df.columns.tolist())
    else:
        # Create Tabs
        tabs = st.tabs(["Distribution", "Mean Scores", "Correlations", "Analysis", "Summary"])
        
        with tabs[0]:
            st.header("Distribution of Responses")
            fig, axes = plt.subplots(len(existing_cols), 1, figsize=(10, 5 * len(existing_cols)))
            if len(existing_cols) == 1: axes = [axes]
            for i, col in enumerate(existing_cols):
                counts = df[col].astype(str).value_counts().sort_index()
                sns.barplot(x=counts.index, y=counts.values, ax=axes[i], palette='viridis')
                axes[i].set_title(col.replace('_', ' ').title())
            plt.tight_layout()
            st.pyplot(fig)

        with tabs[1]:
            st.header("Mean Agreement Scores")
            means = df[existing_cols].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=means.values, y=means.index, palette='viridis', ax=ax)
            for i, v in enumerate(means.values):
                ax.text(v + 0.05, i, f'{v:.2f}', va='center')
            st.pyplot(fig)

        with tabs[2]:
            st.header("Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig)

        with tabs[3]:
            st.header("Relationship Analysis")
            col1, col2 = st.columns(2)
            x_v = col1.selectbox("X Axis", existing_cols, index=0)
            y_v = col2.selectbox("Y Axis", existing_cols, index=1)
            fig, ax = plt.subplots()
            sns.regplot(data=df, x=x_v, y=y_v, ax=ax, line_kws={'color':'red'})
            st.pyplot(fig)

        with tabs[4]:
            st.header("Summary of Key Trends")
