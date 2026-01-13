import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="Section C: Consumer Interests", layout="wide")

# --- CSS FIX: BESARKAN TEXT & TURUN BAWAH ---
st.markdown("""
<style>
/* Sasarkan nilai nombor/teks dalam st.metric */
[data-testid="stMetricValue"] {
    font-size: 28px !important; /* Saiz besar (tapi muat 2 baris) */
    word-wrap: break-word !important; /* Turunkan perkataan panjang */
    white-space: normal !important; /* Benarkan text turun baris */
    line-height: 1.1 !important; /* Rapatkan sikit jarak baris atas-bawah */
    height: auto !important; /* Pastikan kotak tak potong tulisan */
}

/* Sasarkan label (tajuk kecil) supaya kemas */
[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    width: 100% !important;
    white-space: normal !important;
}
</style>
""", unsafe_allow_html=True)

# --- 1. DATA LOADING ---
@st.cache_data
def load_data():
    file_path = "Cleaned_FashionHabitGF.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("File 'Cleaned_FashionHabitGF.csv' not found.")
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
    
    # Cleaning Influence
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
    
    # --- FIX SUSUNAN SKALA ---
    budget_order_logic = ["<500", "500-1000", "1000-3000", ">3000"]
    found_budget = [x for x in budget_order_logic if x in df['Budget'].unique()]
    other_budget = [x for x in df['Budget'].unique() if x not in found_budget]
    final_budget = found_budget + other_budget
    df['Budget'] = pd.Categorical(df['Budget'], categories=final_budget, ordered=True)
    
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
    if not final_freq: final_freq = sorted(df['Frequency'].dropna().unique().tolist())
    df['Frequency'] = pd.Categorical(df['Frequency'], categories=final_freq, ordered=True)

    df['Awareness_Str'] = df['Awareness'].astype(str)
    awareness_order = sorted(df['Awareness_Str'].unique().tolist())
    df['Awareness_Str'] = pd.Categorical(df['Awareness_Str'], categories=awareness_order, ordered=True)
    
    return df

# --- MASTER COLOR PALETTE ---
CONSISTENT_COLORS = ["#003f5c", "#d62728", "#2ca02c", "#bcbd22", "#9467bd", "#17becf"]
CONSISTENT_SCALE = 'Blues'

# --- 2. PLOTLY CHARTS FUNCTIONS ---

def chart_pie_budget(df):
    data = df['Budget'].value_counts().reset_index()
    data.columns = ['Budget', 'Count']
    fig = px.pie(data, values='Count', names='Budget', title="Distribution of Monthly Budget",
                 color_discrete_sequence=CONSISTENT_COLORS, hole=0)
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

def chart_stacked_influence_budget(df):
    df_grouped = df.groupby(['Influence', 'Budget']).size().reset_index(name='Count')
    fig = px.bar(df_grouped, x='Influence', y='Count', color='Budget',
                 title="Does Influence Source Affect Spending Limits?",
                 labels={'Influence': 'Influence Source', 'Count': 'Count', 'Budget': 'Budget Range'},
                 color_discrete_sequence=CONSISTENT_COLORS)
    fig.update_layout(barmode='stack', xaxis_title="Influence Source", yaxis_title="Count")
    return fig

