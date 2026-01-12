import streamlit as st

st.set_page_config(
    page_title="Fashion Shopping Behaviour Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ---------------------------------------------------------
# Define Pages
# ---------------------------------------------------------

home = st.Page(
    "home.py",
    title="Home",
    icon="🏠",
    default=True
)

demographic_izzati = st.Page(
    "demographic/izzati.py",
    title="Demographic Analysis (Izzati)",
    icon="👥"
)

consumer_behaviour_hanis = st.Page(
    "consumer_behaviour/hanis.py",
    title="Consumer Behaviour (Hanis)",
    icon="📱"
)

consumer_interest_syadira = st.Page(
    "consumer_interest/syadira.py",
    title="Consumer Interest (Syadira)",
    icon="👗"
)

consumer_motivation_aina = st.Page(
    "consumer_motivation/aina.py",
    title="Shopping Motivation (Aina)",
    icon="🎯"
)

# ---------------------------------------------------------
# Navigation Menu
# ---------------------------------------------------------

pg = st.navigation(
    {
        "Main Menu": [
            home,
            demographic_izzati,
            consumer_behaviour_hanis,
            consumer_interest_syadira,
            consumer_motivation_aina
        ]
    }
)

pg.run()
