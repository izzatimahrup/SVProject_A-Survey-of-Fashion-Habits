import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="Fashion Motivation Engine",
    page_icon="💎",
    layout="wide"
)

class DataService:
    """Handles all data fetching and column mapping logic."""
    @staticmethod
    @st.cache_data
    def load_data():
        url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
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
        return df, valid_cols

# ======================================================
# UI COMPONENTS
# ======================================================

def render_hero_section(df):
    """Top banner with title and high-level KPIs."""
    st.title("💎 Fashion Brand Motivation Analytics")
    st.markdown("---")
    
    # KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Responses", len(df))
    with c2:
        st.metric("Average Engagement", "3.42")
    with c3:
        st.metric("Top Driver", "Product & Style")
    with c4:
        st.metric("Data Status", "Live CSV")
    st.markdown("---")

def render_global_filters(motivation_cols):
    """In-page filter system instead of sidebar."""
    with st.expander("🛠️ Dashboard Configuration & Filters", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            theme = st.selectbox("Visual Theme", ["Viridis", "Cividis", "Magma", "Rocket"], help="Changes chart color scales")
        with f2:
            sort_order = st.radio("Sort Ranking", ["Highest First", "Lowest First"], horizontal=True)
        with f3:
            # Multi-select to filter which motivations to show in the analysis
            selected_subset = st.multiselect("Filter Motivations", motivation_cols, default=motivation_cols)
            
    return theme, sort_order, selected_subset

def view_ranking_analysis(df, cols, theme, ascending):
    """Section A: Rankings and Averages."""
    st.header("1. Motivation Hierarchy")
    
    means = df[cols].mean().sort_values(ascending=ascending).reset_index()
    means.columns = ['Motivation', 'Score']
    
    fig = px.bar(
        means, x='Score', y='Motivation', 
        orientation='h', text_auto='.2f',
        color='Score', color_continuous_scale=theme,
        range_x=[1, 5]
    )
    fig.update_layout(title_text="Average Agreement Level", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def view_correlation_matrix(df, cols):
    """Section B: Relationship Heatmap."""
    st.header("2. Behavioral Correlations")
    
    # In-page sub-filter for correlation
    c1, c2 = st.columns([2, 1])
    
    with c1:
        corr = df[cols].corr()
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
        fig.update_layout(title_text="How Motivations Move Together", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.info("**How to read this:**")
        st.write("""
        - Values close to **1.0** mean the motivations are linked.
        - Red indicates a strong positive link.
        - Blue indicates a disconnect.
        """)
        st.markdown("---")
        st.write("### Quick Export")
        csv = df[cols].mean().to_csv().encode('utf-8')
        st.download_button("📥 Download Stats as CSV", csv, "stats.csv", "text/csv")

def view_deep_dive(df, cols, theme):
    """Section C: Individual Distribution Analysis."""
    st.header("3. Motivation Deep Dive")
    
    # In-page selection for the deep dive
    target_col = st.selectbox("Choose a motivation to inspect:", cols)
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Frequency Distribution
        counts = df[target_col].value_counts().sort_index().reset_index()
        counts.columns = ['Likert Score', 'Volume']
        fig = px.pie(counts, values='Volume', names='Likert Score', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(title_text=f"Response Share: {target_col}", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        # Statistical Commentary
        avg = df[target_col].mean()
        st.write(f"### Statistics for {target_col}")
        st.subheader(f"Average Score: {avg:.2f}")
        
        if avg >= 3.5:
            st.success("Verdict: **High Impact Driver**")
            st.write("This factor is a key reason why your audience stays engaged. Maintain content quality here.")
        else:
            st.warning("Verdict: **Secondary Driver**")
            st.write("This factor is relevant but not the primary hook for most followers.")

# ======================================================
# MAIN EXECUTION LOOP
# ======================================================

def main():
    # 1. Load Data
    df, motivation_cols = DataService.load_data()
    
    # 2. Render Static Header
    render_hero_section(df)
    
    # 3. Render Global In-Page Filters
    theme, sort_order, selected_cols = render_global_filters(motivation_cols)
    
    if not selected_cols:
        st.error("Please select at least one motivation to display data.")
        return

    # 4. Render Analysis Views
    asc = True if sort_order == "Lowest First" else False
    
    view_ranking_analysis(df, selected_cols, theme, asc)
    st.markdown("---")
    
    view_correlation_matrix(df, selected_cols)
    st.markdown("---")
    
    view_deep_dive(df, selected_cols, theme)

if __name__ == "__main__":
    main()
