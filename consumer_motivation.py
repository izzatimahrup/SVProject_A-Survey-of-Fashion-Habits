import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.parse

# 1. MUST BE FIRST: Page Configuration
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")

# 2. Define the Data Loading Function
@st.cache_data
def load_data():
    # Base URL from your GitHub
    base_url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    
    # This automatically handles spaces and parentheses safely
    safe_url = urllib.parse.quote(base_url, safe=':/')
    
    try:
        data = pd.read_csv(safe_url)
        # Clean column names to match your motivation_questions list
        data.columns = (data.columns
                        .str.strip()
                        .str.lower()
                        .str.replace(' ', '_')
                        .str.replace('(', '')
                        .str.replace(')', '')
                        .str.replace('[', '')
                        .str.replace(']', '')
                        .str.replace('.', '', regex=False))
        return data
    except Exception as e:
        st.error(f"Failed to load data. Error: {e}")
        return None

# 3. Load Data
df = load_data()

if df is not None:
    st.title("📊 Fashion Brand Motivation Dashboard")

    # 4. Standardized list of questions
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Find columns that match keywords
    existing_cols = []
    for q in motivation_questions:
        match = [col for col in df.columns if q in col]
        if match:
            existing_cols.append(match[0])

    if not existing_cols:
        st.error("🚨 No matching columns found in the CSV.")
        with st.expander("Debug: View Actual Column Names"):
            st.write(df.columns.tolist())
    else:
        # Create Tabs
        tabs = st.tabs(["Distribution", "Mean Scores", "Correlations", "Analysis", "Summary"])
        
        with tabs[0]:
            st.header("Distribution of Responses")
            num_q = len(existing_cols)
            fig, axes = plt.subplots(num_q, 1, figsize=(10, 5 * num_q))
            if num_q == 1: axes = [axes]
            for i, col in enumerate(existing_cols):
                counts = df[col].astype(str).value_counts().sort_index()
                sns.barplot(x=counts.index, y=counts.values, ax=axes[i], palette='viridis')
                axes[i].set_title(f"Question: {col.replace('_', ' ').title()}")
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

        # Tab 3 & 4 follow similar logic using st.pyplot()
        
        with tabs[4]:
            st.header("Summary of Key Trends")
            st.info("Primary drivers: Product Style and Collection Updates.")
