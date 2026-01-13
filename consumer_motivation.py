import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="Motivation Analytics", layout="wide")

class MotivationAnalyzer:
    """Class to handle data processing and visualization logic."""
    
    def __init__(self, dataframe):
        self.df = dataframe
        self.questions = [col for col in dataframe.columns if col.startswith('follow_')]
        self.likert_labels = {
            1: 'Strongly Disagree', 2: 'Disagree', 
            3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'
        }
        self.likert_colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

    def get_mean_scores(self):
        return self.df[self.questions].mean().sort_values(ascending=False)

    def get_distribution_data(self):
        dist_list = []
        for col in self.questions:
            counts = self.df[col].value_counts(normalize=True).mul(100).reindex(range(1, 6), fill_value=0)
            counts.index = counts.index.map(self.likert_labels)
            counts.name = col
            dist_list.append(counts)
        return pd.DataFrame(dist_list)

    def get_gender_data(self):
        if 'Gender' not in self.df.columns:
            return None
        gender_means = self.df.groupby('Gender')[self.questions].mean().T.reset_index()
        melted = gender_means.melt(id_vars='index', var_name='Gender', value_name='Mean Score')
        melted.rename(columns={'index': 'Motivation Question'}, inplace=True)
        return melted

# --- UI COMPONENTS ---

def sidebar_setup():
    st.sidebar.header("📁 Data Management")
    uploaded_file = st.sidebar.file_uploader("Upload Survey CSV", type=["csv"])
    
    st.sidebar.header("🎨 Visual Settings")
    palette = st.sidebar.selectbox("Theme Palette", ['viridis', 'magma', 'coolwarm', 'rocket'])
    
    return uploaded_file, palette

def render_header():
    st.title("📊 Motivation Survey Analysis Dashboard")
    st.markdown("""
        Analyze user engagement drivers. This tool processes Likert-scale responses 
        to provide insights into **why** users follow and interact with your brand.
    """)
    st.divider()

def main():
    uploaded_file, palette = sidebar_setup()
    render_header()

    # Load Data
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        # Generate high-quality dummy data for demonstration
        questions = [
            'follow_for_updates_promotions', 'follow_because_like_products',
            'follow_because_entertaining', 'follow_because_discounts_contests',
            'follow_because_express_personality', 'follow_because_online_community',
            'follow_because_support_loyalty'
        ]
        df = pd.DataFrame(np.random.randint(1, 6, size=(300, len(questions))), columns=questions)
        df['Gender'] = np.random.choice(['Male', 'Female'], size=300)
        st.info("💡 Showing sample data. Upload a CSV via the sidebar to analyze your specific results.")

    analyzer = MotivationAnalyzer(df)

    # --- Metrics Row ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Responses", len(df))
    m2.metric("Motivations Tracked", len(analyzer.questions))
    m3.metric("Highest Mean Score", f"{analyzer.get_mean_scores().max():.2f}")

    # --- Tabs Interface ---
    tab1, tab2, tab3 = st.tabs(["📈 Sentiment Analysis", "🔗 Correlations", "👥 Demographic Split"])

    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Ranking by Mean Score")
            means = analyzer.get_mean_scores()
            fig, ax = plt.subplots()
            sns.barplot(x=means.values, y=means.index, palette=palette, ax=ax)
            ax.set_xlim(0, 5)
            st.pyplot(fig)

        with col2:
            st.subheader("Response Distribution")
            dist_df = analyzer.get_distribution_data()
            fig, ax = plt.subplots()
            dist_df[list(analyzer.likert_labels.values())].plot(
                kind='barh', stacked=True, color=analyzer.likert_colors, ax=ax
            )
            ax.legend(bbox_to_anchor=(1.0, 1.0))
            st.pyplot(fig)

    with tab2:
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("Global Correlation Matrix")
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(df[analyzer.questions].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig)
        
        with col_b:
            st.subheader("Deep Dive")
            x_var = st.selectbox("Motivation A", analyzer.questions, index=0)
            y_var = st.selectbox("Motivation B", analyzer.questions, index=1)
            fig, ax = plt.subplots()
            sns.regplot(data=df, x=x_var, y=y_var, scatter_kws={'alpha':0.3}, ax=ax)
            st.pyplot(fig)

    with tab3:
        st.subheader("Gender Behavioral Comparison")
        gender_data = analyzer.get_gender_data()
        if gender_data is not None:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.pointplot(
                data=gender_data, x='Mean Score', y='Motivation Question', 
                hue='Gender', join=True, palette='Set1', markers='o', ax=ax
            )
            ax.set_xlim(1, 5)
            st.pyplot(fig)
        else:
            st.warning("No 'Gender' column found for comparison.")

    # --- Export Section ---
    st.sidebar.divider()
    if st.sidebar.button("Generate CSV Summary"):
        summary = analyzer.get_mean_scores().to_csv().encode('utf-8')
        st.sidebar.download_button("📥 Download Summary", summary, "motivation_summary.csv", "text/csv")

if __name__ == "__main__":
    main()
