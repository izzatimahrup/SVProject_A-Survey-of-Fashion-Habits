import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from math import pi
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper, Legend
from bokeh.palettes import Magma256, Spectral6, Viridis256, Turbo256
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
    df['Budget'] = pd.Categorical(df['Budget'], categories=final_budget, ordered=True)
    
    # 2. FREQUENCY ORDER (Kerap ke Jarang - Ikut Standard Google Form)
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
    
    if not final_freq:
        final_freq = sorted(df['Frequency'].dropna().unique().tolist())
        
    df['Frequency'] = pd.Categorical(df['Frequency'], categories=final_freq, ordered=True)

    # 3. AWARENESS (1 ke 5)
    df['Awareness_Str'] = df['Awareness'].astype(str)
    awareness_order = sorted(df['Awareness_Str'].unique().tolist())
    df['Awareness_Str'] = pd.Categorical(df['Awareness_Str'], categories=awareness_order, ordered=True)
    
    return df

# --- HELPER: RENDER BOKEH ---
def render_bokeh(plot):
    plot.sizing_mode = "scale_width"
    plot.height = 400 
    plot.min_border_bottom = 80  
    plot.min_border_left = 60
    html = file_html(plot, CDN, "my plot")
    components.html(html, height=550, scrolling=False)

# --- PALETTES ---
PALETTE_MAIN = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#8d99ae"]
PALETTE_STACK_1 = ["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"]
PALETTE_STACK_2 = ["#004c6d", "#0083a6", "#00c0d8", "#00ffff", "#73ffff"]

# --- 2. BOKEH CHARTS FUNCTIONS ---

# 1. DONUT CHART
def chart_donut_budget(df):
    data = df['Budget'].value_counts().reset_index(name='value')
    data.columns = ['Budget', 'value'] 
    
    total = data['value'].sum()
    data['angle'] = data['value'] / total * 2 * pi
    data['color'] = PALETTE_MAIN[:len(data)]
    data['percentage'] = (data['value'] / total * 100).round(1).astype(str) + '%'
    
    source = ColumnDataSource(data)
    p = figure(title="Distribution of Monthly Budget", 
               toolbar_location=None, tools="hover", 
               tooltips="@Budget: @value respondents (@percentage)", 
               x_range=(-0.5, 2.0)) 
    p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), 
            end_angle=cumsum('angle'), line_color="white", fill_color='color', 
            legend_field='Budget', source=source)
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.legend.title = "Budget (RM)"
    p.legend.location = "center_right"
    return p

# 2. LOLLIPOP CHART (Awareness)
def chart_lollipop_awareness(df):
    data = df['Awareness_Str'].value_counts().sort_index().reset_index(name='counts')
    data.columns = ['Awareness', 'counts'] 
    data = data.sort_values(by='Awareness')
    
    source = ColumnDataSource(data)
    p = figure(x_range=data['Awareness'].tolist(), title="Self-Perceived Fashion Awareness Level",
               toolbar_location=None, 
               x_axis_label="Likert Scale (1 = Low, 5 = High)", y_axis_label="Total Count")
    p.segment(x0='Awareness', y0=0, x1='Awareness', y1='counts', source=source, 
              line_width=5, line_color="#4a4a4a")
    p.scatter(x='Awareness', y='counts', size=25, source=source, 
              fill_color="#2a9d8f", line_color="white", line_width=2)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.add_tools(HoverTool(tooltips=[("Level", "@Awareness"), ("Count", "@counts")]))
    return p

# 3. BAR CHART (Influence)
def chart_bar_influence(df):
    counts = df['Influence'].value_counts()
    factors = counts.index.tolist()
    source = ColumnDataSource(data=dict(factors=factors, counts=counts, color=[PALETTE_MAIN[1]]*len(factors)))
    
    p = figure(x_range=factors, title="Top Influencing Factors Ranking", 
               toolbar_location=None, tools="hover", 
               x_axis_label="Influence Source", y_axis_label="Number of Respondents")
    p.vbar(x='factors', top='counts', width=0.5, source=source, 
           line_color='white', fill_color='color', alpha=0.9)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 0 
    p.hover.tooltips = [("Driver", "@factors"), ("Count", "@counts")]
    return p

