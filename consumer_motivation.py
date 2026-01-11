import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- App Configuration ---
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")
st.title("📊 Fashion Brand Motivation Dashboard")

# --- Load Data ---
# Replace 'your_data.csv' with your actual file path
@st.cache_data
def load_data():
    # For demonstration, I'm assuming 'df' exists. 
    # Ensure your dataframe is loaded here.
    # df = pd.read_csv("https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv")
    return df

df = load_data()

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

# --- Sidebar ---
st.sidebar.header("Settings")
st.sidebar.info("Use the tabs below to explore different visualizations of the motivation data.")

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
    
    num_questions = len(motivation_questions)
    fig, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
    
    if num_questions == 1:
        axes = [axes]

    for i, col in enumerate(motivation_questions):
        response_counts = df[col].astype(str).value_counts().sort_index()
        ax = axes[i]
        sns.barplot(x=response_counts.index, y=response_counts.values, ax=ax, palette='viridis', hue=response_counts.index, legend=False)
        ax.set_title(f"Question: {col.replace('_', ' ').title()}", fontsize=14)
        ax.set_xlabel('Response (1=Strongly Disagree, 5=Strongly Agree)')
        ax.set_ylabel('Number of Respondents')

    plt.tight_layout()
    st.pyplot(fig)

# --- Tab 2: Mean Agreement Scores ---
with tab2:
    st.header("Mean Agreement Scores")
    motivation_means = df[motivation_questions].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax)
    
    ax.set_title('Mean Agreement Scores for Motivation Questions', fontsize=16)
    ax.set_xlabel('Mean Agreement Score (1-5)')
    ax.set_xlim(0, 5)

    # Add value labels
    for index, value in enumerate(motivation_means.values):
        ax.text(value + 0.05, index, f'{value:.2f}', va='center', fontsize=10)

    st.pyplot(fig)

# --- Tab 3: Correlation Heatmap ---
with tab3:
    st.header("Correlation Heatmap")
    correlation_matrix = df[motivation_questions].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        correlation_matrix, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f", 
        linewidths=.5, 
        ax=ax
    )
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# --- Tab 4: Relationship Analysis ---
with tab4:
    st.header("Relationship Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Select X-axis Motivation", motivation_questions, index=1)
    with col2:
        y_axis = st.selectbox("Select Y-axis Motivation", motivation_questions, index=5)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.regplot(
        data=df, 
        x=x_axis, 
        y=y_axis, 
        scatter_kws={'alpha':0.6}, 
        line_kws={'color':'red'},
        ax=ax
    )
    
    ax.set_title(f'Relationship: {x_axis.title()} vs {y_axis.title()}')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot(fig)
    st.write("**Interpretation:** This scatter plot with a regression line visualizes the relationship between the two selected motivations.")
