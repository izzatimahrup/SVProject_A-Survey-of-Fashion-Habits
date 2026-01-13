import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# PAGE CONFIG
# ======================================================
# Note: set_page_config must be the first Streamlit command.
# If this is a sub-page in a multi-page app, this might need to be in main.py.
if 'page_config_set' not in st.session_state:
    st.set_page_config(page_title="Fashion Motivation Dashboard", layout="wide")
    st.session_state.page_config_set = True

# Helper to center Plotly titles
def center_title(fig):
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return fig

# ======================================================
# LOAD & MAP DATA
# ======================================================
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
    
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].astype(str).str.strip()
        
    return data, valid_cols

df, motivation_cols = load_motivation_data()

# ======================================================
# SIDEBAR FILTERS (Page Specific)
# ======================================================
with st.sidebar:
    st.header("🎯 Page Filters")
    if 'Gender' in df.columns:
        gender_list = ["All"] + sorted(list(df['Gender'].unique()))
        selected_gender = st.selectbox("Filter by Gender", gender_list)
        
        filtered_df = df.copy() if selected_gender == "All" else df[df['Gender'] == selected_gender]
    else:
        filtered_df = df.copy()
    
    st.divider()
    st.caption("Filters only apply to this current analysis page.")

# ======================================================
# HEADER SECTION
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")
st.markdown("Analyzing why consumers engage with fashion brands on social media.")

# Quick KPIs
m1, m2, m3 = st.columns(3)
m1.metric("Total Sample Size", len(filtered_df))
m2.metric("Primary Driver", filtered_df[motivation_cols].mean().idxmax())
m3.metric("Highest Avg Score", f"{filtered_df[motivation_cols].mean().max():.2f}")

# ======================================================
# SECTION A: MOTIVATION RANKING
# ======================================================
st.divider()
st.header("Section A: Motivation Ranking")

motivation_means = filtered_df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Average Score']

fig_ranking = px.bar(
    motivation_means, x='Average Score', y='Motivation',
    orientation='h', text_auto='.2f',
    color='Average Score', color_continuous_scale='Viridis',
    title="Average Agreement Score (Likert 1-5)"
)
fig_ranking.update_layout(xaxis_range=[1, 5])
st.plotly_chart(center_title(fig_ranking), use_container_width=True)

with st.expander("📝 Detailed Interpretation: Ranking Analysis"):
    top_m = motivation_means.iloc[-1]['Motivation']
    bot_m = motivation_means.iloc[0]['Motivation']
    st.write(f"""
    * **Primary Driver:** The highest-ranked motivation is **{top_m}**.
    * **Opportunity Gap:** The lowest score for **{bot_m}** suggests an area for potential growth or a niche interest.
    """)

# ======================================================
# SECTION B: DEEP DIVE (DISTRIBUTIONS)
# ======================================================
st.divider()
st.header("Section B: Deep Dive into Motivations")

col1, col2 = st.columns(2)
for i, col_name in enumerate(motivation_cols):
    counts = filtered_df[col_name].value_counts().sort_index().reset_index()
    counts.columns = ['Score', 'Respondents']
    avg_score = filtered_df[col_name].mean()
    
    fig_dist = px.bar(
        counts, x='Score', y='Respondents', text='Respondents',
        title=f"Distribution: {col_name}",
        color='Score', color_continuous_scale='Plasma'
    )
    fig_dist.update_layout(showlegend=False, height=350, xaxis_title="1 (Disagree) to 5 (Agree)")
    
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.plotly_chart(center_title(fig_dist), use_container_width=True)
        
        # Dynamic Logic
        if avg_score >= 3.8:
            status = "ranks as a **top driver**."
        elif avg_score >= 3.0:
            status = "is a **moderate driver**."
        else:
            status = "ranks as a **minor driver**."
        
        st.write(f"**Analysis:** {status}")
        st.markdown("---")

# ======================================================
# SECTION C: RELATIONSHIPS & GENDER
# ======================================================
st.divider()
st.header("Section C: Engagement Relationships & Demographics")

tab1, tab2, tab3 = st.tabs(["Correlation Heatmap", "Relationship Scatters", "Gender Comparison"])

with tab1:
    st.write("### How motivations move together")
    corr_matrix = filtered_df[motivation_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix, text_auto=".2f",
        color_continuous_scale='RdBu_r', title="Correlation Heatmap"
    )
    st.plotly_chart(center_title(fig_heatmap), use_container_width=True)

with tab2:
    c_side, c_plot = st.columns([1, 2])
    with c_side:
        x_var = st.selectbox("Select X-axis", motivation_cols, index=0)
        y_var = st.selectbox("Select Y-axis", motivation_cols, index=1)
        r_val = filtered_df[x_var].corr(filtered_df[y_var])
        st.write(f"**Correlation Coefficient:** {r_val:.2f}")
        
    with c_plot:
        fig_scatter = px.scatter(
            filtered_df, x=x_var, y=y_var, 
            trendline="ols" if len(filtered_df) > 2 else None,
            opacity=0.4, title=f"Trend: {x_var} vs {y_var}"
        )
        st.plotly_chart(center_title(fig_scatter), use_container_width=True)

with tab3:
    st.write("### Mean Motivation Scores by Gender")
    if 'Gender' in df.columns and len(df['Gender'].unique()) > 1:
        # Step 1: Calculate distributions per gender
        gender_means_list = []
        for g in df['Gender'].unique():
            g_df = df[df['Gender'] == g]
            g_means = g_df[motivation_cols].mean()
            g_means.name = g
            gender_means_list.append(g_means)
        
        df_gender_means = pd.concat(gender_means_list, axis=1).reset_index()
        df_melted = df_gender_means.melt(id_vars='index', var_name='Gender', value_name='Mean Score')
        df_melted.rename(columns={'index': 'Motivation Question'}, inplace=True)

        

        # Step 2: Plot
        fig_dumb, ax_dumb = plt.subplots(figsize=(10, 6))
        sns.pointplot(
            data=df_melted, x='Mean Score', y='Motivation Question', hue='Gender',
            join=True, palette={'Female': '#E74C3C', 'Male': '#3498DB'},
            markers='o', scale=0.8, ax=ax_dumb
        )
        ax_dumb.set_xlim(1, 5)
        ax_dumb.set_title("Gender Disparity in Motivations", fontsize=14)
        st.pyplot(fig_dumb)
    else:
        st.warning("Insufficient gender data for comparison.")

# ======================================================
# FOOTER
# ======================================================
st.divider()
st.markdown("✔ **Consumer Motivation Analysis Complete**")
