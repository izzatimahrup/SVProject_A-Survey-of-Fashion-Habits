import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="Section C: Consumer Interests", layout="wide")

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
    
    # --- FIX SUSUNAN SKALA (LIKERT / ORDINAL) ---
    
    # 1. BUDGET ORDER (Kecil ke Besar)
    budget_order_logic = ["<500", "500-1000", "1000-3000", ">3000"]
    found_budget = [x for x in budget_order_logic if x in df['Budget'].unique()]
    other_budget = [x for x in df['Budget'].unique() if x not in found_budget]
    final_budget = found_budget + other_budget
    # Convert to Categorical so Plotly respects the order
    df['Budget'] = pd.Categorical(df['Budget'], categories=final_budget, ordered=True)
    
    # 2. FREQUENCY ORDER (Kerap ke Jarang)
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

    # 3. AWARENESS (1 ke 5)
    df['Awareness_Str'] = df['Awareness'].astype(str)
    awareness_order = sorted(df['Awareness_Str'].unique().tolist())
    df['Awareness_Str'] = pd.Categorical(df['Awareness_Str'], categories=awareness_order, ordered=True)
    
    return df

# --- COLOR PALETTE (CONSISTENT) ---
# Modern Palette for Plotly
COLOR_SEQUENCE = px.colors.qualitative.Prism 

# --- 2. PLOTLY CHARTS FUNCTIONS ---

# 1. PIE CHART (Ganti Donut)
def chart_pie_budget(df):
    data = df['Budget'].value_counts().reset_index()
    data.columns = ['Budget', 'Count']
    
    fig = px.pie(data, values='Count', names='Budget', 
                 title="Distribution of Monthly Budget",
                 color_discrete_sequence=COLOR_SEQUENCE,
                 hole=0) # Hole=0 means Pie Chart (Full)
    
    # Feedback: Info mesti ada dalam chart, bukan tooltip je
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True)
    return fig

# 2. BAR CHART (Simple & Clean for Awareness)
def chart_bar_awareness(df):
    data = df['Awareness_Str'].value_counts().sort_index().reset_index()
    data.columns = ['Awareness', 'Count']
    
    fig = px.bar(data, x='Awareness', y='Count',
                 title="Self-Perceived Fashion Awareness Level",
                 labels={'Awareness': 'Awareness Level (1-5)', 'Count': 'Number of Respondents'},
                 color='Count', # Color gradient based on count
                 color_continuous_scale='Teal')
    
    fig.update_layout(xaxis_title="Awareness Level", yaxis_title="Total Count")
    return fig

# 3. BAR CHART (Influence Ranking)
def chart_bar_influence(df):
    data = df['Influence'].value_counts().reset_index()
    data.columns = ['Influence', 'Count']
    
    fig = px.bar(data, x='Influence', y='Count',
                 title="Top Influencing Factors Ranking",
                 labels={'Influence': 'Source of Influence', 'Count': 'Number of Respondents'},
                 color='Influence',
                 color_discrete_sequence=COLOR_SEQUENCE)
    
    fig.update_layout(xaxis_title="Influence Source", yaxis_title="Count", showlegend=False)
    return fig

# 4. HEATMAP (Frequency vs Budget)
def chart_heatmap_freq_budget(df):
    # Plotly Density Heatmap is perfect for this matrix
    fig = px.density_heatmap(df, x='Frequency', y='Budget',
                             title="Matrix: Frequency vs. Budget",
                             labels={'Frequency': 'Shopping Frequency', 'Budget': 'Monthly Budget'},
                             color_continuous_scale='OrRd') # Orange-Red scale
    return fig

# 5. BUBBLE CHART (Awareness vs Budget)
# Guna Bubble Chart supaya tak nampak "Weird" macam scatter plot biasa yang bertindih
def chart_bubble_awareness_budget(df):
    # Grouping data untuk dapatkan saiz bubble
    df_grouped = df.groupby(['Awareness_Str', 'Budget']).size().reset_index(name='Count')
    
    fig = px.scatter(df_grouped, x='Awareness_Str', y='Budget',
                     size='Count', # Saiz bubble ikut jumlah orang
                     color='Count',
                     title="Correlation: Awareness vs. Budget",
                     labels={'Awareness_Str': 'Fashion Awareness (1-5)', 'Budget': 'Budget Range'},
                     size_max=40,
                     color_continuous_scale='Viridis')
    
    fig.update_layout(xaxis_title="Awareness Level", yaxis_title="Budget Range")
    return fig

# 6. STACKED BAR (Influence vs Frequency)
def chart_stacked_influence_freq(df):
    # Prepare data specifically for stacked bar to ensure order is respected
    df_grouped = df.groupby(['Influence', 'Frequency']).size().reset_index(name='Count')
    
    fig = px.bar(df_grouped, x='Influence', y='Count', color='Frequency',
                 title="Impact of Influences on Shopping Frequency",
                 labels={'Influence': 'Influence Source', 'Count': 'Count', 'Frequency': 'Frequency'},
                 color_discrete_sequence=px.colors.qualitative.Safe) # Safe palette
    
    fig.update_layout(barmode='stack', xaxis_title="Influence Source", yaxis_title="Count")
    return fig

# 7. STACKED BAR (Influence vs Budget)
def chart_stacked_influence_budget(df):
    df_grouped = df.groupby(['Influence', 'Budget']).size().reset_index(name='Count')
    
    fig = px.bar(df_grouped, x='Influence', y='Count', color='Budget',
                 title="Does Influence Source Affect Spending Limits?",
                 labels={'Influence': 'Influence Source', 'Count': 'Count', 'Budget': 'Budget Range'},
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_layout(barmode='stack', xaxis_title="Influence Source", yaxis_title="Count")
    return fig

# --- 3. MAIN APP ---
def app():
    st.title("SECTION C : CONSUMER INTERESTS ABOUT FASHION")
    
    # --- OBJECTIVE ---
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 5px solid #264653; margin-bottom: 20px;">
        <h4 style="color: #264653; margin-top: 0;">Objective</h4>
        <p style="margin-bottom: 0; color: #333;">
            To analyze consumer interests in fashion by examining their spending habits, trend awareness, 
            and the key external drivers that influence their purchasing decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    if df.empty: return

    # --- FILTER ---
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

    # --- VISUALIZATION (PLOTLY) ---
    
    # 1. DISTRIBUTION (PIE CHART - FIXED)
    st.header("1. Spending Preferences")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        # Pie chart dengan label di dalam
        st.plotly_chart(chart_pie_budget(df_filtered), use_container_width=True)
        st.info("""
        **📝 Analysis:**
        * **A significant majority of respondents allocate a low monthly budget (under RM500) for fashion.**
        * **Trend:** This indicates that price sensitivity is a major factor, with a clear preference for affordable, value-for-money products over expensive luxury brands.
        """)
    st.markdown("---")
    
    # 2. AWARENESS LEVEL (BAR CHART)
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
    
    # 3. RANKING (BAR CHART)
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

    # 5. AWARENESS vs BUDGET (BUBBLE CHART)
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
