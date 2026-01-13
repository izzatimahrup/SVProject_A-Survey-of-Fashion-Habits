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
    # Filter only for columns that exist in the renamed dataframe
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].astype(str).str.strip()
        
    return data, valid_cols

# Initial Load
df_raw, motivation_questions = load_motivation_data()

# ==========================================
# 2. CALCULATION HELPERS
# ==========================================
def calculate_percentages(df_input, columns):
    """Calculates Likert percentages with Python 3.13 type safety"""
    label_map = {
        1: 'Strongly Disagree', 
        2: 'Disagree', 
        3: 'Neutral', 
        4: 'Agree', 
        5: 'Strongly Agree'
    }
    pct_list = []
    
    for col in columns:
        # Force numeric, drop NaNs
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        counts = series.value_counts(normalize=True)
        
        # Cast index to int to avoid float-alignment errors
        counts.index = counts.index.astype(int)
        
        # Reindex and multiply separately
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0)
        counts = counts * 100
        
        # Map labels and name the series
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

# --- TABS FOR ORGANIZATION ---
tab1, tab2, tab3 = st.tabs(["Overview", "Relationships", "Demographics"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mean Agreement Scores")
