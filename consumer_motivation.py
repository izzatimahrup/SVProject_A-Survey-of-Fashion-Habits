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
# 2. CALCULATION HELPERS (The Fix is Here)
# ======================================================
def calculate_percentages(df_input, columns):
    """Calculates Likert percentages and ensures index type safety"""
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    
    for col in columns:
        # Convert to numeric, handle errors, and drop NaNs
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        
        # Get raw frequencies
        counts = series.value_counts(normalize=True)
        
        # --- THE FIX ---
        # Ensure index is integer so it matches [1,2,3,4,5] perfectly
        counts.index = counts.index.astype(int)
        
        # Reindex to ensure all levels 1-5 exist, then multiply
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0)
        counts = counts * 100 
        
        # Map labels and name the series
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

# --- SIDEBAR FILTER ---
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

# Calculate Percentages safely
df_motivation_pct = calculate_percentages(df, motivation_cols)

# Sidebar toggle
show_labels = st.sidebar.checkbox("Show Percentage Labels", value=True)

# Likert Plotting
sns.set_style("whitegrid")
plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

fig, ax = plt.subplots(figsize=(12, 8))
df_motivation_pct[plot_columns].plot(
    kind='barh', stacked=True, color=colors, ax=ax, width=0.8
)

ax.set_title('Percentage Distribution of Responses', fontsize=16, pad=20)
ax.set_xlabel('Percentage (%)', fontsize=12)
ax.set_xlim(0, 100)

if show_labels:
    for c in ax.containers:
        # Only label
