import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# LOAD DATA 
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

df = load_data()

# =========================================================
# HOMEPAGE
# =========================================================

st.title("📊 Fashion Habits on Social Media Dashboard")

st.markdown(
    """
    This interactive dashboard presents findings from a survey conducted for the study  
    *“Consumer Behaviour Towards Fashion Brands on Social Media.”*  
    The dashboard visualises respondents’ demographic profiles, social media usage patterns, 
    fashion interests, and motivations related to fashion consumption on social media platforms.
    """
)

# ---------------------------------------------------------
# SURVEY OVERVIEW
# ---------------------------------------------------------
st.subheader("Survey Overview")

total_respondents = len(df)

st.markdown(
    f"""
    A total of **{total_respondents} valid respondents** participated in this study.  
    The survey was created and administered using **Google Forms**, and distributed online via  
    **WhatsApp group sharing and personal contacts**, allowing for efficient data collection.
    
    👉 **Survey link:**  
    https://forms.gle/y8DT7eQfJXB7f7qY9
    
    The survey targeted respondents **across Malaysia**, with a focus on **young adults and adults**, 
    as these groups represent the most active users of social media platforms and are more likely 
    to engage with fashion-related content and online shopping.
    """
)

# ---------------------------------------------------------
# OVERVIEW OF DASHBOARD SECTIONS
# ---------------------------------------------------------
st.subheader("Overview of Dashboard Sections")

st.markdown(
    "The dashboard is organised into four analytical sections, each focusing on a different aspect "
    "of consumers’ fashion behaviour on social media."
)

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    st.markdown(
        """
        ### 🧍 Section A: Demographic Overview
        Presents the demographic characteristics of respondents, including gender, age group, 
        region, education level, employment status, and average monthly fashion expenditure.
        """
    )

with row1_col2:
    st.markdown(
        """
        ### 📱 Section B: Social Media Usage Patterns
        Illustrates respondents’ activity levels across different social media platforms and 
        common online behaviours such as viewing, sharing, and interacting with content.
        """
    )

with row2_col1:
    st.markdown(
        """
        ### 👗 Section C: Fashion Interest and Awareness
        Highlights respondents’ interest in fashion, awareness of current trends, and the role 
        of social media in shaping fashion-related attitudes.
        """
    )

with row2_col2:
    st.markdown(
        """
        ### 🛍️ Section D: Motivation and Shopping Influence
        Focuses on respondents’ motivations for following fashion brands and the factors that 
        influence shopping decisions on social media platforms.
        """
    )

