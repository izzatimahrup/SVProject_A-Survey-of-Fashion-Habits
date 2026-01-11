import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Config
st.set_page_config(page_title="Fashion Motivation Analysis", layout="wide")
sns.set_style("whitegrid")

st.title("📊 Fashion Brand Motivation Dashboard")

# 2. File Uploader
uploaded_file = st.sidebar.file_uploader("Upload your survey CSV", type=["csv"])

if uploaded_file is not None:
    # Load data and clean column names immediately
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip() # Remove hidden spaces
    
    st.sidebar.success("File Uploaded!")

    # 3. Dynamic Column Mapping
    # This prevents KeyErrors by letting you pick the right columns from your file
    st.sidebar.header("Map Motivation Questions")
    all_columns = df.columns.tolist()
    
    # We create a list of columns to analyze based on user selection
    motivation_questions = st.sidebar.multiselect(
        "Select the columns that represent Motivation Questions:",
        options=all_columns,
        default=all_columns[:7] if len(all_columns) >= 7 else all_columns
    )

    if not motivation_questions:
        st.warning("Please select at least one column from the sidebar to begin analysis.")
    else:
        # --- APP NAVIGATION ---
        tabs = st.tabs(["Distributions", "Mean Scores", "Correlations", "Regression"])

        # TAB 1: DISTRIBUTIONS
        with tabs[0]:
            st.header("Response Distributions")
            num_questions = len(motivation_questions)
            fig, axes = plt.subplots(nrows=num_questions, ncols=1, figsize=(10, 5 * num_questions))
            
            # Fix for single plot indexing
            if num_questions == 1:
                axes = [axes]

            for i, col in enumerate(motivation_questions):
                # Clean data: drop NaNs and ensure string for categorical counting
                clean_data = df[col].dropna().astype(str)
                response_counts = clean_data.value_counts().sort_index()
                
                ax = axes[i]
                sns.barplot(
                    x=response_counts.index, 
                    y=response_counts.values, 
                    ax=ax, 
                    palette='viridis', 
                    hue=response_counts.index, 
                    legend=False
                )
                ax.set_title(f"Question: {col}", fontsize=14)
                ax.set_xlabel('Response (1=Strongly Disagree, 5=Strongly Agree)')
                ax.set_ylabel('Count')
            
            plt.tight_layout()
            st.pyplot(fig)

        # TAB 2: MEAN SCORES
        with tabs[1]:
            st.header("Average Agreement Scores")
            # Convert to numeric, errors='coerce' turns non-numeric text into NaN
            numeric_df = df[motivation_questions].apply(pd.to_numeric, errors='coerce')
            motivation_means = numeric_df.mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax)
            
            for index, value in enumerate(motivation_means.values):
                ax.text(value + 0.05, index, f'{value:.2f}', va='center')
            
            ax.set_xlim(0, 5)
            st.pyplot(fig)

        # TAB 3: CORRELATIONS
        with tabs[2]:
            st.header("Correlation Heatmap")
            numeric_df = df[motivation_questions].apply(pd.to_numeric, errors='coerce')
            corr = numeric_df.corr()

            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig)

        # TAB 4: REGRESSION
        with tabs[3]:
            st.header("Bivariate Relationship")
            col1 = st.selectbox("Select X-axis:", motivation_questions, index=0)
            col2 = st.selectbox("Select Y-axis:", motivation_questions, index=min(1, len(motivation_questions)-1))
            
            fig, ax = plt.subplots(figsize=(10, 7))
            # dropna for the specific pair to avoid errors
            reg_data = df[[col1, col2]].apply(pd.to_numeric, errors='coerce').dropna()
            
            sns.regplot(data=reg_data, x=col1, y=col2, scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax)
            st.pyplot(fig)

else:
    st.info("Please upload a CSV file in the sidebar to generate the visualizations.")
    # Example of how the data should look
    st.write("Your CSV should look something like this:")
    sample_data = pd.DataFrame({
        'Question_1': [5, 4, 3, 5, 2],
        'Question_2': [4, 4, 2, 5, 1],
        'Question_3': [1, 2, 2, 1, 3]
    })
    st.table(sample_data)
