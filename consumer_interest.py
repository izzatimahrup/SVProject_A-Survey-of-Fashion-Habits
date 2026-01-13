import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="Section C: Consumer Interests", layout="wide")

# --- CSS TWEAKS (FOR PERFECT SCREENSHOTS) ---
st.markdown("""
<style>
/* Metric Styling */
[data-testid="stMetricValue"] {
    font-size: 28px !important;
    word-wrap: break-word !important;
    white-space: normal !important;
    line-height: 1.1 !important;
}
/* Reduce padding at top */
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}
/* Reduce gap between elements */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.3rem;
}
/* Make info box compact */
.stAlert {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# --- 1. DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    file_path = "Cleaned_FashionHabitGF.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("Error: 'Cleaned_FashionHabitGF.csv' not found.")
        return pd.DataFrame()

    df = df.rename(columns={
        'Average Monthly Expenses (RM)': 'Budget',
        'Influence on Shopping': 'Influence',
        'Awareness of Fashion Trends': 'Awareness',
        'Employment Status': 'Job',
        '  How often do you buy fashion products (clothes, shoes, accessories)?  ': 'Frequency', 
        'Gender': 'Gender',
        'Age': 'Age',
        'Region': 'Region'
    })
    
    def clean_influence(val):
        val = str(val)
        if "Online community" in val: return "Online Community"
        if "Celebrities" in val: return "Influencers"
        if "Brand advertisements" in val: return "Ads"
        if "Family" in val: return "Family"
        if "Friends" in val: return "Friends"
        if "rely" in val: return "Self-Decision"
        return val
    df['Influence'] = df['Influence'].apply(clean_influence)
    
    # Ordering
    budget_order_logic = ["<500", "500-1000", "1000-3000", ">3000"]
    found_budget = [x for x in budget_order_logic if x in df['Budget'].unique()]
    other_budget = [x for x in df['Budget'].unique() if x not in found_budget]
    final_budget = found_budget + other_budget
    df['Budget'] = pd.Categorical(df['Budget'], categories=final_budget, ordered=True)
    
    freq_order_logic = [
        "Daily", "Every day", "Everyday", "Weekly", "Once a week", "Every week",
        "Monthly", "Once a month", "Every month", "Every 2-3 months", "Quarterly",
        "Every 6 months", "Twice a year", "Annually", "Once a year", "Yearly",
        "Rarely", "Never"
    ]
    found_freq = [x for x in freq_order_logic if x in df['Frequency'].unique()]
    other_freq = [x for x in df['Frequency'].unique() if x not in found_freq]
    final_freq = found_freq + other_freq
    if not final_freq: final_freq = sorted(df['Frequency'].dropna().unique().tolist())
    df['Frequency'] = pd.Categorical(df['Frequency'], categories=final_freq, ordered=True)

    df['Awareness_Str'] = df['Awareness'].astype(str)
    awareness_order = sorted(df['Awareness_Str'].unique().tolist())
    df['Awareness_Str'] = pd.Categorical(df['Awareness_Str'], categories=awareness_order, ordered=True)
    
    return df

# --- COLORS ---
CONSISTENT_COLORS = ["#003f5c", "#d62728", "#2ca02c", "#bcbd22", "#9467bd", "#17becf"]
CONSISTENT_SCALE = 'Blues'

# --- 2. PLOTLY CHART FUNCTIONS (Compact Height: 320px) ---

def chart_pie_budget(df):
    data = df['Budget'].value_counts().reset_index()
    data.columns = ['Budget', 'Count']
    fig = px.pie(data, values='Count', names='Budget', title="Distribution of Monthly Budget",
                 color_discrete_sequence=CONSISTENT_COLORS, hole=0, height=320)
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10)) 
    return fig

def chart_bar_awareness(df):
    data = df['Awareness_Str'].value_counts().sort_index().reset_index()
    data.columns = ['Awareness', 'Count']
    fig = px.bar(data, x='Awareness', y='Count', title="Self-Perceived Fashion Awareness Level",
                 labels={'Awareness': 'Awareness Level (1-5)', 'Count': 'Number of Respondents'},
                 color='Count', color_continuous_scale=CONSISTENT_SCALE, height=320)
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10))
    return fig

def chart_bar_influence(df):
    data = df['Influence'].value_counts().reset_index()
    data.columns = ['Influence', 'Count']
    fig = px.bar(data, x='Influence', y='Count', title="Top Influencing Factors Ranking",
                 labels={'Influence': 'Source of Influence', 'Count': 'Number of Respondents'},
                 color='Influence', color_discrete_sequence=CONSISTENT_COLORS, height=320)
    fig.update_layout(showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
    return fig

def chart_heatmap_freq_budget(df):
    fig = px.density_heatmap(df, x='Frequency', y='Budget', title="Matrix: Frequency vs. Budget",
                             labels={'Frequency': 'Shopping Frequency', 'Budget': 'Monthly Budget'},
                             color_continuous_scale=CONSISTENT_SCALE, height=320)
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10))
    return fig

def chart_bubble_awareness_budget(df):
    df_grouped = df.groupby(['Awareness_Str', 'Budget']).size().reset_index(name='Count')
    fig = px.scatter(df_grouped, x='Awareness_Str', y='Budget', size='Count', color='Count',
                     title="Correlation: Awareness vs. Budget",
                     labels={'Awareness_Str': 'Fashion Awareness (1-5)', 'Budget': 'Budget Range'},
                     size_max=50, color_continuous_scale=CONSISTENT_SCALE, height=320)
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10))
    return fig

def chart_stacked_influence_freq(df):
    df_grouped = df.groupby(['Influence', 'Frequency']).size().reset_index(name='Count')
    fig = px.bar(df_grouped, x='Influence', y='Count', color='Frequency',
                 title="Impact of Influences on Shopping Frequency",
                 labels={'Influence': 'Influence Source', 'Count': 'Count', 'Frequency': 'Frequency'},
                 color_discrete_sequence=CONSISTENT_COLORS, height=320)
    fig.update_layout(barmode='stack', margin=dict(t=40, b=10, l=10, r=10))
    return fig

# --- 3. MAIN APP LAYOUT ---
def app():
    st.title("SECTION C : CONSUMER INTERESTS ABOUT FASHION")
    
    # Objective Box
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 10px; border-left: 5px solid #003f5c; margin-bottom: 10px;">
        <h4 style="color: #003f5c; margin: 0; font-size: 16px;">Objective</h4>
        <p style="margin: 0; color: #333; font-size: 14px;">
            To analyze consumer interests in fashion by examining spending habits, trend awareness, and external drivers.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    if df.empty: return

    # --- FILTERS ---
    st.subheader("🔍 Filter Data Scope")
    f1, f2 = st.columns(2)
    with f1:
        region_options = df['Region'].unique().tolist()
        selected_regions = st.multiselect("Select Region (Scope):", region_options, default=region_options)
    with f2:
        gender_options = df['Gender'].unique().tolist()
        selected_genders = st.multiselect("Select Gender (Scope):", gender_options, default=gender_options)
    
    df_filtered = df[(df['Region'].isin(selected_regions)) & (df['Gender'].isin(selected_genders))]
    st.caption(f"Showing analysis for **{len(df_filtered)}** respondents.")
    st.markdown("---")
    
    if df_filtered.empty:
        st.warning("⚠️ No data available.")
        return

    # --- SCORECARD ---
    st.subheader("📊 Key Consumer Interest Summary")
    total_respondents = len(df_filtered)
    if not df_filtered.empty:
        top_budget = df_filtered['Budget'].mode()[0]
        top_influence = df_filtered['Influence'].mode()[0]
        avg_awareness_val = pd.to_numeric(df_filtered['Awareness'], errors='coerce').mean()
        avg_awareness = f"{avg_awareness_val:.1f} / 5.0" if not pd.isna(avg_awareness_val) else "N/A"
    else:
        top_budget, top_influence, avg_awareness = "N/A", "N/A", "N/A"

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Respondents", f"{total_respondents}")
    m2.metric("Majority Budget", top_budget)
    m3.metric("Top Influence", top_influence)
    m4.metric("Avg. Awareness", avg_awareness)
    
    st.markdown("---")

    # --- VISUALIZATIONS (COMPACT MODE) ---
    
    # 1. DISTRIBUTION (PIE)
    st.header("1. Spending Preferences")
    st.plotly_chart(chart_pie_budget(df_filtered), use_container_width=True)
    st.info("""
    **📝 Analysis:**
    * Most respondents have a budget under RM500, confirming high price sensitivity.
    * Brands must prioritize affordable, value-for-money products to convert interest into sales.
    """)
    st.markdown("---")
    
    # 2. AWARENESS LEVEL (BAR)
    st.header("2. Fashion Knowledge Level")
    st.plotly_chart(chart_bar_awareness(df_filtered), use_container_width=True)
    st.info("""
    **📝 Analysis:**
    * Most respondents (Level 3-4) are educated consumers who understand trends well.
    * Social media acts as a teacher, creating smart buyers who are selective about what they purchase.
    """)
    st.markdown("---")
    
    # 3. RANKING (BAR)
    st.header("3. Key Interest Drivers")
    st.plotly_chart(chart_bar_influence(df_filtered), use_container_width=True)
    st.info("""
    **📝 Analysis:**
    * Online Communities and Influencers are far more trusted than traditional Brand Ads.
    * Consumers rely on "Social Proof" (reviews from real people) rather than corporate marketing.
    """)
    st.markdown("---")
    
    # 4. FREQUENCY vs BUDGET (HEATMAP)
    st.header("4. Interest Intensity Matrix")
    st.plotly_chart(chart_heatmap_freq_budget(df_filtered), use_container_width=True)
    st.info("""
    **📝 Analysis:**
    * A "High Frequency, Low Budget" pattern indicates strong Fast Fashion behavior.
    * Consumers buy cheap items often to keep up with rapid trends instead of investing in expensive pieces.
    """)
    st.markdown("---")

    # 5. AWARENESS vs BUDGET (BUBBLE)
    st.header("5. Awareness vs. Spending Interest")
    st.plotly_chart(chart_bubble_awareness_budget(df_filtered), use_container_width=True)
    st.info("""
    **📝 Analysis:**
    * High awareness often links to low budgets, revealing the "Smart Shopper" effect.
    * Knowledgeable consumers use their skills to find cheaper alternatives rather than spending more.
    """)
    st.markdown("---")

    # 6. INFLUENCE vs FREQUENCY (STACKED BAR)
    st.header("6. Impact of Drivers on Intensity (Frequency)")
    st.plotly_chart(chart_stacked_influence_freq(df_filtered), use_container_width=True)
    st.info("""
    **📝 Analysis:**
    * Influencers drive the highest shopping frequency (Daily/Weekly) among all groups.
    * Constant content updates create a "Fear of Missing Out," triggering habitual browsing and buying.
    """)
    
    st.markdown("---")
    st.success("✅ **Consumer Interest Analysis Complete**")

if __name__ == "__main__":
    app()
