import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fashion Shopping Behaviour Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ---------------------------------------------------------
# Define Pages (BASED ON GOOGLE FORM SECTIONS)
# ---------------------------------------------------------

home = st.Page(
    "home.py",
    title="Home",
    icon="🏠",
    default=True
)

demographic = st.Page(
    "demographic.py",
    title="Demographic Information",
    icon="👥"
)

consumerbehaviour = st.Page(
    "consumer_behaviour.py",
    title="Consumer Behaviour",
    icon="📱"
)

consumerinterest = st.Page(
    "consumer_interest.py",
    title="Consumer Interest in Fashion",
    icon="👗"
)

consumermotivation = st.Page(
    "consumer_motivation.py",
    title="Motivation to Follow Fashion Brands",
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
            consumerbehaviour,
            consumerinterest,
            consumermotivation
        ]
    }
)

# Run Navigation
pg.run()
