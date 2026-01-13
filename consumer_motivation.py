import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. SETTINGS & STYLING
# ==========================================
# It's better to let main.py handle set_page_config, 
# but we define a custom style for our charts here.
CHART_THEME = "RdYlGn" # Red-Yellow-Green for Likert scales
BAR_COLOR = "#2E86C1"   # Professional blue

# ==========================================
# 2. DATA LOADING & MAPPING
# ==========================================
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

# ==========================================
# 3. CALCULATION HELPERS
# ==========================================
def calculate_percentages(df_input, columns):
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    for col in columns:
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        counts = series.value_counts(normalize=True).astype(float)
        counts.index = counts.index.astype(int)
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    return pd.DataFrame(pct_list)

# ==========================================
# 4. SIDEBAR & FILTERS
# ==========================================
with st.sidebar:
    st.header("🎛️ Dashboard Controls")
    if 'Gender' in df_raw.columns:
        gender_options = ["All Genders"] + sorted(list(df_raw['Gender'].unique()))
        selected_gender = st.selectbox("Select Demographic", gender_options)
        
        if selected_gender != "All Genders":
            df = df_raw[df_raw['Gender'] == selected_gender].copy()
        else:
            df = df_raw.copy()
    else:
        df = df_raw.copy()
        selected_gender = "Overall"

    st.divider()
    st.caption("Data Source: GitHub / Cleaned_FashionHabitGF.csv")

# ==========================================
# 5. HEADER & KPIS
# ==========================================
st.title("📊 Consumer Motivation Analysis")
st.markdown(f"Currently viewing analysis for: **{selected_gender}**")

# Calculate metrics for the top row
means_all = df[motivation_questions].mean()
top_motivation = means_all.idxmax()
top_score = means_all.max()

m1, m2, m3 = st.columns(3)
m1.metric("Total Respondents", len(df))
m2.metric("Primary Driver", top_motivation)
m3.metric("Highest Avg Score", f"{top_score:.2f} / 5")

st.divider()

# ==========================================
# 6. STRUCTURED CONTENT (TABS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📈 Sentiment Distribution", "🔗 Relationships", "👥 Demographics"])

with tab1:
    st.subheader("How strongly do consumers agree with these drivers?")
    
    # 1. Ranking Bar Chart
    col_rank, col_desc = st.columns([2, 1])
    with col_rank:
        means_sorted = means_all.sort_values(ascending=True)
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(x=means_sorted.values, y=means_sorted.index, color=BAR_COLOR, ax=ax1)
        ax1.set_xlim(0, 5)
        ax1.set_xlabel("Mean Score (1-5)")
        st.pyplot(fig1)
    
    with col_desc:
        st.write("### Quick Insights")
        st.write(f"The most significant motivation is **{top_motivation}**.")
        st.info("Scores above 3.0 indicate general agreement with the statement.")

    st.divider()

    # 2. Likert Distribution
    st.subheader("Detailed Response Spread")
    df_pct = calculate_percentages(df, motivation_questions)
    likert_colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    df_pct[['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']].plot(
        kind='barh', stacked=True, color=likert_colors, ax=ax2, width=0.8
    )
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("Percentage of Respondents (%)")
    ax2.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    st.pyplot(fig2)

with tab2:
    st.subheader("Correlation & Regression")
    
    col_heat, col_reg = st.columns([1, 1])
    
    with col_heat:
        st.write("**Correlation Matrix**")
        corr = df[motivation_questions].corr()
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3, cbar=False)
        st.pyplot(fig3)
    
    with col_reg:
        st.write("**Trend Analysis**")
        x_var = st.selectbox("Compare (X-Axis):", motivation_questions, index=0)
        y_var = st.selectbox("Against (Y-Axis):", motivation_questions, index=1)
        
        fig4, ax4 = plt.subplots()
        sns.regplot(data=df, x=x_var, y=y_var, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax4)
        ax4.set_title(f"Correlation: {df[x_var].corr(df[y_var]):.2f}")
        st.pyplot(fig4)

with tab3:
    st.subheader("Gender-Based Motivation Gap")
    if 'Gender' in df_raw.columns and len(df_raw['Gender'].unique()) > 1:
        # Prepare dumbbell data
        g_means = df_raw.groupby('Gender')[motivation_questions].mean().T.reset_index()
        df_melted = g_means.melt(id_vars='index', var_name='Gender', value_name='Score')
        df_melted.rename(columns={'index': 'Motivation Question'}, inplace=True)
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.pointplot(data=df_melted, x='Score', y='Motivation Question', hue='Gender', 
                      join=True, palette='Set1', markers='D', ax=ax5)
        ax5.set_xlim(1, 5)
        ax5.grid(axis='x', linestyle='--', alpha=0.7)
        st.pyplot(fig5)
        
        st.expander("What does this tell us?").write("""
            The dumbbell plot shows the distance between Male and Female mean scores. 
            A wider gap indicates that gender significantly influences that specific motivation.
        """)
    else:
        st.warning("Insufficient data categories for gender comparison.")

# ==========================================
# 7. FOOTER
# ==========================================
st.divider()
st.caption(f"Analysis generated for Fashion Habits Research Project • {pd.Timestamp.now().year}")
