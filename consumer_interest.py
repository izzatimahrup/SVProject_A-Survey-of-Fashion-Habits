import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from math import pi
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper
from bokeh.palettes import Magma256, Spectral6
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

    # Rename columns for easier access
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
    
    # Cleaning Influence Column
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
    
    # Sorting Categorical Data (Penting untuk susunan graf)
    budget_order = ["<500", "500-1000", "1000-3000", ">3000"]
    df['Budget'] = pd.Categorical(df['Budget'], categories=budget_order, ordered=True)
    
    # Auto-sort frequency based on unique values found
    freq_sort_list = sorted(df['Frequency'].dropna().unique().tolist())
    df['Frequency'] = pd.Categorical(df['Frequency'], categories=freq_sort_list, ordered=True)

    df['Awareness_Str'] = df['Awareness'].astype(str)
    
    return df

# --- HELPER: RENDER BOKEH (SAIZ KEKAL: 400px / Balanced) ---
def render_bokeh(plot):
    plot.sizing_mode = "scale_width"
    
    # KEKALKAN SIZE INI (Jangan Ubah)
    plot.height = 400 
    
    # Margin Bawah Lebih Besar Supaya Label X Tak Putus
    plot.min_border_bottom = 80  
    plot.min_border_left = 60
    
    html = file_html(plot, CDN, "my plot")
    
    # Frame HTML set tinggi sikit dari graf (buffer)
    components.html(html, height=550, scrolling=False)

# --- PALETTE ---
INTEREST_PALETTE = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#8d99ae"]
STACKED_PALETTE = ["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600", "#488f31"]

# --- 2. BOKEH CHARTS FUNCTIONS (INTEREST FOCUS) ---

