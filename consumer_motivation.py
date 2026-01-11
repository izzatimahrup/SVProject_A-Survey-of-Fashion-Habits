import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")
st.title("📊 Fashion Brand Motivation Dashboard")

# 1. Sidebar for Data Upload
uploaded_file = st.sidebar.file_uploader("https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv")

    
    # Define the questions (ensure these match your CSV column names)
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Distributions", "Mean Scores", "Correlations", "Relationship Analysis"
    ])

    sns.set_style("whitegrid")

    # --- TAB 1: DISTRIBUTIONS ---
    with tab1:
        st.header("Response Distribution per Question")
        num_questions = len(motivation_questions)
        fig1, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
        
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
        st.pyplot(fig1)

    # --- TAB 2: MEAN SCORES ---
    with tab2:
        st.header("Overall Motivation Ranking")
        motivation_means = df[motivation_questions].mean().sort_values(ascending=False)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax2)
        ax2.set_title('Mean Agreement Scores', fontsize=16)
        ax2.set_xlim(0, 5)
        
        # Add labels
        for index, value in enumerate(motivation_means.values):
            ax2.text(value + 0.05, index, f'{value:.2f}', va='center', fontsize=10)
            
        st.pyplot(fig2)
        st.write("**Insight:** This chart shows which factors most strongly drive users to follow fashion brands.")

    # --- TAB 3: HEATMAP ---
    with tab3:
        st.header("Correlation Heatmap")
        correlation_matrix = df[motivation_questions].corr()
        
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax3)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig3)

    # --- TAB 4: RELATIONSHIP (REGPLOT) ---
    with tab4:
        st.header("Variable Relationship Analysis")
        
        col_x = st.selectbox("Select X-axis variable", motivation_questions, index=1)
        col_y = st.selectbox("Select Y-axis variable", motivation_questions, index=5)
        
        fig4, ax4 = plt.subplots(figsize=(10, 7))
        sns.regplot(data=df, x=col_x, y=col_y, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax4)
        
        ax4.set_title(f"Relationship: {col_x} vs {col_y}")
        st.pyplot(fig4)
        
        st.info("The red line indicates the trend. If it slopes upward, people who agree with one tend to agree with the other.")

else:
    st.info("Please upload a CSV file in the sidebar to begin.")
