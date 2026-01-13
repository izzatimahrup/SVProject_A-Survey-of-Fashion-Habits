import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Motivation Analysis Dashboard", layout="wide")

st.title("📊 Motivation Questions Analysis Dashboard")
st.markdown("This dashboard visualizes the motivations behind user engagement and their correlations.")

# --- MOCK DATA LOADING (Replace this with your actual df loading) ---
@st.cache_data
def load_data():
    # In a real scenario: return pd.read_csv('your_data.csv')
    # Creating dummy data for demonstration
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

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
filtered_df = df[df['Gender'].isin(selected_gender)]

# --- TABBED LAYOUT ---
tab1, tab2, tab3, tab4 = st.tabs(["Mean Scores", "Correlations", "Distribution", "Gender Analysis"])

# --- TAB 1: MEAN SCORES BAR CHART ---
with tab1:
    st.header("Mean Agreement Scores")
    motivation_means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax1)
    ax1.set_title('Mean Agreement Scores for Motivation Questions')
    ax1.set_xlim(0, 5)
    
    for index, value in enumerate(motivation_means.values):
        ax1.text(value + 0.05, index, f'{value:.2f}', va='center')
        
    st.pyplot(fig1)

# --- TAB 2: CORRELATION & REGRESSION ---
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Correlation Heatmap")
        corr_matrix = filtered_df[motivation_questions].corr()
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax2)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig2)

    with col2:
        st.subheader("Regression Analysis")
        q1 = st.selectbox("Select X-Axis Motivation", motivation_questions, index=1)
        q2 = st.selectbox("Select Y-Axis Motivation", motivation_questions, index=5)
        
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        sns.regplot(data=filtered_df, x=q1, y=q2, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax3)
        ax3.set_title(f"Trend: {q1} vs {q2}")
        st.pyplot(fig3)

# --- TAB 3: STACKED BAR (PERCENTAGE) ---
with tab3:
    st.header("Percentage Distribution")
    
    # Calculate percentages for the Likert scale
    def get_pct_df(data, questions):
        pct_data = []
        for q in questions:
            counts = data[q].value_counts(normalize=True).sort_index() * 100
            # Ensure all 1-5 scales are present
            counts = counts.reindex(range(1, 6), fill_value=0)
            pct_data.append(counts.values)
        
        return pd.DataFrame(pct_data, index=questions, 
                            columns=['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'])

    df_pct = get_pct_df(filtered_df, motivation_questions)
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

    fig4, ax4 = plt.subplots(figsize=(12, 8))
    df_pct.plot(kind='barh', stacked=True, color=colors, ax=ax4, width=0.8)
    ax4.set_xlim(0, 100)
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig4)

# --- TAB 4: GENDER DUMBBELL PLOT ---
with tab4:
    st.header("Gender Comparison")
    
    # Calculate means per gender
    gender_means = filtered_df.groupby('Gender')[motivation_questions].mean().T.reset_index()
    df_melted = gender_means.melt(id_vars='index', var_name='Gender', value_name='Mean Score')
    df_melted.rename(columns={'index': 'Motivation Question'}, inplace=True)

    fig5, ax5 = plt.subplots(figsize=(12, 8))
    sns.pointplot(
        data=df_melted, x='Mean Score', y='Motivation Question', hue='Gender',
        join=True, palette={'Female': 'red', 'Male': 'blue'},
        markers=['o', 'o'], linestyles=['-', '-'], capsize=0.1, ax=ax5
    )
    ax5.set_xlim(1, 5)
    ax5.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig5)
    st.success("Dumbbell plot generated successfully.")
