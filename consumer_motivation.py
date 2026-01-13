import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. DATA LOADING & ROBUST MAPPING
# ==========================================
@st.cache_data
def load_and_preprocess_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
    # Mapping to handle long survey questions
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
    # Get only the columns that actually exist in the CSV
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].astype(str).str.strip()
        
    return data, valid_cols

df, motivation_questions = load_and_preprocess_data()

# ==========================================
# 2. CALCULATION HELPERS (Python 3.13 Safe)
# ==========================================
def get_motivation_pct(df_input, questions):
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    for q in questions:
        series = pd.to_numeric(df_input[q], errors='coerce').dropna()
        counts = series.value_counts(normalize=True)
        counts.index = counts.index.astype(int) # Fix for Python 3.13 float index issue
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = q
        pct_list.append(counts)
    return pd.DataFrame(pct_list)

# ==========================================
# 3. SIDEBAR FILTERS
# ==========================================
st.sidebar.header("Global Filters")
genders = ["All"] + sorted(list(df['Gender'].unique())) if 'Gender' in df.columns else ["All"]
selected_gender = st.sidebar.selectbox("Select Gender Filter", genders)

if selected_gender == "All":
    filtered_df = df
else:
    filtered_df = df[df['Gender'] == selected_gender]

# ==========================================
# 4. DASHBOARD UI
# ==========================================
st.title("📊 Consumer Motivation Analysis Dashboard")

tab1, tab2, tab3 = st.tabs(["Overview & Distribution", "Relationships", "Gender Comparison"])

# --- TAB 1: RANKING & LIKERT ---
with tab1:
    col1, col2 = st.columns(2) # FIXED THE ERROR HERE
    
    with col1:
        st.subheader("Mean Agreement Scores")
        means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=means.values, y=means.index, palette='viridis', ax=ax)
        ax.set_xlim(0, 5)
        for i, v in enumerate(means.values):
            ax.text(v + 0.05, i, f'{v:.2f}', va='center')
        st.pyplot(fig)

    with col2:
        st.subheader("Response Distribution (%)")
        df_pct = get_motivation_pct(filtered_df, motivation_questions)
        colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]
        fig_pct, ax_pct = plt.subplots(figsize=(10
