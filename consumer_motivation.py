import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Motivation Analysis", layout="wide")

# Custom CSS to improve look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LAYER ---
@st.cache_data
def load_and_clean_data():
    """
    Simulates data loading and cleaning. 
    Replace this with: df = pd.read_csv('data.csv')
    """
    questions = [
        'follow_for_updates_promotions', 'follow_because_like_products',
        'follow_because_entertaining', 'follow_because_discounts_contests',
        'follow_because_express_personality', 'follow_because_online_community',
        'follow_because_support_loyalty'
    ]
    # Generating dummy data
    np.random.seed(42)
    data = np.random.randint(1, 6, size=(200, len(questions)))
    df = pd.DataFrame(data, columns=questions)
    df['Gender'] = np.random.choice(['Male', 'Female', 'Non-Binary'], size=200)
    return df, questions

df, motivation_questions = load_and_clean_data()

# --- HEADER SECTION ---
st.title("📊 Consumer Motivation Analytics")
st.info("Analyze why users follow and engage with brands using Likert-scale survey data.")

# --- IN-PAGE FILTER SECTION ---
with st.expander("🎯 Global Filters", expanded=True):
    col_a, col_b = st.columns([2, 3])
    with col_a:
        all_genders = df['Gender'].unique().tolist()
        selected_genders = st.multiselect(
            "Filter by Gender:", 
            options=all_genders, 
            default=all_genders
        )
    with col_b:
        st.write("") # Spacer
        st.caption(f"Showing data for {len(df[df['Gender'].isin(selected_genders)])} respondents.")

# Apply Global Filter
filtered_df = df[df['Gender'].isin(selected_genders)]

# --- DASHBOARD SECTIONS (TABS) ---
tab_overview, tab_rel, tab_dist, tab_gender = st.tabs([
    "📈 Performance Overview", 
    "🔗 Correlation Analysis", 
    "📊 Response Distribution", 
    "👥 Demographic Split"
])

# --- SECTION 1: OVERVIEW ---
with tab_overview:
    st.subheader("Mean Agreement Scores")
    st.write("Higher scores indicate stronger agreement with the motivation.")
    
    means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
    
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=means.values, y=means.index, palette='viridis', ax=ax1)
    ax1.set_xlim(0, 5)
    for i, v in enumerate(means.values):
        ax1.text(v + 0.05, i, f'{v:.2f}', va='center', fontweight='bold')
    
    st.pyplot(fig1)

# --- SECTION 2: CORRELATION & REGRESSION ---
with tab_rel:
    st.subheader("Motivation Interconnectivity")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Correlation Matrix**")
        corr = filtered_df[motivation_questions].corr()
        fig2, ax2 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='RdBu_r', fmt=".2f", ax=ax2)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig2)
        
    with col2:
        st.markdown("**Relationship Deep-Dive**")
        x_axis = st.selectbox("Predictor (X):", motivation_questions, index=1)
        y_axis = st.selectbox("Target (Y):", motivation_questions, index=5)
        
        fig3, ax3 = plt.subplots()
        sns.regplot(data=filtered_df, x=x_axis, y=y_axis, 
                    scatter_kws={'alpha':0.3}, line_kws={'color':'#e74c3c'}, ax=ax3)
        st.pyplot(fig3)

# --- SECTION 3: DISTRIBUTION ---
with tab_dist:
    st.subheader("Detailed Response Spread")
    
    # Calculate % distribution
    def get_distribution(data, qs):
        results = []
        for q in qs:
            c = data[q].value_counts(normalize=True).reindex(range(1,6), fill_value=0) * 100
            results.append(c.values)
        return pd.DataFrame(results, index=qs, 
                            columns=['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'])

    dist_df = get_distribution(filtered_df, motivation_questions)
    
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    dist_df.plot(kind='barh', stacked=True, 
                 color=["#d73027", "#fc8d59", "#eeeeee", "#91cf60", "#1a9850"], ax=ax4)
    ax4.legend(bbox_to_anchor=(1.0, 1.0))
    st.pyplot(fig4)

# --- SECTION 4: GENDER COMPARISON ---
with tab_gender:
    st.subheader("Gender-Based Divergence")
    
    if len(selected_genders) < 2:
        st.warning("Please select at least two genders in the global filter to compare differences.")
    else:
        # Data Prep for Dumbbell
        g_means = filtered_df.groupby('Gender')[motivation_questions].mean().T
        g_melted = g_means.reset_index().melt(id_vars='index', var_name='Gender', value_name='Score')
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.pointplot(data=g_melted, x='Score', y='index', hue='Gender',
                      join=True, markers='o', scale=1.2, ax=ax5)
        ax5.set_title("Mean Score Gap by Gender")
        ax5.set_xlabel("Likert Score (1-5)")
        ax5.set_ylabel("")
        st.pyplot(fig5)

# --- FOOTER ---
st.divider()
st.caption("Streamlit Motivation Dashboard v1.1 | Data updated: Jan 2026")
