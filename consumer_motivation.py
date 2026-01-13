import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ======================================================
# PAGE CONFIG (Only one allowed per page)
# ======================================================
# If this is a multi-page app, this may be redundant but kept for safety
if 'already_configured' not in st.session_state:
    st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")
    st.session_state.already_configured = True

# ======================================================
# HELPER FUNCTIONS
# ======================================================
def center_title(fig):
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return fig

@st.cache_data
def load_motivation_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
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
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    return data, valid_cols

def calculate_percentages(df, columns):
    """Calculates Likert percentages and handles potential TypeErrors"""
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    
    for col in columns:
        # Ensure numeric to avoid TypeErrors with value_counts or multiplication
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        counts = series.value_counts(normalize=True).reindex([1, 2, 3, 4, 5], fillvalue=0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    
    return pd.DataFrame(pct_list)

@st.cache_data
def process_positive_data(df_input):
    return df_input.copy()

# ======================================================
# MAIN EXECUTION
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")

df, motivation_cols = load_motivation_data()

if not motivation_cols:
    st.error("Could not find the motivation columns in the CSV.")
    st.stop()

# ------------------------------------------------------
# SECTION A: RANKING
# ------------------------------------------------------
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

# ------------------------------------------------------
# SECTION B: CONSUMER SENTIMENT (LIKERT CHART)
# ------------------------------------------------------
st.divider()
st.header("Section B: Deep Dive into Motivations")

# Generate the percentage dataframe
df_motivation_pct = calculate_percentages(df, motivation_cols)
df_motivation_pct_positive = process_positive_data(df_motivation_pct)

# Sidebar Control
st.sidebar.header("Chart Options")
show_labels = st.sidebar.checkbox("Show Percentage Labels", value=True)

# Plotting with Matplotlib/Seaborn
sns.set_style("whitegrid")
plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

fig, ax = plt.subplots(figsize=(12, 7))
df_motivation_pct_positive[plot_columns].plot(
    kind='barh', stacked=True, color=colors, ax=ax, width=0.75
)

ax.set_title('Percentage Distribution of Responses', fontsize=16, pad=20)
ax.set_xlabel('Percentage of Respondents (%)', fontsize=12)
ax.set_ylabel('Motivation Category', fontsize=12)
ax.set_xlim(0, 100)

if show_labels:
    for c in ax.containers:
        labels = [f'{w:.1f}%' if (w := v.get_width()) > 5 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', fontsize=9)

ax.legend(title='Response', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig)

# Blue Interpretation Box
st.info("""
**Data Interpretation:**
This chart shows a positive skew in consumer motivation. The majority of respondents 
fall into the **Agree** (light green) and **Strongly Agree** (dark green) categories. 
The areas in red indicate specific questions where intervention may be needed to 
address underlying dissatisfaction or lack of interest.
""")

# ------------------------------------------------------
# SECTION C: RELATIONSHIPS
# ------------------------------------------------------
st.divider()
st.header("Section C: Engagement Relationships")
tab_corr, tab_rel = st.tabs(["Correlation Heatmap", "Relationship Scatters"])

with tab_corr:
    corr_matrix = df[motivation_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix, text_auto=".2f",
        color_continuous_scale='RdBu_r',
        title="Correlation Heatmap"
    )
    st.plotly_chart(center_title(fig_heatmap), use_container_width=True)

with tab_rel:
    c1, c2 = st.columns([1, 2])
    with c1:
        x_var = st.selectbox("Select X-axis", motivation_cols, index=0)
        y_var = st.selectbox("Select Y-axis", motivation_cols, index=1)
        current_corr = df[x_var].corr(df[y_var])
        st.metric("Correlation Coefficient", f"{current_corr:.2f}")
    
    with c2:
        fig_scatter = px.scatter(df, x=x_var, y=y_var, opacity=0.4, trendline="ols",
                                 title=f"Relationship: {x_var} vs {y_var}")
        st.plotly_chart(center_title(fig_scatter), use_container_width=True)

st.divider()
st.markdown("✔ **Consumer Motivation Analysis Complete**")
