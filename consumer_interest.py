import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from math import pi
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper
from bokeh.palettes import Magma256
from bokeh.transform import transform, cumsum, jitter
from bokeh.embed import file_html
from bokeh.resources import CDN

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
    
    budget_order = ["<500", "500-1000", "1000-3000", ">3000"]
    df['Budget'] = pd.Categorical(df['Budget'], categories=budget_order, ordered=True)
    df['Awareness_Str'] = df['Awareness'].astype(str)
    df['Job'] = df['Job'].apply(lambda x: x.split('(')[0].strip() if isinstance(x, str) else x)

    return df

# --- HELPER: RENDER BOKEH (HEIGHT 450) ---
def render_bokeh(plot):
    plot.sizing_mode = "scale_width"
    
    # 1. SET TINGGI 450 (Lebih Besar & Jelas)
    plot.height = 450 
    
    # 2. MARGIN UNTUK LABEL
    plot.min_border_bottom = 80  
    plot.min_border_left = 60
    
    html = file_html(plot, CDN, "my plot")
    
    # 3. FRAME HTML 600 (450 + 150 buffer selamat)
    components.html(html, height=600, scrolling=False)

# --- PALETTE ---
PRO_PALETTE = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#8d99ae"]
GENDER_PALETTE = ["#1f77b4", "#d62728"] 

# --- 2. BOKEH CHARTS FUNCTIONS ---

# CHART 1: DONUT CHART
def chart_donut_budget(df):
    data = df['Budget'].value_counts().reset_index(name='value')
    data.columns = ['Budget', 'value'] 
    
    total = data['value'].sum()
    data['angle'] = data['value'] / total * 2 * pi
    data['color'] = PRO_PALETTE[:len(data)]
    data['percentage'] = (data['value'] / total * 100).round(1).astype(str) + '%'
    
    source = ColumnDataSource(data)
    
    p = figure(title="Monthly Budget Distribution", 
               toolbar_location=None, tools="hover", 
               tooltips="@Budget: @value respondents (@percentage)", 
               x_range=(-0.5, 2.0)) 

    p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), 
            end_angle=cumsum('angle'), line_color="white", fill_color='color', 
            legend_field='Budget', source=source)
    
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.legend.title = "Budget Range (RM)"
    p.legend.location = "center_right"
    p.legend.border_line_color = "#e0e0e0"
    return p

# CHART 2: SCATTER PLOT
def chart_scatter_age_budget(df):
    source = ColumnDataSource(df)
    color_mapper = CategoricalColorMapper(factors=df['Gender'].unique().tolist(), palette=GENDER_PALETTE)
    budget_factors = ["<500", "500-1000", "1000-3000", ">3000"]
    
    p = figure(title="Correlation: Age vs. Budget", 
               x_range=sorted(df['Age'].unique().tolist()), y_range=budget_factors,
               tools="pan,wheel_zoom,reset,hover", active_scroll="wheel_zoom", 
               x_axis_label="Age Group (Years)", y_axis_label="Monthly Budget (RM)")
    
    p.scatter(x=jitter('Age', width=0.6, range=p.x_range), 
              y=jitter('Budget', width=0.6, range=p.y_range), 
              size=12, source=source, color=transform('Gender', color_mapper),
              fill_alpha=0.6, line_color="white", legend_field='Gender')
    
    p.hover.tooltips = [("Age", "@Age"), ("Budget", "@Budget"), ("Job", "@Job")]
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.ygrid.grid_line_color = "#f0f0f0"
    return p

# CHART 3: BAR CHART
def chart_bar_influence(df):
    counts = df['Influence'].value_counts()
    factors = counts.index.tolist()
    source = ColumnDataSource(data=dict(factors=factors, counts=counts, color=[PRO_PALETTE[1]]*len(factors)))
    
    p = figure(x_range=factors, title="Top Influencing Factors Ranking", 
               toolbar_location=None, tools="hover", 
               x_axis_label="Influence Source", y_axis_label="Number of Respondents")
    
    p.vbar(x='factors', top='counts', width=0.5, source=source, 
           line_color='white', fill_color='color', alpha=0.9)
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 0 
    p.hover.tooltips = [("Factor", "@factors"), ("Count", "@counts")]
    return p

# CHART 4: HEATMAP
def chart_heatmap_job_budget(df):
    df_group = df.groupby(['Job', 'Budget']).size().reset_index(name='counts')
    max_count = df_group['counts'].max()
    df_group['bubble_size'] = (df_group['counts'] / max_count) * 40 + 5 # Besar sikit bubble
    
    source = ColumnDataSource(df_group)
    job_factors = sorted(df['Job'].unique().tolist())
    budget_factors = ["<500", "500-1000", "1000-3000", ">3000"]
    
    p = figure(title="Employment Status vs. Monthly Budget", 
               x_range=job_factors, y_range=budget_factors,
               tools="hover", toolbar_location=None,
               x_axis_label="Employment Status", y_axis_label="Monthly Budget Range")
    
    p.scatter(x="Job", y="Budget", size='bubble_size', 
              source=source, color="#e76f51", fill_alpha=0.7, line_color="#c0392b")
    
    p.grid.grid_line_color = "#e5e5e5"
    p.xaxis.major_label_orientation = 0.3
    p.hover.tooltips = [("Status", "@Job"), ("Budget", "@Budget"), ("Count", "@counts")]
    return p