# 4. HEATMAP (Frequency vs Budget)
def chart_heatmap_freq_budget(df):
    df_group = df.groupby(['Frequency', 'Budget']).size().reset_index(name='counts')
    max_count = df_group['counts'].max()
    df_group['bubble_size'] = (df_group['counts'] / max_count) * 45 + 5
    
    source = ColumnDataSource(df_group)
    freq_factors = df['Frequency'].cat.categories.tolist()
    budget_factors = df['Budget'].cat.categories.tolist()
    
    p = figure(title="Matrix: Frequency vs. Budget", 
               x_range=freq_factors, y_range=budget_factors,
               tools="hover", toolbar_location=None,
               x_axis_label="Shopping Frequency", y_axis_label="Monthly Budget")
    p.scatter(x="Frequency", y="Budget", size='bubble_size', 
              source=source, color="#e76f51", fill_alpha=0.8, line_color="#c0392b")
    p.grid.grid_line_color = "#e5e5e5"
    p.xaxis.major_label_orientation = 0.2
    p.hover.tooltips = [("Freq", "@Frequency"), ("Budget", "@Budget"), ("Count", "@counts")]
    return p

# 5. SCATTER (Awareness vs Budget)
def chart_scatter_awareness_budget(df):
    source = ColumnDataSource(df)
    budget_factors = df['Budget'].cat.categories.tolist()
    
    unique_freq = df['Frequency'].unique().tolist()
    if len(unique_freq) <= len(PALETTE_STACK_1):
        palette_use = PALETTE_STACK_1[:len(unique_freq)]
    else:
        palette_use = Magma256[:len(unique_freq)]
        
    color_mapper = CategoricalColorMapper(factors=unique_freq, palette=palette_use)
    
    p = figure(title="Correlation: Awareness vs. Budget", 
               x_range=["1", "2", "3", "4", "5"], y_range=budget_factors,
               tools="pan,wheel_zoom,reset,hover", active_scroll="wheel_zoom", 
               x_axis_label="Fashion Awareness (1-5)", y_axis_label="Budget Range")
    p.scatter(x=jitter('Awareness_Str', width=0.6, range=p.x_range), 
              y=jitter('Budget', width=0.6, range=p.y_range), 
              size=14, source=source, color=transform('Frequency', color_mapper),
              fill_alpha=0.7, line_color="white", legend_field='Frequency')
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.hover.tooltips = [("Awareness", "@Awareness"), ("Budget", "@Budget"), ("Freq", "@Frequency")]
    return p

# 6. STACKED BAR (Influence vs Frequency)
def chart_stacked_influence_freq(df):
    cross_tab = pd.crosstab(df['Influence'], df['Frequency'])
    factors = cross_tab.index.tolist()
    freq_cols = list(cross_tab.columns)
    
    if len(freq_cols) <= len(PALETTE_STACK_1):
        palette_use = PALETTE_STACK_1[:len(freq_cols)]
    else:
        palette_use = Turbo256[:len(freq_cols)]
    
    source = ColumnDataSource(data=cross_tab)
    p = figure(x_range=factors, title="Impact of Influences on Shopping Frequency",
               toolbar_location=None, tools="hover", tooltips="$name: @$name",
               x_axis_label="Influence Source", y_axis_label="Count of Respondents")
    p.vbar_stack(freq_cols, x='Influence', width=0.5, color=palette_use, source=source, legend_label=freq_cols)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.title = "Frequency"
    return p

