import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="Section C: Consumer Interests", layout="wide")

# --- CSS TWEAKS: METRIC STYLING ---
# Making the metric numbers bigger and allowing text to wrap
st.markdown("""
<style>
/* Target the value text in st.metric */
[data-testid="stMetricValue"] {
    font-size: 28px !important; /* Make it big */
    word-wrap: break-word !important; /* Allow long words to break */
    white-space: normal !important; /* Allow text to wrap to next line */
    line-height: 1.1 !important; /* Tighten line height */
    height: auto !important; /* Adjust height automatically */
}

/* Target the label (small title) to look neat */
[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    width: 100% !important;
    white-space: normal !important;
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
        st.error("Error: 'Cleaned_FashionHabitGF.csv' was not found.")
        return pd.DataFrame()

    # Rename columns to make them easier to code with
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
    
    # Clean up the 'Influence' column to group similar answers
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
    
    # --- ORDERING CATEGORIES ---
    # Fix Budget order manually so it doesn't show up alphabetically
    budget_order_logic = ["<500", "500-1000", "1000-3000", ">3000"]
    # Find which ones actually exist in the data
    found_budget = [x for x in budget_order_logic if x in df['Budget'].unique()]
    # Add any others that might be in the data but not in my list
    other_budget = [x for x in df['Budget'].unique() if x not in found_budget]
    final_budget = found_budget + other_budget
    df['Budget'] = pd.Categorical(df['Budget'], categories=final_budget, ordered=True)
    
    # Fix Frequency order
    freq_order_logic = [
        "Daily", "Every day", "Everyday", 
        "Weekly", "Once a week", "Every week",
        "Monthly", "Once a month", "Every month",
        "Every 2-3 months", "Quarterly",
        "Every 6 months", "Twice a year",
        "Annually", "Once a year", "Yearly",
        "Rarely", "Never"
    ]
    found_freq = [x for x in freq_order_logic if x in df['Frequency'].unique()]
    other_freq = [x for x in df['Frequency'].unique() if x not in found_freq]
    final_freq = found_freq + other_freq
    
    # Fallback if list is empty
    if not final_freq: final_freq = sorted(df['Frequency'].dropna().unique().tolist())
    df['Frequency'] = pd.Categorical(df['Frequency'], categories=final_freq, ordered=True)

    # Fix Awareness order (ensure it treats numbers as categorical)
    df['Awareness_Str'] = df['Awareness'].astype(str)
    awareness_order = sorted(df['Awareness_Str'].unique().tolist())
    df['Awareness_Str'] = pd.Categorical(df['Awareness_Str'], categories=awareness_order, ordered=True)
    
    return df

# --- MASTER COLOR PALETTE ---
# Using a consistent color scheme for professionalism
CONSISTENT_COLORS = ["#003f5c", "#d62728", "#2ca02c", "#bcbd22", "#9467bd", "#17becf"]
CONSISTENT_SCALE = 'Blues'

# --- 2. PLOTLY CHART FUNCTIONS ---

def chart_pie_budget(df):
    data = df['Budget'].value_counts().reset_index()
    data.columns = ['Budget', 'Count']
    fig = px.pie(data, values='Count', names='Budget', title="Distribution of Monthly Budget",
                 color_discrete_sequence=CONSISTENT_COLORS, hole=0)
    # Put text inside to keep it clean
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
    fig.update_layout(showlegend=True)
    return fig

def chart_bar_awareness(df):
    data = df['Awareness_Str'].value_counts().sort_index().reset_index()
    data.columns = ['Awareness', 'Count']
    fig = px.bar(data, x='Awareness', y='Count', title="Self-Perceived Fashion Awareness Level",
                 labels={'Awareness': 'Awareness Level (1-5)', 'Count': 'Number of Respondents'},
                 color='Count', color_continuous_scale=CONSISTENT_SCALE)
    fig.update_layout(xaxis_title="Awareness Level", yaxis_title="Total Count")
    return fig

def chart_bar_influence(df):
    data = df['Influence'].value_counts().reset_index()
    data.columns = ['Influence', 'Count']
    fig = px.bar(data, x='Influence', y='Count', title="Top Influencing Factors Ranking",
                 labels={'Influence': 'Source of Influence', 'Count': 'Number of Respondents'},
                 color='Influence', color_discrete_sequence=CONSISTENT_COLORS)
    fig.update_layout(xaxis_title="Influence Source", yaxis_title="Count", showlegend=False)
    return fig

def chart_heatmap_freq_budget(df):
    fig = px.density_heatmap(df, x='Frequency', y='Budget', title="Matrix: Frequency vs. Budget",
                             labels={'Frequency': 'Shopping Frequency', 'Budget': 'Monthly Budget'},
                             color_continuous_scale=CONSISTENT_SCALE)
    return fig

def chart_bubble_awareness_budget(df):
    df_grouped = df.groupby(['Awareness_Str', 'Budget']).size().reset_index(name='Count')
    fig = px.scatter(df_grouped, x='Awareness_Str', y='Budget', size='Count', color='Count',
                     title="Correlation: Awareness vs. Budget",
                     labels={'Awareness_Str': 'Fashion Awareness (1-5)', 'Budget': 'Budget Range'},
                     size_max=50, color_continuous_scale=CONSISTENT_SCALE)
    fig.update_layout(xaxis_title="Awareness Level", yaxis_title="Budget Range")
    return fig

def chart_stacked_influence_freq(df):
    df_grouped = df.groupby(['Influence', 'Frequency']).size().reset_index(name='Count')
    fig = px.bar(df_grouped, x='Influence', y='Count', color='Frequency',
                 title="Impact of Influences on Shopping Frequency",
                 labels={'Influence': 'Influence Source', 'Count': 'Count', 'Frequency': 'Frequency'},
                 color_discrete_sequence=CONSISTENT_COLORS)
    fig.update_layout(barmode='stack', xaxis_title="Influence Source", yaxis_title="Count")
    return fig

# --- 3. MAIN APP LAYOUT ---
def app():
    st.title("SECTION C : CONSUMER INTERESTS ABOUT FASHION")
    
    # --- OBJECTIVE SECTION ---
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-left: 5px solid #003f5c; margin-bottom: 20px;">
        <h4 style="color: #003f5c; margin-top: 0;">Objective</h4>
        <p style="margin-bottom: 0; color: #333;">
            To analyze consumer interests in fashion by examining their spending habits, trend awareness, 
            and the key external drivers that influence their purchasing decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    if df.empty: return

    # --- 1. FILTERS (TOP SECTION) ---
    st.subheader("🔍 Filter Data Scope")
    f1, f2 = st.columns(2)
    with f1:
        region_options = df['Region'].unique().tolist()
        selected_regions = st.multiselect("Select Region (Scope):", region_options, default=region_options)
    with f2:
        gender_options = df['Gender'].unique().tolist()
        selected_genders = st.multiselect("Select Gender (Scope):", gender_options, default=gender_options)
    
    # Apply the filters
    df_filtered = df[(df['Region'].isin(selected_regions)) & (df['Gender'].isin(selected_genders))]
    st.caption(f"Showing analysis for **{len(df_filtered)}** respondents.")
    st.markdown("---")
    
    if df_filtered.empty:
        st.warning("⚠️ No data available. Please adjust your filters.")
        return

    # --- 2. SCORECARD METRICS ---
    st.subheader("📊 Key Consumer Interest Summary")
    
    # Calculate stats
    total_respondents = len(df_filtered)
    
    if not df_filtered.empty:
        top_budget = df_filtered['Budget'].mode()[0]
        top_influence = df_filtered['Influence'].mode()[0]
        # Calculate mean manually to avoid errors
        avg_awareness_val = pd.to_numeric(df_filtered['Awareness'], errors='coerce').mean()
        avg_awareness = f"{avg_awareness_val:.1f} / 5.0" if not pd.isna(avg_awareness_val) else "N/A"
    else:
        top_budget = "N/A"
        top_influence = "N/A"
        avg_awareness = "N/A"

    # Display metrics in 4 columns
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Respondents", f"{total_respondents}", help="Total number of respondents based on current filters.")
    m2.metric("Majority Budget", top_budget, help="The most common monthly budget range.")
    m3.metric("Top Influence", top_influence, help="The primary factor driving purchasing decisions.")
    m4.metric("Avg. Awareness", avg_awareness, help="Average self-perceived fashion knowledge (Scale 1-5).")
    
    st.markdown("---")

    # --- 3. VISUALIZATIONS (SECTION 1 to 6) ---
    
    # 1. DISTRIBUTION (PIE)
    st.header("1. Spending Preferences")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_pie_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **The Pie Chart shows that most respondents have a monthly budget under RM500.**
        * **Trend:** This confirms the market is highly price sensitive. Although young people love fashion content on social media, they lack spending power, so brands must prioritize products that offer good value.
        """)
    st.markdown("---")
    
    # 2. AWARENESS LEVEL (BAR)
    st.header("2. Fashion Knowledge Level")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_bar_awareness(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **Most people rated themselves at Level 3 and 4, indicating an educated audience.**
        * **Insight:** Social media acts as an educational tool, transforming casual users into knowledgeable fans. This implies brands are dealing with consumers who are smart and selective.
        """)
    st.markdown("---")
    
    # 3. RANKING (BAR)
    st.header("3. Key Interest Drivers")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_bar_influence(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **Online Communities and Influencers score much higher than Brand Ads.**
        * **Trend:** Modern consumers rely on Social Proof because they trust reviews from real people more than corporate messages. Traditional ads alone are no longer sufficient.
        """)
    st.markdown("---")
    
    # 4. FREQUENCY vs BUDGET (HEATMAP)
    st.header("4. Interest Intensity Matrix")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_heatmap_freq_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **A pattern of 'High Frequency, Low Budget' points to Fast Fashion behavior.**
        * **Pattern:** Driven by rapid trends, consumers feel pressured to buy cheap items frequently to stay relevant rather than investing in expensive pieces.
        """)
    st.markdown("---")

    # 5. AWARENESS vs BUDGET (BUBBLE)
    st.header("5. Awareness vs. Spending Interest")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_bubble_awareness_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **High fashion awareness often coincides with low budgets, identifying the Smart Shopper.**
        * **Insight:** High knowledge does not always mean high spending. These digital natives use their knowledge to find cheaper alternatives and sales to stay stylish on a budget.
        """)
    st.markdown("---")

    # 6. INFLUENCE vs FREQUENCY (STACKED BAR)
    st.header("6. Impact of Drivers on Intensity (Frequency)")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_stacked_influence_freq(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **Influencers drive frequent shopping, with followers shopping daily or weekly.**
        * **Link:** This is likely due to the Fear of Missing Out from constant updates, creating a habit of constant browsing and buying.
        """)
    
    st.markdown("---")
    st.success("✅ **Consumer Interest Analysis Complete**")

if __name__ == "__main__":
    app()
