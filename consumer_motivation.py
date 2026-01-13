import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. PAGE SETUP & DATA LOADING
# ==========================================
st.set_page_config(page_title="Consumer Motivation Dashboard", layout="wide")

@st.cache_data
def load_and_preprocess_data():
    # Replace this with your actual data source, e.g., pd.read_csv('data.csv')
    # For now, this assumes 'df' is available.
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    df = pd.read_csv(url)
    
    motivation_questions = [
        'follow_for_updates_promotions', 'follow_because_like_products',
        'follow_because_entertaining', 'follow_because_discounts_contests',
        'follow_because_express_personality', 'follow_because_online_community',
        'follow_because_support_loyalty'
    ]
    
    # Ensure Gender is clean
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].astype(str).str.strip()
        
    return df, motivation_questions

df, motivation_questions = load_and_preprocess_data()

st.title("📊 Consumer Motivation Analysis Dashboard")
st.markdown("Exploring the drivers behind fashion brand engagement on social media.")

# ==========================================
# 2. CALCULATION LOGIC
# ==========================================
# Calculate Likert Percentages for the Stacked Bar
def get_motivation_pct(df, questions):
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    for q in questions:
        counts = df[q].value_counts(normalize=True).reindex([1, 2, 3, 4, 5], fillvalue=0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = q
        pct_list.append(counts)
    return pd.DataFrame(pct_list)

df_motivation_pct = get_motivation_pct(df, motivation_questions)

# ==========================================
# 3. SIDEBAR FILTERS
# ==========================================
st.sidebar.header("Global Filters")
selected_gender = st.sidebar.multiselect("Filter by Gender", options=df['Gender'].unique(), default=list(df['Gender'].unique()))
filtered_df = df[df['Gender'].isin(selected_gender)]

# ==========================================
# 4. DASHBOARD TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["Overview & Ranking", "Relationships", "Demographics"])

# ------------------------------------------
# TAB 1: OVERVIEW & RANKING
# ------------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mean Agreement Scores")
        motivation_means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax)
        ax.set_xlim(0, 5)
        for i, v in enumerate(motivation_means.values):
            ax.text(v + 0.05, i, f'{v:.2f}', va='center')
        st.pyplot(fig)

    with col2:
        st.subheader("Likert Scale Distribution")
        plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
        colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]
        
        fig, ax = plt.subplots(figsize=(10, 6.4))
        df_motivation_pct[plot_columns].plot(kind='barh', stacked=True, color=colors, ax=ax)
        ax.set_xlim(0, 100)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

# ------------------------------------------
# TAB 2: RELATIONSHIPS
# ------------------------------------------
with tab2:
    st.subheader("Correlation Analysis")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Heatmap
        corr = filtered_df[motivation_questions].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)
        
    with col_b:
        st.markdown("**Regression Analysis**")
        x_axis = st.selectbox("Select X axis", motivation_questions, index=1)
        y_axis = st.selectbox("Select Y axis", motivation_questions, index=5)
        
        fig, ax = plt.subplots()
        sns.regplot(data=filtered_df, x=x_axis, y=y_axis, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)
        st.pyplot(fig)

# ------------------------------------------
# TAB 3: DEMOGRAPHICS
# ------------------------------------------
with tab3:
    st.subheader("Gender Differences (Dumbbell Plot)")
    
    # Recalculate melted means for dumbbell plot
    gender_means = df.groupby('Gender')[motivation_questions].mean().T.reset_index()
    df_melted = gender_means.melt(id_vars='index', var_name='Gender', value_name='Mean Score')
    df_melted.rename(columns={'index': 'Question'}, inplace=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.pointplot(
        data=df_melted, x='Mean Score', y='Question', hue='Gender',
        join=True, palette={'Female': 'red', 'Male': 'blue'},
        markers=['o', 'o'], linestyles=['-', '-'], capsize=0.1, ax=ax
    )
    ax.set_xlim(2.5, 4.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

    st.info("Interpretation: The dumbbell plot highlights the gap in motivation scores between genders. Red points represent Female respondents while blue points represent Male respondents.")

st.divider()
st.markdown("✔ Dashboard components loaded successfully.")
