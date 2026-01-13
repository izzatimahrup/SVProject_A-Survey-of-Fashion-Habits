import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="Fashion Brand Motivation Analysis",
    page_icon="📊",
    layout="wide"
)

class DataService:
    """Handles data fetching, mapping, and Likert distribution logic."""
    @staticmethod
    @st.cache_data
    def load_data():
        # URL for the specific Fashion Habit dataset
        url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
        # Shortening long survey questions for better UI display
        mapping = {
            "I follow fashion brands on social media to get updates on new collections or promotions": "Updates & Promotions",
            "I follow fashion brands on social media because  I like their products and style": "Product & Style",
            "I follow fashion brands on social media because it is entertaining.": "Entertainment",
            "I follow fashion brands on social media because I want to receive discounts or participate in contests.": "Discounts & Contests",
            "I follow fashion brands on social media because it helps me express my personality": "Express Personality",
            "I follow fashion brands on social media because I want to feel part of an online community.": "Online Community",
            "I follow fashion brands on social media because I want to support or show loyalty to the brand.": "Brand Loyalty"
        }
        df = df.rename(columns=mapping)
        valid_cols = [v for v in mapping.values() if v in df.columns]
        
        # Ensure we are looking at the specific 104 responses
        if len(df) > 104:
            df = df.head(104)
            
        return df, valid_cols

    @staticmethod
    def get_pct_dist(data, cols):
        """Calculates percentage distribution for the Likert scale."""
        dist_list = []
        labels = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
        for col in cols:
            counts = data[col].value_counts(normalize=True).mul(100).reindex(range(1, 6), fill_value=0)
            counts.index = counts.index.map(labels)
            counts.name = col
            dist_list.append(counts)
        return pd.DataFrame(dist_list)

# ======================================================
# UI VIEWS
# ======================================================

def render_hero_section(df, motivation_cols):
    st.title("💎 Fashion Brand Motivation Analytics")
    
    # KPI Metrics Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Responses", len(df))
    
    # Calculate top driver based on means
    means = df[motivation_cols].mean()
    top_driver = means.idxmax()
    c2.metric("Top Driver", top_driver, f"{means.max():.2f} Avg")
    
    c3.metric("Survey Scale", "Likert (1-5)")
    st.markdown("---")

def render_in_page_filters(cols):
    """Configuration hub inside an expander (no sidebar)."""
    with st.expander("🛠️ Dashboard Settings & Column Filters", expanded=True):
        f1, f2 = st.columns(2)
        with f1:
            selected = st.multiselect("Select Motivations to Analyze", cols, default=cols)
        with f2:
            palette = st.selectbox("Color Palette", ["RdBu_r", "Viridis", "Magma"])
    return selected, palette

def view_stacked_distribution(df, cols):
    """Renders the percentage distribution using the requested stacked bar logic."""
    st.header("1. Percentage Distribution (Stacked)")
    
    df_pct = DataService.get_pct_dist(df, cols)
    plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

    # Using Plotly for interactive version of your Matplotlib logic
    fig = px.bar(
        df_pct.reset_index(), 
        y='index', 
        x=plot_columns,
        orientation='h',
        color_discrete_sequence=colors,
        labels={'value': 'Percentage (%)', 'index': 'Motivation', 'variable': 'Response'},
        title="Agreement Levels Across Motivations"
    )
    
    # Corrected Legend Syntax for Plotly compatibility
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=100),
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)



def view_correlation_matrix(df, cols, palette):
    """Heatmap analysis for behavioral links."""
    st.header("2. Behavioral Correlations")
    
    c_chart, c_info = st.columns([2, 1])
    
    with c_chart:
        corr = df[cols].corr()
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=palette)
        fig.update_layout(title_text="Linkage Between Motivations", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
        
    with c_info:
        st.info("**Analysis Insight:**")
        st.write("A score above **0.50** suggests that users follow for both reasons simultaneously. Brands can use these links to cross-promote content.")
        
        # In-page Download
        csv = df[cols].mean().to_csv().encode('utf-8')
        st.download_button("📥 Download Analysis Summary", csv, "motivation_summary.csv", "text/csv")

# ======================================================
# MAIN EXECUTION
# ======================================================
def main():
    # Load the 104 responses
    df, motivation_cols = DataService.load_data()
    
    if df.empty:
        st.error("Data could not be loaded. Check the URL.")
        return

    # Header
    render_hero_section(df, motivation_cols)
    
    # Filters (Now in-page, not sidebar)
    selected_cols, palette = render_in_page_filters(motivation_cols)
    
    if selected_cols:
        view_stacked_distribution(df, selected_cols)
        st.divider()
        view_correlation_matrix(df, selected_cols, palette)
    else:
        st.warning("Please select motivations to view the analysis.")

if __name__ == "__main__":
    main()
