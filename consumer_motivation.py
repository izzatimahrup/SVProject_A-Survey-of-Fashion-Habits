import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. DATA LOADING & MAPPING
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

# Initialize the dataset locally for this page
df_raw, motivation_questions = load_motivation_data()

# ==========================================
# 2. CALCULATION HELPERS
# ==========================================
def calculate_percentages(df_input, columns):
    label_map = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
    pct_list = []
    for col in columns:
        # Convert to numeric and remove NaNs to prevent calculation errors
        series = pd.to_numeric(df_input[col], errors='coerce').dropna()
        counts = series.value_counts(normalize=True).astype(float)
        counts.index = counts.index.astype(int)
        counts = counts.reindex([1, 2, 3, 4, 5], fillvalue=0.0) * 100
        counts.index = counts.index.map(label_map)
        counts.name = col
        pct_list.append(counts)
    return pd.DataFrame(pct_list)

# ==========================================
# 3. PAGE-SPECIFIC SIDEBAR FILTERING
# ==========================================
with st.sidebar:
    st.header("🎯 Page Filters")
    st.markdown("Filter values for this page only.")
    
    # Check if Gender exists and create a multiselect for more flexibility
    if 'Gender' in df_raw.columns:
        gender_list = sorted(list(df_raw['Gender'].unique()))
        selected_genders = st.multiselect(
            "Filter by Gender", 
            options=gender_list, 
            default=gender_list
        )
        # Apply the local filter
        df = df_raw[df_raw['Gender'].isin(selected_genders)].copy()
    else:
        df = df_raw.copy()
        selected_genders = ["N/A"]

    st.divider()
    if st.button("Reset Page Filters"):
        st.rerun()

# ==========================================
# 4. HEADER & METRICS
# ==========================================
st.title("📊 Consumer Motivation Analysis")
st.info(f"Currently filtering for: {', '.join(selected_genders)}")

# Calculate metrics based on the FILTERED dataframe
if not df.empty:
    means_all = df[motivation_questions].mean()
    top_motivation = means_all.idxmax()
    top_score = means_all.max()

    m1, m2, m3 = st.columns(3)
    m1.metric("Respondents in View", len(df))
    m2.metric("Primary Driver", top_motivation)
    m3.metric("Avg Score", f"{top_score:.2f} / 5")
else:
    st.warning("No data found for the selected filters.")
    st.stop()

st.divider()

# ==========================================
# 5. STRUCTURED TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["📈 Sentiment Analysis", "🔗 Relationships", "👥 Comparative View"])

with tab1:
    # --- RANKING SECTION ---
    st.subheader("Motivation Ranking")
    col_chart, col_text = st.columns([2, 1])
    
    with col_chart:
        means_sorted = means_all.sort_values(ascending=True)
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(x=means_sorted.values, y=means_sorted.index, palette="Blues_d", ax=ax1)
        ax1.set_xlim(0, 5)
        ax1.set_xlabel("Average Likert Score")
        st.pyplot(fig1)
        
    with col_text:
        st.markdown("### Insights")
        st.write(f"The motivation **{top_motivation}** shows the highest level of consumer alignment.")
        st.caption("A score of 3.0 represents a neutral stance.")

    st.divider()

    # --- LIKERT DISTRIBUTION SECTION ---
    st.subheader("Detailed Sentiment Distribution")
    
    df_pct = calculate_percentages(df, motivation_questions)
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"] # Standard diverge scale
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    df_pct[['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']].plot(
        kind='barh', stacked=True, color=colors, ax=ax2, width=0.75
    )
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("Percentage (%)")
    ax2.legend(title="Response", bbox_to_anchor=(1.0, 1), loc='upper left')
    st.pyplot(fig2)

with tab2:
    st.subheader("Motivation Interconnectivity")
    
    
    c_heat, c_reg = st.columns([1, 1.2])
    
    with c_heat:
        st.write("**Correlation Matrix**")
        corr = df[motivation_questions].corr()
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, fmt=".2f", ax=ax3, cbar=False)
        st.pyplot(fig3)
    
    with c_reg:
        st.write("**Exploratory Regression**")
        x_col = st.selectbox("Predictor (X):", motivation_questions, index=0)
        y_col = st.selectbox("Outcome (Y):", motivation_questions, index=1)
        
        fig4, ax4 = plt.subplots()
        sns.regplot(data=df, x=x_col, y=y_col, scatter_kws={'alpha':0.3}, line_kws={'color':'#E74C3C'}, ax=ax4)
        st.pyplot(fig4)

with tab3:
    st.subheader("Gender Comparison Analysis")
    # Note: We use df_raw here to ensure we always see the comparison regardless of sidebar filters
    if 'Gender' in df_raw.columns and len(df_raw['Gender'].unique()) > 1:
        g_means = df_raw.groupby('Gender')[motivation_questions].mean().T.reset_index()
        df_melted = g_means.melt(id_vars='index', var_name='Gender', value_name='Score')
        df_melted.rename(columns={'index': 'Question'}, inplace=True)
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.pointplot(data=df_melted, x='Score', y='Question', hue='Gender', 
                      dodge=True, join=False, palette='coolwarm', markers='o', ax=ax5)
        ax5.set_xlim(1, 5)
        ax5.set_title("Gender Disparity in Engagement Drivers")
        st.pyplot(fig5)
    else:
        st.warning("No gender data available for comparative analysis.")

st.divider()
st.caption(f"Consumer Motivation Analysis Module • Version 2.1 • {pd.Timestamp.now().strftime('%Y-%m-%d')}")
