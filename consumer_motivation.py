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
        title={
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    return fig

# ======================================================
# PAGE TITLE & DESCRIPTION
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")
st.markdown(
    "Analyze the driving factors behind why consumers follow fashion brands on social media. "
    "This dashboard visualizes rankings, distributions, and correlations."
)

# ======================================================
# LOAD & MAP DATA
# ======================================================
@st.cache_data
def load_motivation_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
    # Map long survey sentences to shorter, cleaner display titles
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

# Handle Data Source (Checks for Session State first)
if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
    df, motivation_cols = load_motivation_data() # Logic simplified for this example
else:
    df, motivation_cols = load_motivation_data()

# ======================================================
# SECTION A: OVERALL RANKING (MEAN SCORES)
# ======================================================
st.header("Section A: Motivation Ranking")

# Calculate means and sort for a ranking effect
motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Average Score']

fig_ranking = px.bar(
    motivation_means,
    x='Average Score',
    y='Motivation',
    orientation='h',
    text=motivation_means['Average Score'].apply(lambda x: f'{x:.2f}'),
    title="Average Agreement Score (Likert 1-5)",
    color='Average Score',
    color_continuous_scale='Viridis'
)

fig_ranking.update_layout(xaxis_range=[0, 5])
fig_ranking = center_title(fig_ranking)
st.plotly_chart(fig_ranking, use_container_width=True)

# ======================================================
# SECTION B: DISTRIBUTION OF RESPONSES
# ======================================================
st.divider()
st.header("Section B: Response Distributions")
st.info("Visualizing how many respondents chose each level (1=Strongly Disagree, 5=Strongly Agree)")

# Display charts in 2 columns
col1, col2 = st.columns(2)

for i, col_name in enumerate(motivation_cols):
    counts = df[col_name].value_counts().sort_index().reset_index()
    counts.columns = ['Score', 'Respondents']
    
    fig_dist = px.bar(
        counts,
        x='Score',
        y='Respondents',
        text='Respondents',
        title=f"Distribution: {col_name}",
        color='Score',
        color_continuous_scale='Bluered_r'
    )
    
    fig_dist.update_traces(textposition='outside')
    fig_dist.update_layout(showlegend=False, xaxis_title="Likert Score")
    fig_dist = center_title(fig_dist)

    if i % 2 == 0:
        col1.plotly_chart(fig_dist, use_container_width=True)
    else:
        col2.plotly_chart(fig_dist, use_container_width=True)

# ======================================================
# SECTION C: CORRELATION & RELATIONSHIPS
# ======================================================
st.divider()
st.header("Section C: Engagement Relationships")

tab_corr, tab_rel = st.tabs(["Correlation Heatmap", "Relationship Scatters"])

with tab_corr:
    corr_matrix = df[motivation_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Correlation Heatmap of Motivations"
    )
    fig_heatmap = center_title(fig_heatmap)
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab_rel:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("### Comparison Settings")
        x_var = st.selectbox("Select X-axis Variable", motivation_cols, index=1)
        y_var = st.selectbox("Select Y-axis Variable", motivation_cols, index=5)
    
    with c2:
        fig_scatter = px.scatter(
            df, x=x_var, y=y_var, 
            trendline="ols", 
            opacity=0.4,
            title=f"Relationship between {x_var} and {y_var}"
        )
        fig_scatter = center_title(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
st.markdown("✔ **Analysis Complete**")
