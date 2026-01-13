import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Respondent Motivation Analysis", layout="wide")

# Styling for a clean professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING HELPER ---
def load_real_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    # Cleaning Gender as per your original logic
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].astype(str).str.strip()
    return df

# --- MAIN HEADER & FILE UPLOAD ---
st.title("📊 Respondent Motivation Analysis")
st.markdown("Upload your survey results CSV to generate the behavioral insights dashboard.")

uploaded_file = st.file_uploader("Upload Respondent CSV", type=["csv"])

if uploaded_file is not None:
    # Load the actual data
    df = load_real_data(uploaded_file)
    
    # Define your specific survey questions
    motivation_questions = [
        'follow_for_updates_promotions', 'follow_because_like_products',
        'follow_because_entertaining', 'follow_because_discounts_contests',
        'follow_because_express_personality', 'follow_because_online_community',
        'follow_because_support_loyalty'
    ]

    # Verify columns exist
    missing_cols = [q for q in motivation_questions if q not in df.columns]
    if missing_cols:
        st.error(f"Missing columns in CSV: {missing_cols}")
        st.stop()

    # --- GLOBAL FILTERS SECTION ---
    with st.container():
        st.subheader("🎯 Dashboard Filters")
        col_f1, col_f2 = st.columns([2, 3])
        
        with col_f1:
            genders = sorted(df['Gender'].unique())
            selected_genders = st.multiselect("Filter by Gender", options=genders, default=genders)
            
        filtered_df = df[df['Gender'].isin(selected_genders)]
        
        with col_f2:
            st.write("###") # Padding
            st.metric("Total Respondents", len(filtered_df), delta=f"{len(filtered_df) - len(df)} from total")

    st.divider()

    # --- ANALYSIS TABS ---
    tab1, tab2, tab3 = st.tabs(["📊 Performance & Means", "🔗 Correlations", "👥 Demographic Split"])

    # --- TAB 1: MEANS & DISTRIBUTION ---
    with tab1:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### Mean Agreement Scores")
            motivation_means = filtered_df[motivation_questions].mean().sort_values(ascending=False)
            fig1, ax1 = plt.subplots(figsize=(10, 8))
            sns.barplot(x=motivation_means.values, y=motivation_means.index, palette='viridis', ax=ax1)
            ax1.set_xlim(0, 5)
            for i, v in enumerate(motivation_means.values):
                ax1.text(v + 0.05, i, f'{v:.2f}', va='center', fontweight='bold')
            st.pyplot(fig1)

        with col_right:
            st.markdown("#### Response Distribution (%)")
            # Calculation for Likert distribution
            dist_data = []
            for q in motivation_questions:
                counts = filtered_df[q].value_counts(normalize=True).reindex(range(1, 6), fill_value=0) * 100
                dist_data.append(counts.values)
            
            df_pct = pd.DataFrame(dist_data, index=motivation_questions, 
                                 columns=['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'])
            
            fig2, ax2 = plt.subplots(figsize=(10, 8))
            df_pct.plot(kind='barh', stacked=True, 
                        color=["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"], ax=ax2)
            ax2.set_xlim(0, 100)
            ax2.legend(bbox_to_anchor=(1.0, 1.0))
            st.pyplot(fig2)

    # --- TAB 2: CORRELATIONS ---
    with tab2:
        st.markdown("#### Relationship Analysis")
        c1, c2 = st.columns([3, 2])
        
        with c1:
            st.caption("Correlation Heatmap: How motivations link together")
            corr = filtered_df[motivation_questions].corr()
            fig3, ax3 = plt.subplots(figsize=(10, 7))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
            st.pyplot(fig3)
            
        with c2:
            st.caption("Regression: Predictive Relationship")
            x_var = st.selectbox("Select X Motivation", motivation_questions, index=1)
            y_var = st.selectbox("Select Y Motivation", motivation_questions, index=5)
            fig4, ax4 = plt.subplots()
            sns.regplot(data=filtered_df, x=x_var, y=y_var, scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax4)
            st.pyplot(fig4)

    # --- TAB 3: GENDER ANALYSIS (DUMBBELL) ---
    with tab3:
        st.markdown("#### Gender Dumbbell Comparison")
        if len(selected_genders) < 2:
            st.warning("Please select at least two genders to compare.")
        else:
            # Grouping data as per your original logic
            gender_means = filtered_df.groupby('Gender')[motivation_questions].mean().T
            df_melted = gender_means.reset_index().melt(id_vars='index', var_name='Gender', value_name='Mean Score')
            
            fig5, ax5 = plt.subplots(figsize=(12, 8))
            sns.pointplot(data=df_melted, x='Mean Score', y='index', hue='Gender',
                          join=True, palette='Set1', markers='o', scale=1.1, ax=ax5)
            ax5.set_xlim(1, 5)
            ax5.grid(True, axis='x', linestyle='--', alpha=0.5)
            ax5.set_ylabel("Motivation")
            st.pyplot(fig5)

else:
    st.info("👋 Please upload a CSV file to begin the analysis.")
    # Show a small preview/example of expected format
    st.caption("Expected columns: 'Gender', 'follow_for_updates_promotions', 'follow_because_like_products', etc.")
