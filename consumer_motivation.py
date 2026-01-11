import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Config & Title
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")
st.title("📊 Fashion Brand Motivation Dashboard")

# 2. Data Loading Logic
# This URL is used automatically if no file is uploaded
DEFAULT_URL = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Config & Title
st.set_page_config(page_title="Fashion Brand Motivation Analysis", layout="wide")
st.title("📊 Fashion Brand Motivation Dashboard")

# URL for automatic loading
DEFAULT_URL = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"

@st.cache_data
def load_and_clean_data(file_source):
    data = pd.read_csv(file_source)
    # CLEANING: Remove leading/trailing spaces from column names
    data.columns = data.columns.str.strip()
    return data

# Attempt to load data
try:
    # Sidebar uploader exists, but code defaults to URL if empty
    uploaded_file = st.sidebar.file_uploader("Upload a custom CSV (Optional)", type=["csv"])
    source = uploaded_file if uploaded_file is not None else DEFAULT_URL
    df = load_and_clean_data(source)
except Exception as e:
    st.error(f"Error loading data: {e}")
    df = None

if df is not None:
    # LIST OF TARGET COLUMNS
    # Double-check these match your CSV exactly (case-sensitive)
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Check which columns actually exist
    existing_cols = [col for col in motivation_questions if col in df.columns]

    # --- DEBUGGING SECTION ---
    if len(existing_cols) < len(motivation_questions):
        with st.expander("⚠️ Missing Columns Detected - Click to Debug"):
            st.write("Target columns expected:", motivation_questions)
            st.write("Columns found in your file:", list(df.columns))
            st.info("Check if the spelling in the list above matches your CSV column headers exactly.")

    if not existing_cols:
        st.error("None of the required motivation columns were found.")
        st.write("Available columns in your file are:", list(df.columns))
    else:
        # TABS FOR VISUALS
        tab1, tab2, tab3, tab4 = st.tabs([
            "Distributions", "Mean Scores", "Correlations", "Relationship Analysis"
        ])

        sns.set_style("whitegrid")

        with tab1:
            st.header("Response Distribution")
            num_questions = len(existing_cols)
            fig1, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
            if num_questions == 1: axes = [axes]
            
            for i, col in enumerate(existing_cols):
                # Clean up the data to ensure it's numeric/plottable
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
            st.header("Variable Relationship Analysis")
            col_x = st.selectbox("Select X-axis variable", existing_cols, index=0)
            col_y = st.selectbox("Select Y-axis variable", existing_cols, index=min(1, len(existing_cols)-1))
            fig4, ax4 = plt.subplots(figsize=(10, 7))
            sns.regplot(data=df, x=col_x, y=col_y, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax4)
            st.pyplot(fig4)
# Sidebar only for manual file uploads
uploaded_file = st.sidebar.file_uploader("Upload a custom CSV (Optional)", type=["csv"])

@st.cache_data # This keeps the data in memory so it doesn't reload every click
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return pd.read_csv(DEFAULT_URL)

# Execute data loading
try:
    df = load_data(uploaded_file)
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {e}")
    df = None

# 3. Visualization Logic (Only runs if df is successfully created)
if df is not None:
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Verify columns exist in the dataframe
    existing_cols = [col for col in motivation_questions if col in df.columns]

    if not existing_cols:
        st.error("The required motivation columns were not found in this dataset.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "Distributions", "Mean Scores", "Correlations", "Relationship Analysis"
        ])

        sns.set_style("whitegrid")

        # --- TAB 1: DISTRIBUTIONS ---
        with tab1:
            st.header("Response Distribution")
            num_questions = len(existing_cols)
            fig1, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
            
            if num_questions == 1:
                axes = [axes]
            
            for i, col in enumerate(existing_cols):
                response_counts = df[col].astype(str).value_counts().sort_index()
                sns.barplot(x=response_counts.index, y=response_counts.values, ax=axes[i], palette='viridis', hue=response_counts.index, legend=False)
                axes[i].set_title(f"Question: {col.replace('_', ' ').title()}")
                axes[i].set_xlabel("1=Strongly Disagree, 5=Strongly Agree")
            
            plt.tight_layout()
            st.pyplot(fig1)

        # --- TAB 2: MEAN SCORES ---
        with tab2:
            st.header("Overall Motivation Ranking")
            motivation_means = df[existing_cols].mean().sort_values(ascending=False)
            
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax2)
            
            for index, value in enumerate(motivation_means.values):
                ax2.text(value + 0.05, index, f'{value:.2f}', va='center')
            
            ax2.set_xlim(0, 5)
            st.pyplot(fig2)

        # --- TAB 3: HEATMAP ---
        with tab3:
            st.header("Correlation Heatmap")
            fig3, ax3 = plt.subplots(figsize=(10, 8))
            sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
            st.pyplot(fig3)

        # --- TAB 4: RELATIONSHIP ---
        with tab4:
            st.header("Variable Relationship Analysis")
            col_x = st.selectbox("Select X-axis variable", existing_cols, index=1)
            col_y = st.selectbox("Select Y-axis variable", existing_cols, index=5)
            
            fig4, ax4 = plt.subplots(figsize=(10, 7))
            sns.regplot(data=df, x=col_x, y=col_y, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax4)
            st.pyplot(fig4)
