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
    default=True,
    url_path="Home_Page"
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
    icon="📱",
    url_path="Consumer_Behaviour_on_Social_Media-Hanis"
)

consumer_interest_syadira = st.Page(
    "consumer_interest.py",
    title="Consumer Intrest in Fashion",
    icon="👗",
    url_path="Consumer_Interest_About_Fashion-Syadira"
)

consumer_motivation_aina = st.Page(
    "consumer_motivation.py",
    title="Motivation to Follow Fashion Brand",
    icon="🎯",
    url_path="Motivation_to_Follow_Fashion_Brands-Aina"
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
