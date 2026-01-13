import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ======================================================
# 1. DATA LOADING & MAPPING
# ======================================================
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
    return data, valid_cols

# ======================================================
# 2. CALCULATION HELPERS
# ======================================================
def calculate_percentages(df_input, columns):
    """Calculates Likert percentages and ensures type safety"""
    label_map = {
        1: 'Strongly Disagree', 
        2: 'Disagree', 
        3: 'Neutral', 
        4: 'Agree', 
        5: 'Strongly Agree'
    }
    pct_list = []
    
    for col in columns:
        # Force to numeric and drop NaNs
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        
        # Get percentages, ensure integer index
        counts = series.value_counts(normalize=True)
        counts.index = counts.index.astype(int)
        
        # Reindex, multiply by 100, and map labels
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    
    return pd.DataFrame(pct_list)

# ======================================================
# 3. MAIN DASHBOARD EXECUTION
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")

# Load Data
df_raw, motivation_cols = load_motivation_data()

# --- DEMOGRAPHIC FILTER ---
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
    selected_gender = "Overall Scaling"

# ------------------------------------------------------
# SECTION A: RANKING
# ------------------------------------------------------
st.header("Section A: Motivation Ranking")
motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Average Score']

fig_ranking = px.bar(
    motivation_means, x='Average Score', y='Motivation',
    orientation='h', text_auto='.2f',
    color='Average Score', color_continuous_scale='Viridis',
    title=f"Average Agreement Score: {selected_gender}"
)
fig_ranking.update_layout(xaxis_range=[1, 5], title={'x': 0.5, 'xanchor': 'center'})
st.plotly_chart(fig_ranking, use_container_width=True)

# ------------------------------------------------------
# SECTION B: CONSUMER SENTIMENT (LIKERT)
# ------------------------------------------------------
st.divider()
st.header("Section B: Deep Dive into Motivations")

# Calculate Percentages
df_motivation_pct = calculate_percentages(df, motivation_cols)

# Plotting with Matplotlib
sns
