import streamlit as st
import pandas as pd

# Set page to wide mode for a more professional look
st.set_page_config(page_title="Fashion Habits Dashboard", layout="wide")

# ---------------------------------------------------------
# LOAD DATA 
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

df = load_data()

# =========================================================
# HOMEPAGE HEADER
# =========================================================

# Using a combination of emojis and subheaders for a "title" feel
st.markdown("# 🛍️ **Dashboard of Fashion Habits on Social Media**")

st.divider()

# Case Study 
st.markdown("## 🏭 Case Study & Industrial Relevance")

st.markdown(
    "This study adopts a **case study approach** to examine consumer fashion behaviour on social media platforms. "
    "The findings are highly relevant to the **fashion and digital marketing industry**, where social media "
    "strongly influences brand engagement and online purchasing decisions."
)

# Problem Definition 
st.markdown("## ❓ Problem Definition")

st.markdown(
    "Despite the growing role of social media in fashion marketing, there is limited empirical understanding of how "
    "**demographic factors influence fashion awareness, spending behaviour, and shopping decisions** online."
)


# ---------------------------------------------------------
# SURVEY OVERVIEW (The "Quick Stats" Row)
# ---------------------------------------------------------
st.markdown("## 📋 **Survey Overview**")

col1, col2 = st.columns([1, 2])

with col1:
    # A big, bold stat for impact
    st.markdown(f"""
        ### **{len(df)}**
        **Valid Respondents**
    """)
    st.write("---")
    st.markdown("📍 **Location:** Across Malaysia")
    st.markdown("👥 **Focus:** Young Adults & Adults")

with col2:
    st.markdown(
        """
        The data was gathered via **Google Forms** and distributed through a network of 
        **WhatsApp groups and personal contacts**. The survey consists of **29 structured questions**, 
        primarily measured using **5-point Likert scales**.

        Participation was **voluntary**, responses were **anonymous**, and the data was used 
        strictly for **academic purposes**, ensuring ethical research practices.
        """
    )

    st.markdown("🔗 **[View the survey questionnaire]**"   (https://forms.gle/y8DT7eQfJXB7f7qY9)")


st.write("") # Just some spacing

# ---------------------------------------------------------
# DASHBOARD NAVIGATION GUIDE
# ---------------------------------------------------------
st.markdown("## 📑  **Dashboard Section**")
st.write("The dashboard is split into 4 Section:")

# Creating a 4-column grid for the sections
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("### 🧍\n**Section A - Izzati**")
    st.caption("Demographic Information")
    st.markdown("*Gender, age, education, and monthly fashion spend.*")

with s2:
    st.markdown("### 📱\n**Section B - Hanis**")
    st.caption("Consumer Behaviour on Social Media")
    st.markdown("*Activity levels and how users interact with content.*")

with s3:
    st.markdown("### 👗\n**Section C - Syadira**")
    st.caption("Consumer Intrest in Fashion")
    st.markdown("*Interests, trends, and the influence of social media.*")

with s4:
    st.markdown("### 🛍️\n**Section D - Aina**")
    st.caption("Motivation to Follow Fashion Brand")
    st.markdown("*The 'Why' behind the buy and brand influence.*")

st.divider()

