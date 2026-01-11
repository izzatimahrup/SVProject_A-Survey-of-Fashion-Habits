import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

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
        title={
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    return fig

# ======================================================
# PAGE TITLE & DESCRIPTION
# ======================================================
st.title("📊 Fashion Brand Motivation Analysis")
st.markdown(
    "This section explores why consumers follow fashion brands on social media, "
    "ranking their motivations from promotions to community building."
)

# ======================================================
# LOAD & MAP DATA
# ======================================================
@st.cache_data
def load_motivation_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    
    # Mapping the long question sentences to short keys for analysis
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
    return data, list(column_mapping.values())

df, motivation_cols = load_motivation_data()

if df.empty:
    st.error("Data could not be loaded.")
    st.stop()

# ======================================================
# SECTION 1: OVERALL RANKING (MEAN SCORES)
# ======================================================
st.header("Section 1: Why Consumers Follow Brands")

# Calculate means and sort
motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Mean Score']

fig1 = px.bar(
    motivation_means,
    x='Mean Score',
    y='Motivation',
    orientation='h',
    text=motivation_means['Mean Score'].apply(lambda x: f'{x:.2f}'),
    title="Average Agreement Score per Motivation (1-5)",
    color='Mean Score',
    color_continuous_scale='Viridis'
)

fig1.update_layout(xaxis_range=[0, 5])
fig1 = center_title(fig1)
st.plotly_chart(fig1, use_container_width=True)

# ======================================================
# SECTION 2: DISTRIBUTION OF RESPONSES
# ======================================================
st.divider()
st.header("Section 2: Distribution of Agreement Levels")

# Display charts in 2 columns
col1, col2 = st.columns(2)

for i, col in enumerate(motivation_cols):
    counts = df[col].value_counts().sort_index().reset_index()
    counts.columns = ['Likert Scale', 'Respondent Count']
    
    fig = px.bar(
        counts,
        x='Likert Scale',
        y='Respondent Count',
        text='Respondent Count',
        title=f"Distribution: {col}",
        color='Likert Scale',
        color_continuous_scale='Plasma'
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, xaxis_title="1 (Strongly Disagree) to 5 (Strongly Agree)")
    fig = center_title(fig)

    if i % 2 == 0:
        col1.plotly_chart(fig, use_container_width=True)
    else:
        col2.plotly_chart(fig, use_container_width=True)

# ======================================================
# SECTION 3: MOTIVATION RELATIONSHIPS
# ======================================================
st.divider()
st.header("Section 3: Motivation Correlation & Relationships")

c1, c2 = st.columns([1.2, 0.8])

with c1:
    # Correlation Heatmap
    corr_matrix = df[motivation_cols].corr()
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Correlation Heatmap between Motivations"
    )
    fig_corr = center_title(fig_corr)
    st.plotly_chart(fig_corr, use_container_width=True)

with c2:
    # Scatter Plot with Regression
    st.subheader("Deep Dive into Relationships")
    var_x = st.selectbox("Select Motivation (X-axis)", motivation_cols, index=1)
    var_y = st.selectbox("Select Motivation (Y-axis)", motivation_cols, index=5)
    
    fig_scatter = px.scatter(
        df, x=var_x, y=var_y, 
        trendline="ols", 
        opacity=0.5,
        title=f"Relationship: {var_x} vs {var_y}"
    )
    fig_scatter = center_title(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
st.markdown("✔ **Consumer Motivation Visualizations Complete**")
