import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ======================================================
# 1. HELPERS & CONFIG
# ======================================================
def center_title(fig):
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return fig

# ======================================================
# 2. DATA LOADING & MAPPING
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

df_raw, motivation_questions = load_motivation_data()

# ======================================================
# 3. PAGE TITLE & IN-PAGE FILTER
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")

# --- IN-PAGE FILTER SECTION ---
st.markdown("### 🔍 Filter Analysis")
col_filt1, col_filt2 = st.columns([1, 2])

with col_filt1:
    if 'Gender' in df_raw.columns:
        gender_options = ["All Genders"] + sorted(list(df_raw['Gender'].unique()))
        selected_gender = st.selectbox("View by Demographic:", gender_options)
        
        if selected_gender != "All Genders":
            df = df_raw[df_raw['Gender'] == selected_gender].copy()
        else:
            df = df_raw.copy()
    else:
        df = df_raw.copy()
        selected_gender = "All Genders"

with col_filt2:
    st.info(f"Showing results for **{selected_gender}**. Adjust the dropdown to filter the charts below.")

# ======================================================
# 4. TOP-LEVEL KPI METRICS
# ======================================================
if not df.empty:
    m_scores = df[motivation_questions].mean()
    top_m = m_scores.idxmax()
    top_val = m_scores.max()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Respondents", len(df))
    m2.metric("Primary Motivation", top_m)
    m3.metric("Highest Avg Score", f"{top_val:.2f} / 5")
else:
    st.warning("No data found for this selection.")
    st.stop()

st.divider()

# ======================================================
# 5. ANALYSIS TABS
# ======================================================
tab1, tab2, tab3 = st.tabs(["📈 Sentiment Ranking", "🔗 Relationships", "👥 Demographic Gap"])

with tab1:
    # --- RANKING CHART ---
    st.subheader("Section A: Motivation Ranking")
    ranking_data = m_scores.sort_values(ascending=True).reset_index()
    ranking_data.columns = ['Motivation', 'Avg Score']
    
    fig_rank = px.bar(
        ranking_data, x='Avg Score', y='Motivation',
        orientation='h', text_auto='.2f',
        color='Avg Score', color_continuous_scale='Viridis',
        title="Average Agreement (1-5)"
    )
    fig_rank.update_layout(xaxis_range=[1, 5])
    st.plotly_chart(center_title(fig_rank), use_container_width=True)

    st.divider()

    # --- INDIVIDUAL DISTRIBUTIONS ---
    st.subheader("Section B: Detailed Distribution")
    
    
    # Use 2 columns for smaller distribution charts
    dist_col1, dist_col2 = st.columns(2)
    for i, col_name in enumerate(motivation_questions):
        counts = df[col_name].value_counts().sort_index().reset_index()
        counts.columns = ['Score', 'Respondents']
        
        fig_dist = px.bar(
            counts, x='Score', y='Respondents', text='Respondents',
            title=f"Distribution: {col_name}",
            color='Score', color_continuous_scale='Plasma'
        )
        fig_dist.update_layout(showlegend=False, height=300)
        
        target = dist_col1 if i % 2 == 0 else dist_col2
        with target:
            st.plotly_chart(center_title(fig_dist), use_container_width=True)
            st.markdown("---")

with tab2:
    st.subheader("Section C: Connection Analysis")
    
    
    rel_col1, rel_col2 = st.columns([1, 1.2])
    
    with rel_col1:
        st.write("**Correlation Matrix**")
        corr = df[motivation_questions].corr()
        fig_heat = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with rel_col2:
        st.write("**Trend Exploration**")
        x_ax = st.selectbox("Predictor (X):", motivation_questions, index=0)
        y_ax = st.selectbox("Outcome (Y):", motivation_questions, index=1)
        
        fig_scat = px.scatter(df, x=x_ax, y=y_ax, trendline="ols", opacity=0.4)
        st.plotly_chart(fig_scat, use_container_width=True)

with tab3:
    st.subheader("Section D: Gender Motivation Disparity")
    # We compare the RAW data here to see the gap between groups
    if 'Gender' in df_raw.columns and len(df_raw['Gender'].unique()) > 1:
        g_means = df_raw.groupby('Gender')[motivation_questions].mean().T.reset_index()
        df_melted = g_means.melt(id_vars='index', var_name='Gender', value_name='Score')
        df_melted.rename(columns={'index': 'Motivation'}, inplace=True)
        
        fig_dumb, ax_dumb = plt.subplots(figsize=(10, 6))
        sns.pointplot(
            data=df_melted, x='Score', y='Motivation', hue='Gender',
            join=True, palette={'Female': '#E74C3C', 'Male': '#3498DB'},
            markers='o', ax=ax_dumb
        )
        ax_dumb.set_xlim(1, 5)
        ax_dumb.set_title("Gender Mean Scores comparison", fontsize=14)
        st.pyplot(fig_dumb)
        
        st.info("The dumbbell plot highlights areas where Male and Female consumers prioritize different factors.")
    else:
        st.warning("Gender comparison is unavailable for this dataset.")

# ======================================================
# 6. FOOTER
# ======================================================
st.divider()
st.caption(f"Consumer Motivation Analysis • {pd.Timestamp.now().year}")
