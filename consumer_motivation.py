import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Fashion Brand Motivation Dashboard", layout="wide")

st.title("📊 Fashion Brand Motivation Analysis")

# --- DATA LOADING ---
# Assuming 'df' is your dataframe. 
# For this example, I'll assume it's already loaded or you can upload it:
# df = pd.read_csv("your_data.csv")

# Defining the motivation questions list
motivation_questions = [
    'follow_for_updates_promotions',
    'follow_because_like_products',
    'follow_because_entertaining',
    'follow_because_discounts_contests',
    'follow_because_express_personality',
    'follow_because_online_community',
    'follow_because_support_loyalty'
]

# --- SIDEBAR / NAVIGATION ---
st.sidebar.header("Navigation")
viz_type = st.sidebar.radio("Go to:", [
    "Response Distributions", 
    "Mean Agreement Scores", 
    "Correlation Heatmap", 
    "Relationship Analysis"
])

sns.set_style("whitegrid")

# --- VIZ 1: DISTRIBUTIONS ---
if viz_type == "Response Distributions":
    st.header("Distribution of Responses")
    num_questions = len(motivation_questions)
    fig, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
    
    if num_questions == 1:
        axes = [axes]

    for i, col in enumerate(motivation_questions):
        response_counts = df[col].astype(str).value_counts().sort_index()
        ax = axes[i]
        sns.barplot(x=response_counts.index, y=response_counts.values, ax=ax, palette='viridis', hue=response_counts.index, legend=False)
        ax.set_title(col.strip().replace('_', ' ').title(), fontsize=14)
        ax.set_xlabel('Response (1=Strongly Disagree, 5=Strongly Agree)')
        ax.set_ylabel('Number of Respondents')
    
    plt.tight_layout()
    st.pyplot(fig)

# --- VIZ 2: MEAN SCORES ---
elif viz_type == "Mean Agreement Scores":
    st.header("Mean Agreement Scores")
    motivation_means = df[motivation_questions].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax)
    
    ax.set_title('Mean Agreement Scores per Motivation', fontsize=16)
    ax.set_xlim(0, 5)
    
    # Add value labels
    for index, value in enumerate(motivation_means.values):
        ax.text(value + 0.05, index, f'{value:.2f}', va='center', fontsize=10)
        
    st.pyplot(fig)
    st.info("A score closer to 5 indicates stronger general agreement among respondents.")

# --- VIZ 3: HEATMAP ---
elif viz_type == "Correlation Heatmap":
    st.header("Correlation Heatmap")
    motivation_df = df[motivation_questions]
    correlation_matrix = motivation_df.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
    plt.xticks(rotation=45, ha='right')
    
    st.pyplot(fig)
    st.write("This heatmap reveals how different motivations correlate. Values closer to 1.0 indicate that respondents who agreed with one motivation likely agreed with the other.")

# --- VIZ 4: REGRESSION ---
elif viz_type == "Relationship Analysis":
    st.header("Relationship Analysis")
    
    # Selection boxes for dynamic analysis
    col1 = st.selectbox("Select X-axis Motivation:", motivation_questions, index=1)
    col2 = st.selectbox("Select Y-axis Motivation:", motivation_questions, index=5)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.regplot(data=df, x=col1, y=col2, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)

    ax.set_title(f'Relationship: {col1.replace("_", " ")} vs {col2.replace("_", " ")}')
    st.pyplot(fig)
    
    st.markdown("""
    **Interpretation:**
    The scatter points represent individual responses. The **red line** indicates the general trend:
    * **Upward slope:** Motivations tend to increase together.
    * **Flat line:** Motivations are likely independent.
    """)