# --- 3. MAIN APP ---
def app():
    st.title("SECTION C : CONSUMER INTERESTS ABOUT FASHION")
    
    # --- OBJEKTIF ---
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

    # --- 1. FILTER (DI ATAS) ---
    st.subheader("🔍 Filter Data Scope")
    f1, f2 = st.columns(2)
    with f1:
        region_options = df['Region'].unique().tolist()
        selected_regions = st.multiselect("Select Region (Scope):", region_options, default=region_options)
    with f2:
        gender_options = df['Gender'].unique().tolist()
        selected_genders = st.multiselect("Select Gender (Scope):", gender_options, default=gender_options)
    
    # Proses Filter
    df_filtered = df[(df['Region'].isin(selected_regions)) & (df['Gender'].isin(selected_genders))]
    st.caption(f"Showing analysis for **{len(df_filtered)}** respondents.")
    st.markdown("---")
    
    if df_filtered.empty:
        st.warning("⚠️ No data available.")
        return

    # --- 2. SCORECARD METRICS (DI BAWAH FILTER) ---
    st.subheader("📊 Key Consumer Interest Summary")
    
    # Kira Data
    total_respondents = len(df_filtered)
    
    if not df_filtered.empty:
        top_budget = df_filtered['Budget'].mode()[0]
        top_influence = df_filtered['Influence'].mode()[0]
        avg_awareness_val = pd.to_numeric(df_filtered['Awareness'], errors='coerce').mean()
        avg_awareness = f"{avg_awareness_val:.1f} / 5.0" if not pd.isna(avg_awareness_val) else "N/A"
    else:
        top_budget = "N/A"
        top_influence = "N/A"
        avg_awareness = "N/A"

    # Papar Kad
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Respondents", f"{total_respondents}", help="Total number of respondents based on current filters.")
    m2.metric("Majority Budget", top_budget, help="The most common monthly budget range selected by respondents.")
    m3.metric("Top Influence", top_influence, help="The primary factor driving purchasing decisions.")
    m4.metric("Avg. Awareness", avg_awareness, help="Average self-perceived fashion knowledge level (Scale 1-5).")
    
    st.markdown("---")

    # --- 3. VISUALIZATION (GRAF DI BAWAH) ---
    
    # 1. DISTRIBUTION (PIE)
    st.header("1. Spending Preferences")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_pie_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **A significant majority of respondents allocate a low monthly budget (under RM500) for fashion.**
        * **Trend:** This indicates that price sensitivity is a major factor, with a clear preference for affordable, value-for-money products over expensive luxury brands.
        """)
    st.markdown("---")
    
    # 2. AWARENESS LEVEL (BAR)
    st.header("2. Fashion Knowledge Level")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_bar_awareness(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **Most respondents rate their fashion knowledge at levels 3 or 4, showing they are quite updated with current trends.**
        * **Insight:** This suggests that despite having limited budgets, they still care deeply about maintaining a stylish image and staying relevant.
        """)
    st.markdown("---")
    
    # 3. RANKING (BAR)
    st.header("3. Key Interest Drivers")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_bar_influence(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **Online Communities and Social Media Influencers rank as the top drivers of interest, far surpassing traditional advertisements.**
        * **Trend:** This confirms that modern consumers trust social proof and peer reviews more than direct marketing from brands.
        """)
    st.markdown("---")
    
    # 4. FREQUENCY vs BUDGET (HEATMAP)
    st.header("4. Interest Intensity Matrix")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_heatmap_freq_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **A strong pattern emerges where consumers shop frequently (weekly or monthly) but maintain a low budget.**
        * **Pattern:** This points towards a 'Fast Fashion' behavior, where the interest lies in buying affordable items often to constantly refresh their wardrobe.
        """)
    st.markdown("---")

    # 5. AWARENESS vs BUDGET (BUBBLE)
    st.header("5. Awareness vs. Spending Interest")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_bubble_awareness_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **Interestingly, high fashion awareness (Level 5) does not strictly correlate with high spending.**
        * **Insight:** This suggests that knowledgeable consumers are 'smart shoppers' who use their trend awareness to find cheaper alternatives or sales rather than overspending.
        """)
    st.markdown("---")

    # 6. INFLUENCE vs FREQUENCY (STACKED BAR)
    st.header("6. Impact of Drivers on Intensity (Frequency)")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_stacked_influence_freq(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **Respondents influenced by Influencers tend to shop more frequently compared to those relying on family advice.**
        * **Link:** This is likely because social media feeds constantly expose them to new trends, triggering a continuous desire to buy and stay updated.
        """)
    st.markdown("---")

    # 7. INFLUENCE vs BUDGET (STACKED BAR)
    st.header("7. Impact of Drivers on Spending Power")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        st.plotly_chart(chart_stacked_influence_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **While advice from Family and Friends usually leads to conservative spending, high-value purchases (>RM1000) are often driven by external media.**
        * **Insight:** This suggests that stronger visual persuasion from Ads or Influencers is needed to justify larger financial commitments.
        """)

    st.markdown("---")
    st.success("✅ **Consumer Interest Analysis Complete**")

if __name__ == "__main__":
    app()