# CHART 1: DONUT CHART (Budget Preference)
def chart_donut_budget(df):
    data = df['Budget'].value_counts().reset_index(name='value')
    data.columns = ['Budget', 'value'] 
    
    total = data['value'].sum()
    data['angle'] = data['value'] / total * 2 * pi
    data['color'] = INTEREST_PALETTE[:len(data)]
    data['percentage'] = (data['value'] / total * 100).round(1).astype(str) + '%'
    
    source = ColumnDataSource(data)
    
    p = figure(title="Consumer Spending Preference (Budget)", 
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

# CHART 2: SCATTER PLOT (Awareness vs Budget) 
def chart_scatter_awareness_budget(df):
    source = ColumnDataSource(df)
    budget_factors = ["<500", "500-1000", "1000-3000", ">3000"]
    
    unique_freq = df['Frequency'].unique().tolist()
    # Pastikan palette cukup warna
    palette_use = STACKED_PALETTE if len(unique_freq) <= 6 else Magma256[:len(unique_freq)]
    color_mapper = CategoricalColorMapper(factors=unique_freq, palette=palette_use)
    
    p = figure(title="Fashion Awareness vs. Spending Preference", 
               x_range=["1", "2", "3", "4", "5"], y_range=budget_factors,
               tools="pan,wheel_zoom,reset,hover", active_scroll="wheel_zoom", 
               x_axis_label="Fashion Awareness Level (1-5)", y_axis_label="Monthly Budget Preference (RM)")
    
    p.scatter(x=jitter('Awareness_Str', width=0.6, range=p.x_range), 
              y=jitter('Budget', width=0.6, range=p.y_range), 
              size=14, source=source, color=transform('Frequency', color_mapper),
              fill_alpha=0.7, line_color="white", legend_field='Frequency')
    
    p.hover.tooltips = [("Awareness", "@Awareness"), ("Budget", "@Budget"), ("Freq", "@Frequency")]
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.legend.title = "Engagement (Frequency)"
    p.ygrid.grid_line_color = "#f0f0f0"
    return p

# CHART 3: BAR CHART (Interest Drivers)
def chart_bar_influence(df):
    counts = df['Influence'].value_counts()
    factors = counts.index.tolist()
    source = ColumnDataSource(data=dict(factors=factors, counts=counts, color=[INTEREST_PALETTE[1]]*len(factors)))
    
    p = figure(x_range=factors, title="Top Drivers of Consumer Interest", 
               toolbar_location=None, tools="hover", 
               x_axis_label="Source of Interest", y_axis_label="Number of Respondents")
    
    p.vbar(x='factors', top='counts', width=0.5, source=source, 
           line_color='white', fill_color='color', alpha=0.9)
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 0 
    p.hover.tooltips = [("Driver", "@factors"), ("Count", "@counts")]
    return p

# CHART 4: HEATMAP (Intensity vs Budget)
def chart_heatmap_freq_budget(df):
    df_group = df.groupby(['Frequency', 'Budget']).size().reset_index(name='counts')
    max_count = df_group['counts'].max()
    df_group['bubble_size'] = (df_group['counts'] / max_count) * 45 + 5
    
    source = ColumnDataSource(df_group)
    freq_factors = sorted(df['Frequency'].unique().tolist())
    budget_factors = ["<500", "500-1000", "1000-3000", ">3000"]
    
    p = figure(title="Interest Intensity Matrix: Frequency vs. Budget", 
               x_range=freq_factors, y_range=budget_factors,
               tools="hover", toolbar_location=None,
               x_axis_label="Interest Intensity (Shopping Frequency)", y_axis_label="Budget Preference")
    
    p.scatter(x="Frequency", y="Budget", size='bubble_size', 
              source=source, color="#e76f51", fill_alpha=0.8, line_color="#c0392b")
    
    p.grid.grid_line_color = "#e5e5e5"
    p.xaxis.major_label_orientation = 0.2
    p.hover.tooltips = [("Frequency", "@Frequency"), ("Budget", "@Budget"), ("Count", "@counts")]
    return p

# CHART 5: STACKED BAR (Drivers vs Intensity)
def chart_stacked_influence_freq(df):
    cross_tab = pd.crosstab(df['Influence'], df['Frequency'])
    factors = cross_tab.index.tolist()
    freq_cols = cross_tab.columns.tolist()
    
    palette_use = STACKED_PALETTE if len(freq_cols) <= 6 else Magma256[:len(freq_cols)]
    
    source = ColumnDataSource(data=cross_tab)
    
    p = figure(x_range=factors, title="Impact of Influences on Interest Intensity",
               toolbar_location=None, tools="hover", tooltips="$name: @$name",
               x_axis_label="Interest Driver (Influence)", y_axis_label="Count of Respondents")
    
    p.vbar_stack(freq_cols, x='Influence', width=0.5, color=palette_use, source=source, legend_label=freq_cols)
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.title = "Frequency"
    return p

# CHART 6: LOLLIPOP CHART (Awareness)
def chart_lollipop_awareness(df):
    data = df['Awareness_Str'].value_counts().sort_index().reset_index(name='counts')
    data.columns = ['Awareness', 'counts'] 
    data = data.sort_values(by='Awareness')
    
    source = ColumnDataSource(data)
    p = figure(x_range=data['Awareness'].tolist(), title="Self-Perceived Fashion Awareness",
               toolbar_location=None, 
               x_axis_label="Awareness Level (1 = Low Interest, 5 = High Interest)", y_axis_label="Total Count")
    
    p.segment(x0='Awareness', y0=0, x1='Awareness', y1='counts', source=source, 
              line_width=5, line_color="#4a4a4a")
    p.scatter(x='Awareness', y='counts', size=25, source=source, 
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
            To analyze consumer <b>interests and preferences</b> in fashion, focusing on spending tendencies, 
            trend awareness, and the key external drivers that spark their interest, independent of demographic factors.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    if df.empty: return

    # --- FILTER (SCOPE KAJIAN) ---
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

    # --- VISUALIZATION (UI BALANCED [1, 5, 1]) ---
    
    # 1. DISTRIBUTION (Budget Preference)
    st.header("1. Spending Preferences")
    st.caption("Overview of consumer willingness to spend on fashion.")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        render_bokeh(chart_donut_budget(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Preference:** The majority of consumers prefer a **Budget-Friendly (<RM500)** approach to fashion.
        * **Interest Level:** Only a small segment shows interest in high-end spending (>RM3000), indicating a price-conscious market interest.
        """)
    st.markdown("---")
    
    # 2. AWARENESS vs BUDGET
    st.header("2. Awareness vs. Spending Interest")
    st.caption("Does knowing more about fashion trends increase the interest to spend?")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_scatter_awareness_budget(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Pattern:** High fashion awareness (Level 4-5) does not automatically translate to high spending interest.
        * **Insight:** Consumers are interested in trends but prefer to access them at a lower cost (Smart Shopping interest).
        """)
    st.markdown("---")
    
    # 3. RANKING (Influence/Drivers)
    st.header("3. Key Interest Drivers")
    st.caption("What sparks the consumer's interest to shop?")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_bar_influence(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Top Driver:** **Online Community** and **Influencers** are the primary sources that ignite consumer interest.
        * **Trust:** Traditional ads have lower impact; interest is driven more by social proof and peer validation.
        """)
    st.markdown("---")
    
    # 4. FREQUENCY vs BUDGET (Intensity)
    st.header("4. Interest Intensity Matrix")
    st.caption("Analyzing the relationship between Shopping Frequency (Intensity) and Budget.")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_heatmap_freq_budget(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **High Intensity, Low Budget:** A strong cluster shows consumers with high interest (shopping frequently) but keeping to a low budget.
        * **Preference:** This indicates a preference for fast-fashion consumption—buying affordable items often.
        """)
    st.markdown("---")

    # 5. INFLUENCE vs FREQUENCY
    st.header("5. Impact of Drivers on Intensity")
    st.caption("Which driver sustains the most consistent shopping interest?")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_stacked_influence_freq(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Digital Impact:** Consumers driven by 'Influencers' show higher shopping intensity (Frequency) compared to family-driven consumers.
        * **Engagement:** Social media acts as a constant trigger, keeping consumer interest active and continuous.
        """)
    st.markdown("---")

    # 6. AWARENESS
    st.header("6. Fashion Knowledge Level")
    st.caption("Self-perceived level of fashion trend awareness.")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_lollipop_awareness(df_filtered))
        st.info("""
        **📝 Interpretation & Analysis:**
        * **Trend:** The market shows a **Moderate-to-High** interest in keeping up with trends.
        * **Conclusion:** Consumers are interested and knowledgeable, meaning they value style/aesthetics even if their budget is limited.
        """)

    st.markdown("---")
    st.success("✅ **Consumer Interest Analysis Complete**")

if __name__ == "__main__":
    app()
