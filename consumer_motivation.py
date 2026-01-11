import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")

# 2. Define the Data Loading Function
@st.cache_data
def load_data():
    # Correcting the URL and handling the filename spaces/parentheses
    base_url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF (1).csv"
    safe_url = urllib.parse.quote(base_url, safe=':/')
    
    try:
        # Load into a temporary variable 'data'
        data = pd.read_csv(safe_url)
        
        # Standardize column names (lowercase, no spaces, no dots)
        data.columns = (data.columns
                        .str.strip()
                        .str.lower()
                        .str.replace(' ', '_')
                        .str.replace('(', '')
                        .str.replace(')', '')
                        .str.replace('.', '', regex=False))
        return data # Return 'data', not 'df'
    except Exception as e:
        st.error(f"Failed to load data. Error: {e}")
        return None

# 3. Execution
df = load_data()

if df is not None:
    st.title("📊 Fashion Brand Motivation Dashboard")

    # Define motivation questions
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Verify which columns actually exist in the CSV
    existing_cols = [c for c in motivation_questions if c in df.columns]

    if not existing_cols:
        st.error("🚨 No matching columns found. Please check your CSV headers.")
        with st.expander("View found columns"):
            st.write(df.columns.tolist())
    else:
        # --- Tabs ---
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Distribution", "Mean Scores", "Correlations", "Analysis", "Summary & Trends"
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
            means = df[existing_cols].mean().sort_values(ascending=False)
            col_a, col_b = st.columns(2)
            col_a.metric("Top Motivation", means.index[0].replace('_',' ').title(), f"{means.iloc[0]:.2f}")
            col_b.metric("Lowest Motivation", means.index[-1].replace('_',' ').title(), f"{means.iloc[-1]:.2f}")
            
            st.info("""
            **General Observations:**
            - **Primary Drivers:** Products and promotions are the strongest reasons users follow brands.
            - **Social Factors:** Community and brand loyalty appear to be weaker motivators in this sample.
            """)
else:
    st.error("Check the Sidebar Debug info or your GitHub URL.")
