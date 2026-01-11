import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.parse

# 1. Page Configuration - MUST be the very first Streamlit command
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")

# 2. Define the Data Loading Function
@st.cache_data
def load_data():
    # Base URL from your GitHub
    base_url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    
    # Safely handle spaces and parentheses for the web request
    safe_url = urllib.parse.quote(base_url, safe=':/')
    
    try:
        data = pd.read_csv(safe_url)
        # Clean column names to lowercase and underscores to match your list below
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

# 3. Main Logic
df = load_data()

if df is not None:
    st.title("📊 Fashion Brand Motivation Dashboard")

    # 4. Standardized list of questions (matches the cleaning logic above)
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
        st.error("🚨 No matching columns found in the CSV headers.")
        with st.sidebar.expander("Debug: View Actual Columns"):
            st.write(df.columns.tolist())
    else:
        # Create Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Distribution", "Mean Scores", "Correlations", "Relationship Analysis", "Summary"
        ])

        with tab1:
            st.header("Distribution of Responses")
            num_q = len(existing_cols)
            fig, axes = plt.subplots(num_q, 1, figsize=(10, 5 * num_q))
            if num_q == 1: axes = [axes]
            for i, col in enumerate(existing_cols):
                counts = df[col].astype(str).value_counts().sort_index()
                sns.barplot(x=counts.index, y=counts.values, ax=axes[i], palette='viridis')
                axes[i].set_title(f"Question: {col.replace('_', ' ').title()}")
                axes[i].set_xlabel('Score (1=Strongly Disagree, 5=Strongly Agree)')
            plt.tight_layout()
            st.pyplot(fig)

        with tab2:
            st.header("Mean Agreement Scores")
            means = df[existing_cols].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=means.values, y=means.index, palette='viridis', ax=ax)
            ax.set_xlim(0, 5)
            for i, v in enumerate(means.values):
                ax.text(v + 0.05, i, f'{v:.2f}', va='center')
            st.pyplot(fig)

        with tab3:
            st.header("Correlation Heatmap")
            if len(existing_cols) > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
                st.pyplot(fig)

        with tab4:
            st.header("Relationship Analysis")
            c1, c2 = st.columns(2)
            x_ax = c1.selectbox("Select X-axis", existing_cols, index=0)
            y_ax = c2.selectbox("Select Y-axis", existing_cols, index=1)
            fig, ax = plt.subplots()
            sns.regplot(data=df, x=x_ax, y=y_ax, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)
            st.pyplot(fig)

        with tab5:
            st.header("Summary of Key Trends")
            st.info("""
            - **Top Drivers:** High agreement for product style and promotional updates.
            - **Moderate Drivers:** Entertainment and discounts.
            - **Lowest Impact:** Online community and brand loyalty.
            """)
