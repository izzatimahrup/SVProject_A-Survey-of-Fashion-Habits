import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ======================================================
# 1. PAGE CONFIG & HELPERS
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
# 3. CALCULATION HELPERS (FIXED FOR PYTHON 3.13)
# ======================================================
def calculate_percentages(df_input, columns):
    """Ensures type safety between float/int indexes for Python 3.13"""
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    
    for col in columns:
        # Convert to numeric and remove NaNs
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        counts = series.value_counts(normalize=True)
        
        # FIX: Explicitly cast index to integer before reindexing
        counts.index = counts.index.astype(int)
        
        # FIX: Reindex and then multiply by 100 separately
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0)
        counts = counts * 100
        
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
        
    return pd.DataFrame(pct_list)

# ======================================================
# 5. HEADER & TOP-LEVEL METRICS
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")
st.markdown(f"**Current View:** {selected_gender}")

if not df.empty:
    m_scores = df[motivation_questions].mean()
    top_m = m_scores.idxmax()
    top_val = m_scores.max()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Sample Size", len(df))
    kpi2.metric("Top Motivation", top_m)
    kpi3.metric("Highest Avg Score", f"{top_val:.2f} / 5")
else:
    st.error("No data available for the selected filter.")
    st.stop()

st.divider()

# ======================================================
# 6. STRUCTURED CONTENT (TABS)
# ======================================================
tab1, tab2, tab3 = st.tabs(["📈 Distributions", "🔗 Relationships", "👥 Comparative View"])

# --- TAB 1: RANKING & SPREAD ---
with tab1:
    st.header("Section A: Motivation Ranking")
    
    # Ranking Plotly Bar
    ranking_data = m_scores.sort_values(ascending=True).reset_index()
    ranking_data.columns = ['Motivation', 'Avg Score']
    
    fig_rank = px.bar(
        ranking_data, x='Avg Score', y='Motivation',
        orientation='h', text_auto='.2f',
        color='Avg Score', color_continuous_scale='Viridis',
        title="Average Agreement Score"
    )
    fig_rank.update_layout(xaxis_range=[1, 5])
    st.plotly_chart(center_title(fig_rank), use_container_width=True)

    st.divider()
    
    # Detailed Distributions (2 columns)
    st.header("Section B: Deep Dive into Distributions")
    col_a, col_b = st.columns(2)
    
    for i, col_name in enumerate(motivation_questions):
        counts = df[col_name].value_counts().sort_index().reset_index()
        counts.columns = ['Score', 'Respondents']
        avg_score = df[col_name].mean()
        
        fig_dist = px.bar(
            counts, x='Score', y='Respondents', text='Respondents',
            title=f"Distribution: {col_name}",
            color='Score', color_continuous_scale='Plasma'
        )
        fig_dist.update_layout(showlegend=False, height=350)
        
        target = col_a if i % 2 == 0 else col_b
        with target:
            st.plotly_chart(center_title(fig_dist), use_container_width=True)
            
            # Dynamic Insight
            if avg_score >= 3.8:
                st.success(f"**Top Driver:** {col_name} shows strong agreement.")
            elif avg_score >= 3.0:
                st.info(f"**Moderate Driver:** {col_name} shows neutral to positive lean.")
            else:
                st.warning(f"**Minor Driver:** {col_name} has lower impact.")
            st.markdown("---")

# --- TAB 2: CORRELATIONS ---
with tab2:
    st.header("Section C: Engagement Relationships")
    
    c_heat, c_scatter = st.columns([1, 1.2])
    
    with c_heat:
        st.write("**Correlation Matrix**")
        corr = df[motivation_questions].corr()
        fig_heat = px.imshow(
            corr, text_auto=".2f",
            color_continuous_scale='RdBu_r', aspect="auto"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with c_scatter:
        st.write("**Trend Explorer**")
        x_ax = st.selectbox("X-Axis", motivation_questions, index=0)
        y_ax = st.selectbox("Y-Axis", motivation_questions, index=1)
        
        fig_scat = px.scatter(
            df, x=x_ax, y=y_ax, 
            trendline="ols", opacity=0.5,
            title=f"Trend: {x_ax} vs {y_ax}"
        )
        st.plotly_chart(fig_scat, use_container_width=True)

# --- TAB 3: GENDER COMPARISON (DUMBBELL) ---
with tab3:
    st.header("Section D: Gender Disparity Analysis")
    
    if 'Gender' in df_raw.columns and len(df_raw['Gender'].unique()) > 1:
        # Calculate means per gender (Using df_raw so comparison is always visible)
        g_means = df_raw.groupby('Gender')[motivation_questions].mean().T.reset_index()
        df_melted = g_means.melt(id_vars='index', var_name='Gender', value_name='Score')
        df_melted.rename(columns={'index': 'Motivation'}, inplace=True)
        
        # Seaborn Dumbbell Plot
        fig_dumb, ax_dumb = plt.subplots(figsize=(10, 6))
        sns.pointplot(
            data=df_melted, x='Score', y='Motivation', hue='Gender',
            join=True, palette={'Female': '#E74C3C', 'Male': '#3498DB'},
            markers='o', ax=ax_dumb
        )
        ax_dumb.set_xlim(1, 5)
        ax_dumb.grid(True, axis='x', linestyle='--', alpha=0.5)
        st.pyplot(fig_dumb)
        
        st.info("**Tip:** Points further apart indicate a larger perception gap between genders.")
    else:
        st.warning("Insufficient demographic data for comparison.")

# ======================================================
# 7. FOOTER
# ======================================================
st.divider()
st.caption(f"Fashion Habits Research • Motivation Module • {pd.Timestamp.now().year}")
