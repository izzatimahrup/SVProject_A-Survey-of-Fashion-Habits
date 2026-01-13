import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Config
st.set_page_config(page_title="Motivation Analysis Dashboard", layout="wide")

st.title("📊 Motivation Survey Analysis Dashboard")
st.markdown("This dashboard visualizes the drivers behind user engagement based on Likert scale survey data.")

# --- 1. Data Loading ---
@st.cache_data
def load_sample_data():
    """Generates dummy data if no file is uploaded."""
    questions = [
        'follow_for_updates_promotions', 'follow_because_like_products',
        'follow_because_entertaining', 'follow_because_discounts_contests',
        'follow_because_express_personality', 'follow_because_online_community',
        'follow_because_support_loyalty'
    ]
    data = np.random.randint(1, 6, size=(200, len(questions)))
    df = pd.DataFrame(data, columns=questions)
    df['Gender'] = np.random.choice(['Male', 'Female'], size=200)
    return df, questions

uploaded_file = st.sidebar.file_uploader("Upload your survey CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Basic cleaning for Gender column
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].astype(str).str.strip()
    motivation_questions = [col for col in df.columns if col.startswith('follow_')]
else:
    df, motivation_questions = load_sample_data()
    st.sidebar.info("Using sample data. Upload a CSV to analyze your own.")

# --- 2. Sidebar Filters ---
st.sidebar.header("Settings")
selected_palette = st.sidebar.selectbox("Color Palette", ['viridis', 'magma', 'coolwarm', 'rocket'])

# --- 3. Analysis Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Mean Scores", "Correlations", "Distribution", "Gender Comparison"])

with tab1:
    st.subheader("Mean Agreement Scores")
    motivation_means = df[motivation_questions].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=motivation_means.values, y=motivation_means.index, palette=selected_palette, ax=ax)
    ax.set_xlim(0, 5)
    for index, value in enumerate(motivation_means.values):
        ax.text(value + 0.05, index, f'{value:.2f}', va='center')
    st.pyplot(fig)

with tab2:
    st.subheader("Correlation Heatmap")
    corr_matrix = df[motivation_questions].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    st.divider()
    
    st.subheader("Relationship Between Specific Motivations")
    col_x = st.selectbox("Select X axis", motivation_questions, index=1)
    col_y = st.selectbox("Select Y axis", motivation_questions, index=5)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=df, x=col_x, y=col_y, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)
    st.pyplot(fig)

with tab3:
    st.subheader("Percentage Distribution (Stacked)")
    
    # Calculate percentages for the Likert scale
    def get_pct_dist(data, cols):
        dist_list = []
        labels = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
        for col in cols:
            counts = data[col].value_counts(normalize=True).mul(100).reindex(range(1, 6), fill_value=0)
            counts.index = counts.index.map(labels)
            counts.name = col
            dist_list.append(counts)
        return pd.DataFrame(dist_list)

    df_pct = get_pct_dist(df, motivation_questions)
    plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]

    fig, ax = plt.subplots(figsize=(12, 8))
    df_pct[plot_columns].plot(kind='barh', stacked=True, color=colors, ax=ax, width=0.8)
    ax.set_xlim(0, 100)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

with tab4:
    st.subheader("Gender Comparison (Dumbbell Plot)")
    
    if 'Gender' in df.columns:
        # Calculate means by gender
        gender_means = df.groupby('Gender')[motivation_questions].mean().T.reset_index()
        df_melted = gender_means.melt(id_vars='index', var_name='Gender', value_name='Mean Score')
        df_melted.rename(columns={'index': 'Motivation Question'}, inplace=True)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.pointplot(
            data=df_melted, x='Mean Score', y='Motivation Question', hue='Gender',
            join=True, palette={'Female': 'red', 'Male': 'blue', 'nan': 'gray'},
            markers='o', linestyles='-', capsize=0.1, ax=ax
        )
        ax.set_xlim(1, 5)
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
    else:
        st.error("Gender column not found in dataset.")

st.sidebar.markdown("---")
st.sidebar.write("Created with ❤️ using Streamlit & Seaborn")
