import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Title
st.title("📊 Fashion Brand Motivation Dashboard")

# 2. Data Loading Logic
DEFAULT_URL = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"

@st.cache_data
def load_and_map_data(file_source):
    data = pd.read_csv(file_source)
    data.columns = data.columns.str.strip()
    
    # Mapping the long question sentences to short keys for the code
    column_mapping = {
        "I follow fashion brands on social media to get updates on new collections or promotions": "follow_for_updates_promotions",
        "I follow fashion brands on social media because  I like their products and style": "follow_because_like_products",
        "I follow fashion brands on social media because it is entertaining.": "follow_because_entertaining",
        "I follow fashion brands on social media because I want to receive discounts or participate in contests.": "follow_because_discounts_contests",
        "I follow fashion brands on social media because it helps me express my personality": "follow_because_express_personality",
        "I follow fashion brands on social media because I want to feel part of an online community.": "follow_because_online_community",
        "I follow fashion brands on social media because I want to support or show loyalty to the brand.": "follow_because_support_loyalty"
    }
    
    # Rename columns that exist in the file
    data = data.rename(columns=column_mapping)
    return data

# Handle Data Source (Checks if main.py already uploaded a file, otherwise uses URL)
df = None
if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
    df = load_and_map_data(st.session_state.uploaded_file)
else:
    try:
        df = load_and_map_data(DEFAULT_URL)
    except Exception as e:
        st.error(f"Could not load default data: {e}")

# 3. Visualization Logic
if df is not None:
    motivation_keys = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Filter to only keys that successfully mapped
    existing_cols = [k for k in motivation_keys if k in df.columns]

    if not existing_cols:
        st.error("Motivation columns not found. Please check column naming.")
        st.write("Available columns:", list(df.columns))
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "Distributions", "Mean Scores", "Correlations", "Relationship Analysis"
        ])

        sns.set_style("whitegrid")

        with tab1:
            st.header("Response Distribution")
            fig1, axes = plt.subplots(nrows=len(existing_cols), ncols=1, figsize=(10, 4 * len(existing_cols)))
            if len(existing_cols) == 1: axes = [axes]
            
            for i, col in enumerate(existing_cols):
                counts = df[col].value_counts().sort_index()
                sns.barplot(x=counts.index, y=counts.values, ax=axes[i], palette='viridis', hue=counts.index, legend=False)
                axes[i].set_title(f"Question: {col.replace('_', ' ').title()}")
            
            plt.tight_layout()
            st.pyplot(fig1)

        with tab2:
            st.header("Overall Motivation Ranking")
            motivation_means = df[existing_cols].mean().sort_values(ascending=False)
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax2)
            for index, value in enumerate(motivation_means.values):
                ax2.text(value + 0.05, index, f'{value:.2f}', va='center')
            ax2.set_xlim(0, 5)
            st.pyplot(fig2)

        with tab3:
            st.header("Correlation Heatmap")
            fig3, ax3 = plt.subplots(figsize=(10, 8))
            sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
            st.pyplot(fig3)

        with tab4:
            st.header("Relationship Analysis")
            col_x = st.selectbox("Select X-axis variable", existing_cols, index=1)
            col_y = st.selectbox("Select Y-axis variable", existing_cols, index=5)
            fig4, ax4 = plt.subplots(figsize=(10, 7))
            sns.regplot(data=df, x=col_x, y=col_y, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax4)
            st.pyplot(fig4)
