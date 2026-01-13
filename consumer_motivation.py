import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ======================================================
# 1. DATA LOADING & MAPPING
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
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    return data, valid_cols

# ======================================================
# 2. CALCULATION HELPERS
# ======================================================
def calculate_percentages(df_input, columns):
    """Calculates Likert percentages and ensures type safety for Python 3.13"""
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    
    for col in columns:
        # Force to numeric and drop NaNs
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        
        # Get percentages, ensure integer index for reindexing
        counts = series.value_counts(normalize=True)
        counts.index = counts.index.astype(int)
        
        # Reindex to [1,2,3,4,5], multiply by 100, and map text labels
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    
    return pd.DataFrame(pct_list)

# ======================================================
# 3. MAIN DASHBOARD EXECUTION
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")

# Load Data
df_raw, motivation_cols = load_motivation_data()

# --- DEMOGRAPHIC FILTER ---
st.sidebar.header("Filter Results")
# Adjust 'Gender' to match your actual CSV column name if different
if 'Gender' in df_raw.columns:
    gender_options = ["All"] + list(df_raw['Gender'].unique())
    selected_gender = st.sidebar.selectbox("Filter by Gender", gender_options)
    
    if selected_gender != "All":
        df = df_raw[df_raw['Gender'] == selected_gender].copy()
    else:
        df = df_raw.copy()
else:
    df = df_raw.copy()

# ------------------------------------------------------
# SECTION A: RANKING (PLOTLY)
# ------------------------------------------------------
st.header("Section A: Motivation Ranking")
motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Average Score']

fig_ranking = px.bar(
    motivation_means, x='Average Score', y='Motivation',
    orientation='h', text_auto='.2f',
    color='Average Score', color_continuous_scale='Viridis',
    title=f"Average Agreement Score ({selected_gender if 'Gender' in df_raw.columns else 'Overall'})"
)
fig_ranking.update_layout(xaxis_range=[1, 5], title={'x': 0.5, 'xanchor': 'center'})
st.plotly_chart(fig_ranking, use_container_width=True)

# ------------------------------------------------------
# SECTION B: CONSUMER SENTIMENT (MATPLOTLIB/SEABORN)
# ------------------------------------------------------
st.divider()
st.header("Section B: Deep Dive into Motivations")

# Calculate the percentages for the Likert chart
df_motivation_pct = calculate_percentages(df, motivation_cols)

# Sidebar toggle for labels
show_labels = st.sidebar.checkbox("Show Percentage Labels", value=True)

# Plotting Logic
sns.set_style("whitegrid")
plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

fig, ax = plt.subplots(figsize=(12, 8))
df_motivation_pct[plot_columns].plot(
    kind='barh', stacked=True, color=colors, ax=ax, width=0.8
)

# Customizing the visual
ax.set_title('Percentage Distribution of Responses', fontsize=16, pad=20)
ax.set_xlabel('Percentage of Respondents (%)', fontsize=12)
ax.set_ylabel('Motivation Question', fontsize=12)
ax.set_xlim(0, 100)

if show_labels:
    for c in ax.containers:
        # Only show label if segment is large enough (>5%) to prevent clutter
        labels = [f'{w:.1f}%' if (w := v.get_width()) > 5 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', fontsize=9)

ax.legend(title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Display in Streamlit
st.pyplot(fig)

# --- BLUE INTERPRETATION BOX ---
st.info(f"""
**Data Interpretation ({selected_gender if 'Gender' in df_raw.columns else 'Overall'}):**
The chart shows a strong positive sentiment across most motivations. 
The **Agree** (light green) and **Strongly Agree** (dark green) categories dominate, 
suggesting that respondents are generally well-aligned with the brand's social media goals. 
Watch for red or orange segments which indicate potential friction points.
""")

# ------------------------------------------------------
# SECTION C: RELATIONSHIPS (CORRELATION)
# ------------------------------------------------------
st.divider()
st.header("Section C: Engagement Relationships")
tab_corr, tab_rel = st.tabs(["Correlation Heatmap", "Relationship Scatters"])

with tab_corr:
    corr_matrix = df[motivation_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix, text_auto=".2f",
        color_continuous_scale='RdBu_r',
        title="How Motivations Move Together"
    )
    fig_heatmap.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab_rel:
    col_x, col_y = st.columns([1, 2])
    with col_x:
        x_var = st.selectbox("Select X-axis", motivation_cols, index=0)
        y_var = st.selectbox("Select Y-axis", motivation_cols, index=1)
        st.metric("Correlation", f"{df[x_var].corr(df[y_var]):.2f}")
    with col_y:
        fig_scatter = px.scatter(df, x=x_var, y=y_var, opacity=0.4, trendline="ols")
        st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
st.markdown("✔ **Consumer Motivation Analysis Complete**")