# CHART 5: STACKED BAR
def chart_stacked_gender_influence(df):
    cross_tab = pd.crosstab(df['Influence'], df['Gender'])
    factors = cross_tab.index.tolist()
    genders = cross_tab.columns.tolist() 
    source = ColumnDataSource(data=cross_tab)
    
    p = figure(x_range=factors, title="Comparison: Influence by Gender",
               toolbar_location=None, tools="hover", tooltips="$name: @$name",
               x_axis_label="Influence Source", y_axis_label="Count of Respondents")
    
    p.vbar_stack(genders, x='Influence', width=0.5, color=GENDER_PALETTE, source=source, legend_label=genders)
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.title = "Gender"
    return p

# CHART 6: LOLLIPOP CHART
def chart_lollipop_awareness(df):
    data = df['Awareness_Str'].value_counts().sort_index().reset_index(name='counts')
    data.columns = ['Awareness', 'counts'] 
    data = data.sort_values(by='Awareness')
    
    source = ColumnDataSource(data)
    p = figure(x_range=data['Awareness'].tolist(), title="Fashion Awareness Level",
               toolbar_location=None, 
               x_axis_label="Awareness Rating (1 = Low, 5 = High)", y_axis_label="Total Count")
    
    p.segment(x0='Awareness', y0=0, x1='Awareness', y1='counts', source=source, 
              line_width=4, line_color="#4a4a4a")
    p.scatter(x='Awareness', y='counts', size=22, source=source, 
              fill_color="#2a9d8f", line_color="white", line_width=2)
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.add_tools(HoverTool(tooltips=[("Rating", "@Awareness"), ("Count", "@counts")]))
    return p

# --- 3. MAIN APP ---
def app():
    st.title("SECTION C : CONSUMER INTERESTS ABOUT FASHION")
    
    # --- OBJECTIVE ---
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 5px solid #264653; margin-bottom: 20px;">
        <h4 style="color: #264653; margin-top: 0;">Objective</h4>
        <p style="margin-bottom: 0; color: #333;">
            To analyze the relationship between consumer demographics and spending habits while identifying the 
            key external factors influencing fashion purchasing decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    if df.empty: return

    # --- FILTER ---
    st.subheader("🔍 Data Filter Options")
    f1, f2 = st.columns(2)
    
    with f1:
        region_options = df['Region'].unique().tolist()
        selected_regions = st.multiselect("Select Region:", region_options, default=region_options)
        
    with f2:
        gender_options = df['Gender'].unique().tolist()
        selected_genders = st.multiselect("Select Gender:", gender_options, default=gender_options)
    
    df_filtered = df[(df['Region'].isin(selected_regions)) & (df['Gender'].isin(selected_genders))]
    
    st.caption(f"Showing analysis for **{len(df_filtered)}** respondents based on your selection.")
    st.markdown("---")
    
    if df_filtered.empty:
        st.warning("⚠️ No data available. Please adjust filters.")
        return

    # --- VISUALIZATION + ANALYSIS (HEIGHT 450) ---
    
    # 1. DISTRIBUTION
    st.header("1. Distribution Analysis")
    st.caption("Overview of budget allocation among respondents.")
    c1, c2, c3 = st.columns([1, 2, 1]) 
    with c2:
        render_bokeh(chart_donut_budget(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Pattern:** Majority of respondents fall into the **<RM500 (Low Budget)** category.
        * **Trend:** High spending power (>RM3000) is a minority, indicating a price-sensitive consumer base.
        """)
    st.markdown("---")
    
    # 2. CORRELATION
    st.header("2. Correlation Analysis")
    st.caption("Examining relationships between demographics and spending.")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        render_bokeh(chart_scatter_age_budget(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Correlation:** No clear linear correlation between **Age** and **Budget** (Older age does not guarantee higher budget).
        * **Anomaly:** Several young respondents (20-25 years old) show unusually high budgets, likely due to family support.
        """)
    st.markdown("---")
    
    # 3. RANKING
    st.header("3. Ranking Analysis")
    st.caption("Identifying key drivers of consumer decisions.")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        render_bokeh(chart_bar_influence(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Trend:** **Online Community** and **Influencers** are the top ranking factors, surpassing traditional "Friends".
        * **Insight:** Digital marketing has a stronger impact on this demographic than direct word-of-mouth.
        """)
    st.markdown("---")
    
    # 4. PATTERN RECOGNITION
    st.header("4. Pattern Recognition")
    st.caption("Employment status density against spending brackets.")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        render_bokeh(chart_heatmap_job_budget(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Pattern:** **Students** are heavily clustered in the <RM500 budget range.
        * **Insight:** Employment status is a stronger predictor of purchasing power compared to age or gender.
        """)
    st.markdown("---")

    # 5. COMPARISON
    st.header("5. Comparison Analysis")
    st.caption("Contrasting behavior between gender groups.")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        render_bokeh(chart_stacked_gender_influence(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Comparison:** Female respondents show a higher tendency for **Self-Decision**, while males are slightly more influenced by **Ads**.
        * **Pattern:** Both genders show significant reliance on social media (Influencers/Community).
        """)
    st.markdown("---")

    # 6. TRENDS
    st.header("6. Trend Analysis")
    st.caption("Self-perceived fashion awareness levels.")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        render_bokeh(chart_lollipop_awareness(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Trend:** The data is skewed towards **Moderate to High (3-4)** awareness levels.
        * **Insight:** Despite low budgets, the respondents are highly conscious of fashion trends.
        """)

    st.markdown("---")
    st.success("✅ **Analysis Complete:** All charts rendered based on filtered parameters.")

if __name__ == "__main__":
    app()
