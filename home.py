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
st.markdown("# 👗 **Fashion Habits on Social Media**")
st.markdown("### *Decoding the Digital Runway: A Consumer Behavior Study*")

st.divider()

# A nice "Intro" box using st.info for a soft background color
st.info(
    """
    **Welcome!** This interactive dashboard explores the findings from our study:  
    > *“Consumer Behaviour Towards Fashion Brands on Social Media.”* Explore how demographics, social platforms, and personal motivations drive the way we shop and interact with fashion online today.
    """
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
        The data was gathered via **Google Forms** and distributed through a 
        network of **WhatsApp groups and personal contacts**. 
        
        This method allowed us to capture a snapshot of the most active social media users 
        who are shaping the future of online fashion engagement.
        
        🔗 **[Click here to view the original Survey] (https://forms.gle/y8DT7eQfJXB7f7qY9)**
        """
    )

st.write("") # Just some spacing

# ---------------------------------------------------------
# DASHBOARD NAVIGATION GUIDE
# ---------------------------------------------------------
st.markdown("## 🧭 **What’s Inside?**")
st.write("The dashboard is split into four distinct analytical lenses:")

# Creating a 4-column grid for the sections
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("### 🧍\n**Section A**")
    st.caption("Demographic Overview")
    st.markdown("*Gender, age, education, and monthly fashion spend.*")

with s2:
    st.markdown("### 📱\n**Section B**")
    st.caption("Social Media Usage")
    st.markdown("*Activity levels and how users interact with content.*")

with s3:
    st.markdown("### 👗\n**Section C**")
    st.caption("Fashion Awareness")
    st.markdown("*Interests, trends, and the influence of social media.*")

with s4:
    st.markdown("### 🛍️\n**Section D**")
    st.caption("Shopping Motivation")
    st.markdown("*The 'Why' behind the buy and brand influence.*")

st.divider()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    "<div style='text-align: center; color: gray;'>Built with ❤️ using Streamlit | Fashion Habit Study 2024</div>", 
    unsafe_allow_html=True
)
