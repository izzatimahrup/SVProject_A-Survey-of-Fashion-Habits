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
    "demographic.py",
    title="Demographic Analysis (Izzati)",
    icon="👥"
)

consumer_behaviour_hanis = st.Page(
    "consumer_behaviour.py",
    title="Consumer Behaviour",
    icon="📱"
)

consumer_interest_syadira = st.Page(
    "consumer_interest.py",
    title="Consumer Interest",
    icon="👗"
)

consumer_motivation_aina = st.Page(
    "consumer_motivation.py",
    title="Shopping Motivation",
    icon="🎯"
)

# ---------------------------------------------------------
# Navigation Menu
# ---------------------------------------------------------

pg = st.navigation(
    {
        "Main Menu": [
            home,
            demographic,
            consumer_behaviour,
            consumer_interest,
            consumer_motivation
        ]
    }
)

pg.run()
