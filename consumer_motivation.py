import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
# SECTION B: CONSUMER SENTIMENT (DISTRIBUTIONS)
# ======================================================
st.divider()
st.header("Section B: Deep Dive into Motivations")

# 1. CALCULATE PERCENTAGES (Fixes the NameError)
def calculate_percentages(df, columns):
    # Mapping numeric scores back to labels for the chart
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    
    pct_list = []
    for col in columns:
        # Get counts of each score (1-5), ensure all 1-5 are present even if 0
        counts = df[col].value_counts(normalize=True).reindex([1, 2, 3, 4, 5], fillvalue=0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    
    return pd.DataFrame(pct_list)

# Generate the missing dataframe
df_motivation_pct = calculate_percentages(df, motivation_cols)

# 2. DATA PROCESSING FOR PLOT
@st.cache_data
def process_data(df_input):
    df_pos = df_input.copy()
    # We keep them positive for a standard stacked bar
    for col in ['Strongly Disagree', 'Disagree']:
        if col in df_pos.columns:
            df_pos[col] = df_pos[col].abs()
    return df_pos

df_motivation_pct_positive = process_data(df_motivation_pct)

# 3. SIDEBAR CONTROLS
st.sidebar.header("Chart Options")
show_labels = st.sidebar.checkbox("Show Percentage Labels", value=True)

# 4. PLOTTING
sns.set_style("whitegrid")
plot_columns_positive = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
colors_positive = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

fig, ax = plt.subplots(figsize=(12, 8))
df_motivation_pct_positive[plot_columns_positive].plot(
    kind='barh', stacked=True, color=colors_positive, ax=ax, width=0.8
)

ax.set_title('Percentage Distribution of Responses', fontsize=16)
ax.set_xlabel('Percentage of Respondents (%)', fontsize=12)
ax.set_xlim(0, 100)

if show_labels:
    for c in ax.containers:
        labels = [f'{w:.1f}%' if (w := v.get_width()) > 5 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', fontsize=9)

ax.legend(title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# 5. DISPLAY
st.pyplot(fig)

# --- BLUE INTERPRETATION BOX ---
st.info("""
**Data Interpretation:**
This chart shows a positive skew in consumer motivation. The majority of respondents 
fall into the **Agree** (light green) and **Strongly Agree** (dark green) categories. 
The areas in red indicate specific questions where intervention may be needed to 
address underlying dissatisfaction or lack of interest.
""")

# ======================================================
# SECTION C: RELATIONSHIPS
# ======================================================
st.divider()
st.header("Section C: Engagement Relationships")

tab_corr, tab_rel = st.tabs(["Correlation Heatmap", "Relationship Scatters"])

with tab_corr:
    st.write("### How motivations move together")
    corr_matrix = df[motivation_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix, text_auto=".2f",
        color_continuous_scale='RdBu_r',
        title="Correlation Heatmap"
    )
    st.plotly_chart(center_title(fig_heatmap), use_container_width=True)
    
    with st.expander("📝 Detailed Interpretation: Heatmap Correlation"):
        st.write("""
        * **Positive Correlation (Blue):** When two motivations are highly correlated (e.g., > 0.60), it means users who follow for one reason are very likely to follow for the other. 
        * **Strategic Value:** High correlations allow brands to "bundle" content. For example, if 'Entertainment' and 'Style' correlate, entertaining videos should always showcase product style.
        """)

with tab_rel:
    c1, c2 = st.columns([1, 2])
    with c1:
        x_var = st.selectbox("Select X-axis", motivation_cols, index=0)
        y_var = st.selectbox("Select Y-axis", motivation_cols, index=min(1, len(motivation_cols)-1))
        
        current_corr = df[x_var].corr(df[y_var])
        st.write(f"**Correlation Coefficient:** {current_corr:.2f}")
        
        if current_corr > 0.6:
            st.success("Analysis: **Strong Relationship**. These two factors are deeply linked in the consumer's mind.")
        elif current_corr > 0.3:
            st.warning("Analysis: **Moderate Relationship**. There is a visible trend, but other factors are also at play.")
        else:
            st.error("Analysis: **Weak Relationship**. These factors operate independently of one another.")
    
    with c2:
        try:
            import statsmodels
            t_line = "ols"
        except ImportError:
            t_line = None
            
        fig_scatter = px.scatter(
            df, x=x_var, y=y_var, 
            trendline=t_line, 
            opacity=0.4,
            title=f"Relationship: {x_var} vs {y_var}"
        )
        st.plotly_chart(center_title(fig_scatter), use_container_width=True)

st.divider()
st.markdown("✔ **Consumer Motivation Analysis Complete**")
