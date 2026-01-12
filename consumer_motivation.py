import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Fashion Brand Motivation Analysis",
    layout="wide"
)

# ======================================================
# HELPER: CENTER ALL PLOTLY TITLES
# ======================================================
def center_title(fig):
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center'}
    )
    return fig

# ======================================================
# PAGE TITLE & DESCRIPTION
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")

st.subheader("Objective")
st.markdown(
    "To analyze the driving factors behind why consumers follow fashion brands on social media."
)

# ======================================================
# LOAD & MAP DATA
# ======================================================
@st.cache_data
def load_motivation_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
    # Mapping dictionary to shorten long survey questions
    column_mapping = {
        "I follow fashion brands on social media to get updates on new collections or promotions": "Updates & Promotions",
        "I follow fashion brands on social media because  I like their products and style": "Product & Style",
        "I follow fashion brands on social media because it is entertaining.": "Entertainment",
        "I follow fashion brands on social media because I want to receive discounts or participate in contests.": "Discounts & Contests",
        "I follow fashion brands on social media because it helps me express my personality": "Express Personality",
        "I follow fashion brands on social media because I want to feel part of an online community.": "Online Community",
        "I follow fashion brands on social media because I want to support or show loyalty to the brand.": "Brand Loyalty"
    }
    
    data = data.rename(columns=column_mapping)
    # Extract only the values that now exist as column names in the dataframe
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    return data, valid_cols

df, motivation_cols = load_motivation_data()

if not motivation_cols:
    st.error("Could not find the motivation columns in the CSV. Check your column mapping keys.")
    st.stop()

# ======================================================
# SECTION A: RANKING
# ======================================================
st.header("Section A: Motivation Ranking")
motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Average Score']

fig_ranking = px.bar(
    motivation_means, x='Average Score', y='Motivation',
    orientation='h', text_auto='.2f',
    color='Average Score', color_continuous_scale='Viridis',
    title="Average Agreement Score (Likert 1-5)"
)
fig_ranking.update_layout(xaxis_range=[1, 5])
st.plotly_chart(center_title(fig_ranking), use_container_width=True)

# Interpretation for Section A
top_motivation = motivation_means.iloc[-1]['Motivation']
bottom_motivation = motivation_means.iloc[0]['Motivation']

with st.expander("📝 Detailed Interpretation: Ranking Analysis"):
    st.write(f"""
    * **Primary Driver:** The highest-ranked motivation is **{top_motivation}**. This indicates that the audience is most strongly driven by tangible value and core brand identity. 
    * **Strategic Insight:** Marketing efforts should lean heavily into the highest-scoring factors to ensure maximum follower retention.
    * **Opportunity Gap:** The lowest score for **{bottom_motivation}** suggests either a lack of interest from the audience or an untapped area where brands could improve their engagement strategies.
    """)

# ======================================================
# SECTION B: DISTRIBUTIONS
# ======================================================
st.divider()
st.header("Section B: Response Distributions")
st.write("This section visualizes the consensus. A high concentration in
