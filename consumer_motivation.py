import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Motivation Analysis Dashboard", layout="wide")

# Applying Seaborn style globally
sns.set_style("whitegrid")

# --- DATA LOADING & PREPARATION ---
@st.cache_data
def load_data():
    # REPLACE THIS with your actual data loading: df = pd.read_csv('your_file.csv')
    # For now, creating dummy data to ensure the script runs
    motivation_questions = [
        'follow_for_updates_promotions', 'follow_because_like_products',
        'follow_because_entertaining', 'follow_because_discounts_contests',
        'follow_because_express_personality', 'follow_because_online_community',
        'follow_because_support_loyalty'
    ]
    data = np.random.randint(1, 6, size=(100, len(motivation_questions)))
    df = pd.DataFrame(data, columns=motivation_questions)
    df['Gender'] = np.random.choice(['Male', 'Female'], size=100)
    return df, motivation_questions

df, motivation_questions = load_data()

# --- HEADER ---
st.title("📊 Motivation Analysis Dashboard")
st.markdown("This interactive dashboard explores survey respondent motivations using Likert-scale data.")

# --- IN-PAGE FILTERS ---
# Placing the gender filter at the top for better structure
st.subheader("🎯 Global Filters")
all_genders = df['Gender'].unique().tolist()
selected_genders = st.multiselect("Select Gender(s) to include:", options=all_genders, default=all_genders)

# Apply filter to the main dataframe
filtered_df = df[df['Gender'].isin(selected_genders)]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- TABBED ANALYSIS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Mean Scores", 
    "🔗 Correlations", 
    "📊 Response Distribution", 
    "👥 Gender Analysis"
])

# --- TAB 1: MEAN SCORES ---
with tab1:
    st.header("Agreement Mean Scores")
    motivation_means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax1)
    ax1.set_title('Mean Agreement Scores (1=Strongly Disagree, 5=Strongly Agree)')
    ax1.set_xlim(0, 5)
    
    # Value labels
    for index, value in enumerate(motivation_means.values):
        ax1.text(value + 0.05, index, f'{value:.2f}', va='center')
    
    st.pyplot(fig1)

# --- TAB 2: CORRELATIONS & REGRESSION ---
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Correlation Heatmap")
        corr_matrix = filtered_df[motivation_questions].corr()
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax2)
        st.pyplot(fig2)

    with col2:
        st.header("Regression Analysis")
        # Let user choose which questions to compare
        q_x = st.selectbox("Select X-Axis Motivation:", motivation_questions, index=1)
        q_y = st.selectbox("Select Y-Axis Motivation:", motivation_questions, index=5)
        
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        sns.regplot(data=filtered_df, x=q_x, y=q_y, scatter_kws={'alpha':0.6}, line_kws={'color':'red'}, ax=ax3)
        ax3.set_title(f"Relationship: {q_x} vs {q_y}")
        st.pyplot(fig3)

# --- TAB 3: STACKED DISTRIBUTION ---
with tab3:
    st.header("Percentage Distribution of Responses")
    
    # Calculate percentages
    dist_data = []
    for q in motivation_questions:
        counts = filtered_df[q].value_counts(normalize=True).reindex(range(1, 6), fill_value=0) * 100
        dist_data.append(counts.values)
    
    df_dist = pd.DataFrame(dist_data, index=motivation_questions, 
                           columns=['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'])
    
    fig4, ax4 = plt.subplots(figsize=(12, 8))
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]
    df_dist.plot(kind='barh', stacked=True, color=colors, ax=ax4, width=0.8)
    ax4.set_xlim(0, 100)
    ax4.legend(title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig4)

# --- TAB 4: GENDER DUMBBELL PLOT ---
with tab4:
    st.header("Gender-Based Comparison")
    
    # Calculate means per gender
    gender_means = filtered_df.groupby('Gender')[motivation_questions].mean().T
    df_melted = gender_means.reset_index().melt(id_vars='index', var_name='Gender', value_name='Mean Score')
    df_melted.rename(columns={'index': 'Motivation Question'}, inplace=True)

    fig5, ax5 = plt.subplots(figsize=(12, 8))
    sns.pointplot(
        data=df_melted, 
        x='Mean Score', 
        y='Motivation Question', 
        hue='Gender',
        join=True, 
        palette={'Female': 'red', 'Male': 'blue'},
        markers=['o', 'o'], 
        capsize=0.1,
        ax=ax5
    )
    ax5.set_xlim(1, 5) # Adjusted to full Likert scale
    ax5.set_title("Dumbbell Plot: Mean Motivation Scores by Gender")
    st.pyplot(fig5)
    st.success("Analysis complete.")
