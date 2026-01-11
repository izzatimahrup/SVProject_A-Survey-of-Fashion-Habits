import streamlit as st
import pandas as pd

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Fashion Habits Dashboard",
    page_icon="👠",
    layout="wide",
)

# 2. Custom CSS for a "Fashion" feel
st.markdown("""
    <style>
    .main {
        background-color: #fcfaf8;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .section-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA 
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

try:
    df = load_data()
except Exception as e:
    st.error("Could not load data. Check your URL.")
    df = pd.DataFrame()

# =========================================================
# HEADER SECTION
# =========================================================
col_header, col_logo = st.columns([3, 1])

with col_header:
    st.title("✨ Fashion Habits & Social Media")
    st.subheader("Visualizing Consumer Behavior in the Digital Age")
    st.markdown(
        """
        This interactive dashboard explores how social media influences fashion choices 
        among Malaysians. Dive into demographics, trends, and shopping motivations.
        """
    )

with col_logo:
    # A simple placeholder or a fashion-related emoji/graphic
    st.markdown("<h1 style='text-align: right; font-size: 80px;'>🛍️</h1>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# HIGHLIGHT METRICS
# ---------------------------------------------------------
total_respondents = len(df)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="Total Respondents", value=total_respondents, delta="Valid Entries")
with m2:
    st.metric(label="Primary Platform", value="Instagram", delta="Trending") # You can calculate this dynamically
with m3:
    st.metric(label="Target Region", value="Malaysia", delta="National Survey")

# ---------------------------------------------------------
# SURVEY OVERVIEW (Expander to save space)
# ---------------------------------------------------------
with st.expander("📖 About the Study & Methodology"):
    st.markdown(
        f"""
        The survey was administered via **Google Forms** and distributed through **WhatsApp** targeting active social media users.
        
        * **Target Audience:** Young adults & adults in Malaysia.
        * **Objective:** Understand the bridge between social content and purchasing decisions.
        * **Link:** [View Original Survey](https://forms.gle/y8DT7eQfJXB7f7qY9)
        """
    )

st.write("## 🧭 Explore the Data")

# ---------------------------------------------------------
# DASHBOARD SECTIONS (Using modern grid approach)
# ---------------------------------------------------------

row1 = st.columns(2)
row2 = st.columns(2)

with row1[0]:
    st.markdown("""
        <div class="section-card">
            <h3>🧍 Section A: Demographics</h3>
            <p>Who are the respondents? Explore gender splits, age groups, education, and monthly fashion spending.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("View Demographics", key="btn_a"):
        st.info("Navigate to the Demographics page in the sidebar (or logic below).")

with row1[1]:
    st.markdown("""
        <div class="section-card">
            <h3>📱 Section B: Social Media Usage</h3>
            <p>How do people interact? Analysis of platform activity levels and sharing behaviors.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("View Usage Patterns", key="btn_b"):
        pass

with row2[0]:
    st.markdown("""
        <div class="section-card">
            <h3>👗 Section C: Fashion Awareness</h3>
            <p>The role of influencers and digital trends in shaping personal style and attitudes.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("View Fashion Interest", key="btn_c"):
        pass

with row2[1]:
    st.markdown("""
        <div class="section-card">
            <h3>🛍️ Section D: Shopping Motivation</h3>
            <p>The 'Why' behind the buy. Identifying factors that convert views into purchases.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("View Shopping Influence", key="btn_d"):
        pass

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.caption("Developed for the study: 'Consumer Behaviour Towards Fashion Brands on Social Media' • 2024")
