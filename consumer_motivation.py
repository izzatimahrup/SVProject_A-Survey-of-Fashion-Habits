import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. PAGE SETUP & DATA LOADING
# ==========================================
if 'already_configured' not in st.session_state:
    st.set_page_config(page_title="Consumer Motivation Dashboard", layout="wide")
    st.session_state.already_configured = True

@st.cache_data
def load_and_preprocess_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
    # This MUST match the keys used in your CSV exactly
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
    # This creates the list of columns based on what was actually found and renamed
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].astype(str).str.strip()
        
    return data, valid_cols

df, motivation_questions = load_and_preprocess_data()

# Safety check to prevent the KeyError
if not motivation_questions:
    st.error("🚨 KeyError: No matching motivation columns found. Please check the text in column_mapping.")
    st.stop()

# ==========================================
# 2. CALCULATION HELPERS
# ==========================================
def get_motivation_pct(df_input, questions):
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    for q in questions:
        # pd.to_numeric handles non-integer data types safely
        series = pd.to_numeric(df_input[q], errors='coerce').dropna()
        counts = series.value_counts(normalize=True)
        counts.index = counts.index.astype(int)
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = q
        pct_list.append(counts)
    return pd.DataFrame(pct_list)

# ==========================================
# 3. DASHBOARD UI
# ==========================================
st.title("📊 Consumer Motivation Analysis Dashboard")

# Sidebar
st.sidebar.header("Global Filters")
genders = ["All"] + sorted(list(df['Gender'].unique())) if 'Gender' in df.columns else ["All"]
selected_gender = st.sidebar.selectbox("Select Gender", genders)

if selected_gender == "All":
    filtered_df = df
else:
    filtered_df = df[df['Gender'] == selected_gender]

tab1, tab2, tab3 = st.tabs(["Overview", "Relationships", "Gender Comparison"])

with tab1:
    col1, col2 = st
