import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="FSDK | The Digital Runway",
    page_icon="✨",
    layout="wide"
)

# ---------------------------------------------------------
# LOAD DATA 
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

df = load_data()

# ---------------------------------------------------------
# SIDEBAR - THE RESEARCH TEAM
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎓 **FSDK Research Team**")
    st.markdown("---")
    st.write("👤 **Izzati** (Demographics)")
    st.write("👤 **Hanis** (Behaviour)")
    st.write("👤 **Syadira** (Interests)")
    st.write("👤 **Aina** (Motivations)")
    st.divider()
    st.info("Study: Consumer Behaviour Towards Fashion Brands")

# =========================================================
# HOMEPAGE HEADER
# =========================================================
st.markdown("# 👠 **THE DIGITAL RUNWAY**")
st.markdown("### *A Study on Social Media Fashion Habits*")
st.write("---")

# Introductory Statement
st.markdown(
    """
    Welcome to our Final Year Project dashboard. We are students from the **Faculty of Data Science and Computing (FSDK), Year 4**. 
    This survey analyzes how social media platforms shape the way we discover, follow, and purchase fashion.
    """
)

# ---------------------------------------------------------
# QUICK STATS BANNERS
# ---------------------------------------------------------
st.write("")
m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="Total Respondents", value=len(df))
with m2:
    st.metric(label="Target Region", value="Malaysia")
with m3:
    st.metric(label="Academic Year", value="2024/2025")

st.write("---")

# ---------------------------------------------------------
# THEMED RESEARCH SECTIONS
# ---------------------------------------------------------
st.markdown("## 📊 **Research Focus Areas**")
st.write("Click into each section to explore the data curated by our team.")

# Layout for the four sections
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown("### 🧍 **Section A: Audience Profile**")
    st.markdown("> **Lead Researcher: Izzati**")
    st.caption("Analyzing gender distribution, age groups, and regional background to define who our fashion consumers are.")
    if st.button("Explore Demographics", use_container_width=True):
        st.write("Navigation logic for Izzati's section goes here.")

with col2:
    st.markdown("### 📱 **Section B: Digital Engagement**")
    st.markdown("> **Lead Researcher: Hanis**")
    st.caption("Tracking activity levels across Instagram, TikTok, and Pinterest, and how users interact with fashion content.")
    if st.button("Explore Behaviour", use_container_width=True):
        st.write("Navigation logic for Hanis's section goes here.")

with col3:
    st.markdown("### 👗 **Section C: Style & Trend Awareness**")
    st.markdown("> **Lead Researcher: Syadira**")
    st.caption("Measuring interest in fashion trends and the impact of social media on personal style choices.")
    if st.button("Explore Interests", use_container_width=True):
        st.write("Navigation logic for Syadira's section goes here.")

with col4:
    st.markdown("### 🛍️ **Section D: Purchase Motivations**")
    st.markdown("> **Lead Researcher: Aina**")
    st.caption("Identifying the 'Why'—from discount hunting to brand loyalty and self-expression.")
    if st.button("Explore Motivations", use_container_width=True):
        st.write("Navigation logic for Aina's section goes here.")

st.divider()
