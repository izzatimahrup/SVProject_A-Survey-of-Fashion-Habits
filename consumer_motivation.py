import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. MUST BE FIRST: Page Configuration
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")

# 2. Define the Data Loading Function
@st.cache_data
def load_data():
    # We define the URL INSIDE the function and read it into a local variable 'data'
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv"
    data = pd.read_csv(url)
    return data  # Return the local variable, NOT 'df'

# 3. Execution: Create the 'df' variable by calling the function
try:
    df = load_data()
    st.title("📊 Fashion Brand Motivation Dashboard")
except Exception as e:
    st.error(f"Failed to load data. Technical details: {e}")
    st.stop()

# 4. Define motivation questions (ensure these match your CSV column names exactly)
motivation_questions = [
    'follow_for_updates_promotions',
    'follow_because_like_products',
    'follow_because_entertaining',
    'follow_because_discounts_contests',
    'follow_because_express_personality',
    'follow_because_online_community',
    'follow_because_support_loyalty'
]

# --- Sidebar ---
st.sidebar.header("Navigation")
st.sidebar.info("Select a tab above to view different analytical perspectives.")

# --- Main Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Distribution", 
    "Mean Scores", 
    "Correlations", 
    "Relationship Analysis"
])

# --- Tab 1: Distribution of Responses ---
with tab1:
    st.header("Distribution of Responses")
    sns.set_style("whitegrid")
    
    # Filter for columns that actually exist in the CSV to prevent errors
    existing_cols = [c for c in motivation_questions if c in df.columns]
    
    num_questions = len(existing_cols)
    if num_questions > 0:
        fig, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
        
        if num_questions == 1:
            axes = [axes]

        for i, col in enumerate(existing_cols):
            response_counts = df[col].astype(str).value_counts().sort_index()
            ax = axes[i]
            sns.barplot(x=response_counts.index, y=response_counts.values, ax=ax, palette='viridis', hue=response_counts.index, legend=False)
            ax.set_title(f"Question: {col.replace('_', ' ').title()}", fontsize=14)
            ax.set_xlabel('Response (1=Strongly Disagree, 5=Strongly Agree)')
            ax.set_ylabel('Number of Respondents')

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.error("None of the specified motivation columns were found in the dataset.")

# --- Tab 2: Mean Agreement Scores ---
with tab2:
    st.header("Mean Agreement Scores")
    existing_cols = [c for c in motivation_questions if c in df.columns]
    if existing_cols:
        motivation_means = df[existing_cols].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax)
        
        ax.set_title('Mean Agreement Scores (1-5)', fontsize=16)
        ax.set_xlim(0, 5)

        for index, value in enumerate(motivation_means.values):
            ax.text(value + 0.05, index, f'{value:.2f}', va='center', fontsize=10)

        st.pyplot(fig)

# --- Tab 3: Correlation Heatmap ---
with tab3:
    st.header("Correlation Heatmap")
    existing_cols = [c for c in motivation_questions if c in df.columns]
    if len(existing_cols) > 1:
        correlation_matrix = df[existing_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

# --- Tab 4: Relationship Analysis ---
with tab4:
    st.header("Relationship Analysis")
    existing_cols = [c for c in motivation_questions if c in df.columns]
    
    if len(existing_cols) >= 2:
        c1, c2 = st.columns(2)
        with c1:
            x_axis = st.selectbox("Select X-axis", existing_cols, index=0)
        with c2:
            y_axis = st.selectbox("Select Y-axis", existing_cols, index=1)

        fig, ax = plt.subplots(figsize=(10, 7))
        sns.regplot(data=df, x=x_axis, y=y_axis, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)
        ax.set_title(f"Correlation between {x_axis} and {y_axis}")
        st.pyplot(fig)

# Standardized list of questions (Check these match your CSV exactly!)
motivation_questions = [
    'follow_for_updates_promotions',
    'follow_because_like_products',
    'follow_because_entertaining',
    'follow_because_discounts_contests',
    'follow_because_express_personality',
    'follow_because_online_community',
    'follow_because_support_loyalty'
]

# --- CHANGE THIS LINE TO ADD TAB 5 ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Distribution", 
    "Mean Scores", 
    "Correlations", 
    "Relationship Analysis",
    "Summary & Trends"
])

# ... (Existing code for Tab 1, 2, 3, 4 goes here) ...

# --- NEW TAB 5: Summary & Trends ---
with tab5:
    st.header("Summary of Key Motivations and Trends")
    
    # Calculate means for the summary
    motivation_means = df[motivation_questions].mean().sort_values(ascending=False)
    
    # Key Metrics
    m1, m2 = st.columns(2)
    m1.metric("Most Agreed-Upon", motivation_means.index[0], f"{motivation_means.iloc[0]:.2f}")
    m2.metric("Least Agreed-Upon", motivation_means.index[-1], f"{motivation_means.iloc[-1]:.2f}")
    
    st.divider()
    
    # Detailed Distribution Table
    st.subheader("Statistical Breakdown (%)")
    summary_data = []
    for col in motivation_questions:
        counts = df[col].value_counts(normalize=True).sort_index() * 100
        mode_val = df[col].mode()[0]
        summary_data.append({
            "Motivation": col.replace('_', ' ').title(),
            "Most Common Score": mode_val,
            "Avg Score": round(df[col].mean(), 2)
        })
    
    st.table(pd.DataFrame(summary_data))

    # General Trends (Your Colab text)
    st.subheader("General Trends Observed")
    st.info("""
    - **Primary Drivers:** Highest agreement for liking products/style and updates on promotions.
    - **Secondary Drivers:** Entertainment value is a significant factor.
    - **Moderate Interest:** Discounts and personal expression show high neutral sentiment.
    - **Lower Interest:** Online community and brand loyalty are the least compelling reasons.
    """)
