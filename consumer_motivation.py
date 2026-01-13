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

# Initialize data
df_raw, motivation_questions = load_motivation_data()

# ==========================================
# 2. CALCULATION HELPERS (Python 3.13 FIX)
# ==========================================
def calculate_percentages(df_input, columns):
    """Calculates Likert percentages and ensures type safety for Python 3.13"""
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    
    for col in columns:
        # 1. Force to numeric and drop empty rows
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        
        # 2. Get normalized counts (percentages as decimals)
        counts = series.value_counts(normalize=True)
        
        # 3. THE FIX: Force index to integer type before reindexing
        counts.index = counts.index.astype(int)
        
        # 4. Reindex to 1-5 scale, THEN multiply by 100
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0)
        counts = counts * 100
        
        # 5. Map to labels and append
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    
    return pd.DataFrame(pct_list)

# ==========================================
# 3. DASHBOARD UI
# ==========================================
st.title("📊 Consumer Motivation Analysis Dashboard")

# SIDEBAR FILTER
st.sidebar.header("Filter Results")
if 'Gender' in df_raw.columns:
    gender_options = ["All"] +