# 7. STACKED BAR (Influence vs Budget)
def chart_stacked_influence_budget(df):
    cross_tab = pd.crosstab(df['Influence'], df['Budget'])
    factors = cross_tab.index.tolist()
    budget_cols = list(cross_tab.columns)
    
    if len(budget_cols) <= len(PALETTE_STACK_2):
        palette_use = PALETTE_STACK_2[:len(budget_cols)]
    else:
        palette_use = Viridis256[:len(budget_cols)]

    source = ColumnDataSource(data=cross_tab)
    p = figure(x_range=factors, title="Does Influence Source Affect Spending Limits?",
               toolbar_location=None, tools="hover", tooltips="$name: @$name",
               x_axis_label="Influence Source", y_axis_label="Count of Respondents")
    
    p.vbar_stack(budget_cols, x='Influence', width=0.5, color=palette_use, source=source, legend_label=budget_cols)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.title = "Budget"
    return p

# --- 3. MAIN APP ---
def app():
    st.title("SECTION C : CONSUMER INTERESTS ABOUT FASHION")
    
    # --- OBJECTIVE ---
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 5px solid #264653; margin-bottom: 20px;">
        <h4 style="color: #264653; margin-top: 0;">Objective</h4>
        <p style="margin-bottom: 0; color: #333;">
            To see what fashion consumers like, how much they spend, and what makes them want to buy products.
            We want to understand their shopping habits and interests.
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

    # --- VISUALIZATION (7 CHARTS) ---
    
    # 1. DISTRIBUTION
    st.header("1. Spending Preferences")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        render_bokeh(chart_donut_budget(df_filtered))
        st.info("""
        **📝 Analysis:**
        * **Most people have a low budget (under RM500).** This shows that price is very important. 
        * **Trend:** People want fashion that is cheap and affordable, not expensive luxury brands.
        """)
    st.markdown("---")
    
    # 2. AWARENESS LEVEL
    st.header("2. Fashion Knowledge Level")
    c1, c2, c3 = st.columns([1, 5, 1]) 
    with c2:
        render_bokeh(chart_lollipop_awareness(df_filtered))
        st.info("""
        **📝 Analysis:**
        * **Most people rate themselves 3 or 4 out of 5.** This means they know about current fashion trends.
        * **Insight:** Even if they don't have much money, they still care about looking stylish and modern.
        """)
    st.markdown("---")
    
    # 3. RANKING
    st.header("3. Key Interest Drivers")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_bar_influence(df_filtered))
        st.info("""
        **📝 Analysis:**
        * **Online Community and Influencers are the most popular.**
        * **Trend:** People trust what they see on social media more than normal brand advertisements.
        """)
    st.markdown("---")
    
    # 4. FREQUENCY vs BUDGET
    st.header("4. Interest Intensity Matrix")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_heatmap_freq_budget(df_filtered))
        st.info("""
        **📝 Analysis:**
        * **Many people shop very often but keep a low budget.**
        * **Pattern:** This shows they prefer buying cheap items many times (Fast Fashion) rather than buying one expensive item.
        """)
    st.markdown("---")

    # 5. AWARENESS vs BUDGET
    st.header("5. Awareness vs. Spending Interest")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_scatter_awareness_budget(df_filtered))
        st.info("""
        **📝 Analysis:**
        * **Knowing a lot about fashion (Level 5) doesn't mean spending a lot.**
        * **Insight:** Smart shoppers follow trends by finding cheaper alternatives or sales, not just spending blindly.
        """)
    st.markdown("---")

    # 6. INFLUENCE vs FREQUENCY
    st.header("6. Impact of Drivers on Intensity (Frequency)")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_stacked_influence_freq(df_filtered))
        st.info("""
        **📝 Analysis:**
        * **People who follow Influencers shop more often.**
        * **Link:** Social media always shows new trends every day, making people feel the need to buy things continuously.
        """)
    st.markdown("---")

    # 7. INFLUENCE vs BUDGET
    st.header("7. Impact of Drivers on Spending Power")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c2:
        render_bokeh(chart_stacked_influence_budget(df_filtered))
        st.info("""
        **📝 Analysis:**
        * **Friends and Family usually suggest safer, cheaper choices.**
        * **Insight:** To make people spend big money (over RM1000), they usually need strong convincing from Influencers or Ads.
        """)

    st.markdown("---")
    st.success("✅ **Consumer Interest Analysis Complete (7 Charts)**")

if __name__ == "__main__":
    app()
