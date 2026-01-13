import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. DATA LOADING & MAPPING
# ==========================================
@st.cache_data
def load_motivation_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
    # Mapping dictionary to shorten long survey questions
    column_mapping = {
        "I follow fashion brands on social media to get updates on new collections or promotions": "Updates & Promotions",
        "I follow fashion brands on social media because  I like their products and style": "Product & Style",
        "I follow fashion brands on social media because it is entertaining.": "Entertainment",
        "I follow fashion brands on social media because I want to receive discounts or participate in contests.": "Discounts & Contests",
        "I follow fashion brands on social media because it helps me express my personality": "Express Personality",
        "I follow fashion brands on social media because I want to feel part of an online community.": "Online Community",
        "I follow fashion brands on social media because I want to support or show loyalty to the brand.": "Brand Loyalty"
    }
    
    data = data.rename(columns=column_mapping)
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].astype(str).str.strip()
        
    return data, valid_cols

# Load data early
df_raw, motivation_questions = load_motivation_data()

# ==========================================
# 2. CALCULATION HELPERS
# ==========================================
def calculate_percentages(df_input, columns):
    """Calculates Likert percentages and ensures type safety"""
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    
    for col in columns:
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        counts = series.value_counts(normalize=True)
        counts.index = counts.index.astype(int)
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    
    return pd.DataFrame(pct_list)

# ==========================================
# 3. DASHBOARD UI
# ==========================================
st.title("📊 Consumer Motivation Analysis Dashboard")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Results")
if 'Gender' in df_raw.columns:
    gender_options = ["All"] + sorted(list(df_raw['Gender'].unique()))
    selected_gender = st.sidebar.selectbox("Filter by Gender", gender_options)
    
    if selected_gender != "All":
        df = df_raw[df_raw['Gender'] == selected_gender].copy()
    else:
        df = df_raw.copy()
else:
    df = df_raw.copy()
    selected_gender = "Overall"

tab1, tab2, tab3 = st.tabs(["Overview", "Relationships", "Gender Comparison"])

# --- TAB 1: RANKING & DISTRIBUTION ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mean Agreement Scores")
        means = df[motivation_questions].mean().sort_values(ascending=False)
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        sns.barplot(x=means.values, y=means.index, palette='viridis', ax=ax1)
        ax1.set_xlim(0, 5)
        st.pyplot(fig1)

    with col2:
        st.subheader("Distribution (%)")
        df_pct = calculate_percentages(df, motivation_questions)
        colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        df_pct[['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']].plot(
            kind='barh', stacked=True, color=colors, ax=ax2
        )
        ax2.set_xlim(0, 100)
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig2)

# --- TAB 2: CORRELATIONS ---
with tab2:
    st.subheader("Correlation Heatmap")
    corr = df[motivation_questions].corr()
    fig3, ax3 = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
    st.pyplot(fig3)

# --- TAB 3: DUMBBELL PLOT ---
with tab3:
    st.subheader("Mean Motivation Scores by Gender")
    if 'Gender' in df_raw.columns:
        gender_means = df_raw.groupby('Gender')[motivation_questions].mean().T.reset_index()
        df_melted = gender_means.melt(id_vars='index', var_name='Gender', value_name='Score')
        
        fig4, ax4 = plt.subplots(figsize=(12, 8))
        sns.pointplot(data=df_melted, x='Score', y='index', hue='Gender', join=True, ax=ax4)
        ax4.set_xlim(1, 5)
        st.pyplot(fig4)
    else:
        st.warning("No gender data available.")

# Blue Interpretation Box
st.info(f"**Interpretation ({selected_gender}):** This view displays how consumers prioritize brand updates vs. community engagement.")

st.divider()
st.markdown("✔ **Analysis Complete**")
