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

# ======================================================
# DATA ENGINE CLASS
# ======================================================
class FashionMotivationEngine:
    """Handles data loading, cleaning, and metric calculations."""
    
    def __init__(self, url):
        self.url = url
        self.column_mapping = {
            "I follow fashion brands on social media to get updates on new collections or promotions": "Updates & Promotions",
            "I follow fashion brands on social media because  I like their products and style": "Product & Style",
            "I follow fashion brands on social media because it is entertaining.": "Entertainment",
            "I follow fashion brands on social media because I want to receive discounts or participate in contests.": "Discounts & Contests",
            "I follow fashion brands on social media because it helps me express my personality": "Express Personality",
            "I follow fashion brands on social media because I want to feel part of an online community.": "Online Community",
            "I follow fashion brands on social media because I want to support or show loyalty to the brand.": "Brand Loyalty"
        }
        self.df, self.motivation_cols = self._load_and_process()

    def _load_and_process(self):
        try:
            data = pd.read_csv(self.url)
            data.columns = data.columns.str.strip()
            data = data.rename(columns=self.column_mapping)
            valid_cols = [v for v in self.column_mapping.values() if v in data.columns]
            return data, valid_cols
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame(), []

    def get_rankings(self):
        means = self.df[self.motivation_cols].mean().sort_values(ascending=True).reset_index()
        means.columns = ['Motivation', 'Average Score']
        return means

# ======================================================
# HELPER FUNCTIONS
# ======================================================
def center_title(fig):
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return fig

# ======================================================
# MAIN APPLICATION
# ======================================================
def main():
    # 1. Header & Objective Section
    st.title("📊 Fashion Brand Motivation Dashboard")
    
    with st.container():
        col_obj, col_stat = st.columns([2, 1])
        with col_obj:
            st.subheader("Objective")
            st.info("To analyze the driving factors behind why consumers follow fashion brands on social media, identifying whether trends are transactional, aesthetic, or community-based.")
        
        # 2. Load Data
        data_url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
        engine = FashionMotivationEngine(data_url)
        
        if engine.df.empty:
            st.stop()

        with col_stat:
            st.metric("Total Respondents", len(engine.df))
            top_val = engine.get_rankings().iloc[-1]
            st.metric("Top Motivation", top_val['Motivation'], f"{top_val['Average Score']:.2f} Avg")

    st.divider()

    # 3. Sidebar Configuration
    st.sidebar.header("🎨 Visual Settings")
    color_theme = st.sidebar.selectbox("Color Theme", ["Viridis", "Plasma", "Cividis", "Magma"])
    
    # 4. Analysis Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Ranking & Distribution", "🔗 Correlation Analysis", "👥 Detailed Trends"])

    # --- Tab 1: Ranking & Distribution ---
    with tab1:
        st.header("Section A: Motivation Ranking")
        rank_df = engine.get_rankings()
        
        fig_ranking = px.bar(
            rank_df, x='Average Score', y='Motivation',
            orientation='h', text_auto='.2f',
            color='Average Score', color_continuous_scale=color_theme,
            title="Global Motivation Leaderboard"
        )
        fig_ranking.update_layout(xaxis_range=[1, 5])
        st.plotly_chart(center_title(fig_ranking), use_container_width=True)

        st.subheader("Frequency Distribution")
        selected_col = st.selectbox("Select Motivation to View Distribution", engine.motivation_cols)
        
        counts = engine.df[selected_col].value_counts().sort_index().reset_index()
        counts.columns = ['Likert Score', 'Respondents']
        
        fig_dist = px.bar(
            counts, x='Likert Score', y='Respondents', 
            text='Respondents', color='Likert Score',
            color_continuous_scale=color_theme,
            title=f"Distribution Analysis: {selected_col}"
        )
        st.plotly_chart(center_title(fig_dist), use_container_width=True)

    # --- Tab 2: Correlation ---
    with tab2:
        st.header("Section B: Engagement Relationships")
        
        col_heat, col_scatter = st.columns([1, 1])
        
        with col_heat:
            st.write("### Motivation Heatmap")
            corr = engine.df[engine.motivation_cols].corr()
            fig_heat = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r')
            st.plotly_chart(center_title(fig_heat), use_container_width=True)
            
        with col_scatter:
            st.write("### Relationship Deep-Dive")
            x_var = st.selectbox("Motivation X", engine.motivation_cols, index=0)
            y_var = st.selectbox("Motivation Y", engine.motivation_cols, index=1)
            
            fig_rel = px.scatter(engine.df, x=x_var, y=y_var, trendline="ols", opacity=0.5)
            st.plotly_chart(center_title(fig_rel), use_container_width=True)

    # --- Tab 3: Detailed Trends ---
    with tab3:
        st.header("Section C: Strategic Categorization")
        
        # Grid layout for dynamic logic
        cols = st.columns(2)
        for i, col_name in enumerate(engine.motivation_cols):
            avg_score = engine.df[col_name].mean()
            
            # Category Logic
            if col_name in ["Online Community", "Brand Loyalty", "Express Personality"]:
                cat = "Social Proof & Identity"
                icon = "👥"
            elif col_name in ["Updates & Promotions", "Discounts & Contests"]:
                cat = "Transactional Value"
                icon = "💰"
            else:
                cat = "Aesthetic Alignment"
                icon = "🎨"

            with cols[i % 2]:
                with st.expander(f"{icon} {col_name}", expanded=True):
                    st.write(f"**Average Score:** {avg_score:.2f}")
                    st.write(f"**Strategic Category:** {cat}")
                    
                    if avg_score >= 3.8:
                        st.success("Status: **Primary Driver**")
                    elif avg_score >= 3.0:
                        st.warning("Status: **Moderate Driver**")
                    else:
                        st.error("Status: **Minor Driver**")

    st.divider()
    st.markdown("<center>✔ <b>Consumer Motivation Analysis Framework Complete</b></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
