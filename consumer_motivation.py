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
    """Handles data processing and Likert distribution logic."""
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

def render_hero_section(df):
    st.title("💎 Fashion Brand Motivation Analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Responses", len(df))
    c2.metric("Top Driver", "Product & Style")
    c3.metric("Scale", "Likert (1-5)")
    st.markdown("---")

def render_filters(cols):
    """In-page filter expander."""
    with st.expander("🛠️ Dashboard Configuration", expanded=True):
        f1, f2 = st.columns(2)
        with f1:
            selected_cols = st.multiselect("Filter Motivations", cols, default=cols)
        with f2:
            chart_type = st.radio("Chart Preference", ["Interactive (Plotly)", "Static (Matplotlib)"], horizontal=True)
    return selected_cols, chart_type

def view_stacked_distribution(df, cols, chart_type):
    """Section: Percentage Distribution using your specific logic."""
    st.header("1. Percentage Distribution (Stacked)")
    
    # Calculate Data
    df_pct = DataService.get_pct_dist(df, cols)
    plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

    if chart_type == "Static (Matplotlib)":
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12, 6))
        df_pct[plot_columns].plot(kind='barh', stacked=True, color=colors, ax=ax, width=0.8)
        ax.set_xlim(0, 100)
        ax.set_xlabel("Percentage (%)")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
    else:
        # Interactive Plotly Version of your logic
        fig = px.bar(
            df_pct.reset_index(), 
            y='index', 
            x=plot_columns,
            orientation='h',
            color_discrete_sequence=colors,
            labels={'value': 'Percentage (%)', 'index': 'Motivation', 'variable': 'Response'},
            title="Response Sentiment Distribution"
        )
        fig.update_layout(legend_direction="h", legend_y=-0.2)
        st.plotly_chart(fig, use_container_width=True)



def view_correlation_hub(df, cols):
    st.header("2. Behavioral Correlations")
    c1, c2 = st.columns([2, 1])
    with c1:
        corr = df[cols].corr()
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.info("💡 **Insight:** Strong correlations (Red) suggest that users who value one motivation usually value the other.")
        csv = df[cols].corr().to_csv().encode('utf-8')
        st.download_button("📥 Download Correlation CSV", csv, "correlation.csv")

# ======================================================
# MAIN EXECUTION
# ======================================================
def main():
    df, motivation_cols = DataService.load_data()
    render_hero_section(df)
    
    selected_cols, chart_type = render_filters(motivation_cols)
    
    if selected_cols:
        view_stacked_distribution(df, selected_cols, chart_type)
        st.markdown("---")
        view_correlation_hub(df, selected_cols)
    else:
        st.warning("Please select at least one motivation column.")

if __name__ == "__main__":
    main()
