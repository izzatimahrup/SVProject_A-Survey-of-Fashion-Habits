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
    title="Demographic Information",
    icon="👥",
    url_path="Demographic_Information-Izzati"
)

consumer_behaviour_hanis = st.Page(
    "consumer_behaviour.py",
    title="Consumer Behaviour on Social Media",
    icon="📱"
)

consumer_interest_syadira = st.Page(
    "consumer_interest.py",
    title="Consumer Intrest in Fashion",
    icon="👗"
)

consumer_motivation_aina = st.Page(
    "consumer_motivation.py",
    title="Motivation to Follow Fashion Brand",
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
