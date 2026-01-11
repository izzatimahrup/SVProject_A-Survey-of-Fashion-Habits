import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")

# 2. Correct Data Loading
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv"
    data = pd.read_csv(url)
    
    # --- CRITICAL FIX: Clean the Column Names ---
    # This removes spaces, dots, and brackets and makes everything lowercase
    # This helps match your list to the actual CSV headers
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

# 3. Execution
try:
    df = load_data()
    st.title("📊 Fashion Brand Motivation Dashboard")
except Exception as e:
    st.error(f"Failed to load data. Error: {e}")
    st.stop()

# 4. Define the target names
# Note: Ensure these keywords appear somewhere in your CSV column headers!
motivation_questions = [
    'follow_for_updates_promotions',
    'follow_because_like_products',
    'follow_because_entertaining',
    'follow_because_discounts_contests',
    'follow_because_express_personality',
    'follow_because_online_community',
    'follow_because_support_loyalty'
]

# Find columns that CONTAIN these keywords to be safe
existing_cols = []
for q in motivation_questions:
    # Check if the keyword exists inside any of the actual CSV column names
    match = [col for col in df.columns if q in col]
    if match:
        existing_cols.append(match[0])

# --- Sidebar Diagnostic ---
with st.sidebar:
    st.header("Debug Info")
    if st.checkbox("Show Actual CSV Headers"):
        st.write(df.columns.tolist())

# Check if we found anything
if not existing_cols:
    st.error("🚨 Column Match Failed!")
    st.write("The app couldn't find your motivation columns. Please check 'Show Actual CSV Headers' in the sidebar and make sure the names match.")
    st.stop()

# --- Main Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Distribution", "Mean Scores", "Correlations", "Relationship Analysis", "Summary"
])

# Tab 1: Distribution
with tab1:
    st.header("Distribution of Responses")
    num_questions = len(existing_cols)
    fig, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
    if num_questions == 1: axes = [axes]

    for i, col in enumerate(existing_cols):
        response_counts = df[col].astype(str).value_counts().sort_index()
        sns.barplot(x=response_counts.index, y=response_counts.values, ax=axes[i], palette='viridis')
        axes[i].set_title(f"Question: {col.replace('_', ' ').title()}", fontsize=14)
    
    plt.tight_layout()
    st.pyplot(fig)

# Tab 2: Mean Scores
with tab2:
    st.header("Mean Agreement Scores")
    motivation_means = df[existing_cols].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax)
    ax.set_xlim(0, 5)
    for index, value in enumerate(motivation_means.values):
        ax.text(value + 0.05, index, f'{value:.2f}', va='center')
    st.pyplot(fig)

# Tab 3: Heatmap
with tab3:
    st.header("Correlation Heatmap")
    if len(existing_cols) > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)

# Tab 4: Relationship
with tab4:
    st.header("Relationship Analysis")
    c1, c2 = st.columns(2)
    x_ax = c1.selectbox("Select X-axis", existing_cols, index=0)
    y_ax = c2.selectbox("Select Y-axis", existing_cols, index=1)
    fig, ax = plt.subplots()
    sns.regplot(data=df, x=x_ax, y=y_ax, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)
    st.pyplot(fig)

# Tab 5: Summary (Your Colab Insights)
with tab5:
    st.header("Summary of Key Trends")
    st.info("""
    - **Top Drivers:** Highest agreement for product style and promotional updates.
    - **Neutral Areas:** Discounts and personal expression show high neutral sentiment.
    - **Lowest Impact:** Online community and brand loyalty.
    """)
