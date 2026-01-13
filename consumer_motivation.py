import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Fashion Brand Motivation Analysis",
    layout="wide"
)

# ======================================================
# HELPER: CENTER ALL PLOTLY TITLES
# ======================================================
def center_title(fig):
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center'}
    )
    return fig

# ======================================================
# PAGE TITLE & DESCRIPTION
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")

st.subheader("Objective")
st.markdown(
    "To analyze the driving factors behind why consumers follow fashion brands on social media."
)

# ======================================================
# LOAD & MAP DATA
# ======================================================
@st.cache_data
def load_motivation_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
    # Mapping dictionary to shorten long survey questions
    column_mapping = {
        "I follow fashion brands on social media to get updates on new collections or promotions": "Updates & Promotions",
        "I follow fashion brands on social media because  I like their products and style": "Product & Style",
        "I follow fashion brands on social media because it is entertaining.": "Entertainment",
        "I follow fashion brands on social media because I want to receive discounts or participate in contests.": "Discounts & Contests",
        "I follow fashion brands on social media because it helps me express my personality": "Express Personality",
        "I follow fashion brands on social media because I want to feel part of an online community.": "Online Community",
        "I follow fashion brands on social media because I want to support or show loyalty to the brand.": "Brand Loyalty"
    }
    
    data = data.rename(columns=column_mapping)
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    
    # Clean Gender Column
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].astype(str).str.strip()
        
    return data, valid_cols

df, motivation_cols = load_motivation_data()

if not motivation_cols:
    st.error("Could not find the motivation columns in the CSV. Check your column mapping keys.")
    st.stop()

# ======================================================
# SECTION A: RANKING & GENDER ANALYSIS
# ======================================================
st.header("Section A: Motivation Ranking & Demographic Insights")

# --- Ranking Chart ---
col_rank, col_dumb = st.columns([1, 1.2])

with col_rank:
    st.subheader("Overall Ranking")
    motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
    motivation_means.columns = ['Motivation', 'Average Score']

    fig_ranking = px.bar(
        motivation_means, x='Average Score', y='Motivation',
        orientation='h', text_auto='.2f',
        color='Average Score', color_continuous_scale='Viridis',
        title="Average Agreement Score (Likert 1-5)"
    )
    fig_ranking.update_layout(xaxis_range=[1, 5], height=500)
    st.plotly_chart(center_title(fig_ranking), use_container_width=True)

# --- Dumbbell Plot (Gender Analysis) ---
with col_dumb:
    st.subheader("Gender Comparison")
    
    # Processing Gender Distributions for Plotly
    gender_mean_list = []
    for gender in df['Gender'].unique():
        gender_df = df[df['Gender'] == gender]
        g_means = gender_df[motivation_cols].mean()
        for motivation, score in g_means.items():
            gender_mean_list.append({'Motivation': motivation, 'Gender': gender, 'Mean Score': score})
    
    df_melted_means = pd.DataFrame(gender_mean_list)
    
    # Create Dumbbell using Plotly Graph Objects for better control
    fig_dumbbell = go.Figure()

    for motivation in motivation_cols:
        motivation_data = df_melted_means[df_melted_means['Motivation'] == motivation]
        
        # Add connecting line
        if len(motivation_data) >= 2:
            fig_dumbbell.add_trace(go.Scatter(
                x=motivation_data['Mean Score'], y=[motivation]*len(motivation_data),
                mode='lines', line=dict(color='lightgrey', width=2),
                showlegend=False
            ))

    # Add gender points
    for gender, color in zip(df['Gender'].unique(), ['#FF4B4B', '#1C83E1', '#00C49A']):
        gender_data = df_melted_means[df_melted_means['Gender'] == gender]
        fig_dumbbell.add_trace(go.Scatter(
            x=gender_data['Mean Score'], y=gender_data['Motivation'],
            mode='markers', name=gender,
            marker=dict(color=color, size=12)
        ))

    fig_dumbbell.update_layout(
        title="Mean Scores: Male vs Female Gap",
        xaxis_title="Average Score (Likert Scale)",
        xaxis_range=[2.0, 5.0],
        height=500,
        legend_title="Gender",
        margin=dict(l=20, r=20, t=40, b=40)
    )
    st.plotly_chart(center_title(fig_dumbbell), use_container_width=True)

# Interpretation for Section A
top_motivation = motivation_means.iloc[-1]['Motivation']
bottom_motivation = motivation_means.iloc[0]['Motivation']

with st.expander("📝 Detailed Interpretation: Ranking & Demographic Analysis"):
    st.write(f"""
    * **Primary Driver:** The highest-ranked motivation is **{top_motivation}**. This indicates that the audience is most strongly driven by tangible value and core brand identity. 
    * **Gender Nuance:** The dumbbell plot reveals the "gap" in interest. For example, if markers are far apart, one gender finds that specific motivation significantly more compelling than the other.
    * **Strategic Insight:** Marketing efforts should lean heavily into high-scoring factors while adjusting messaging if a significant gender gap exists in your primary target audience.
    """)
# ======================================================
# SECTION B: CONSUMER SENTIMENT (DISTRIBUTIONS)
# ======================================================
st.divider()
st.header("Section B: Deep Dive into Motivations")
st.write("Analyzing the specific trends and trust factors for each motivation.")



col1, col2 = st.columns(2)

for i, col_name in enumerate(motivation_cols):
    # Data Processing
    counts = df[col_name].value_counts().sort_index().reset_index()
    counts.columns = ['Score', 'Respondents']
    avg_score = df[col_name].mean()
    
    # Create the Chart
    fig_dist = px.bar(
        counts, x='Score', y='Respondents', text='Respondents',
        title=f"Distribution: {col_name}",
        color='Score', color_continuous_scale='Plasma'
    )
    fig_dist.update_layout(showlegend=False, height=350, xaxis_title="1 (Disagree) to 5 (Agree)")
    
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        st.plotly_chart(center_title(fig_dist), use_container_width=True)
        
        # 📝 DYNAMIC ANALYSIS LOGIC
        st.write("### 📝 Analysis:")
        
        # 1. Determine the Driver Status
        if avg_score >= 3.8:
            status = f"**{col_name}** ranks as a **top driver** of interest among respondents."
        elif avg_score >= 3.0:
            status = f"**{col_name}** is a **moderate driver**, showing steady but not primary interest."
        else:
            status = f"**{col_name}** currently ranks as a **minor driver**, suggesting lower impact on this audience."
        
        # 2. Determine the Strategic Trend
        if col_name in ["Online Community", "Brand Loyalty", "Express Personality"]:
            trend = "This confirms that modern consumers trust **social proof** and peer identity more than traditional direct marketing."
        elif col_name in ["Updates & Promotions", "Discounts & Contests"]:
            trend = "This reflects a **transactional trend**, where consumers follow for immediate, tangible rewards and efficiency."
        else:
            trend = "This highlights a focus on **aesthetic alignment**, where the visual 'vibe' of the brand is the main anchor for the consumer."

        st.write(status)
        st.write(f"**Trend:** {trend}")
        st.markdown("---")

# ======================================================
# SECTION C: RELATIONSHIPS
# ======================================================
st.divider()
st.header("Section C: Engagement Relationships")

tab_corr, tab_rel = st.tabs(["Correlation Heatmap", "Relationship Scatters"])

with tab_corr:
    st.write("### How motivations move together")
    corr_matrix = df[motivation_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix, text_auto=".2f",
        color_continuous_scale='RdBu_r',
        title="Correlation Heatmap"
    )
    st.plotly_chart(center_title(fig_heatmap), use_container_width=True)
    
    with st.expander("📝 Detailed Interpretation: Heatmap Correlation"):
        st.write("""
        * **Positive Correlation (Blue):** When two motivations are highly correlated (e.g., > 0.60), it means users who follow for one reason are very likely to follow for the other. 
        * **Strategic Value:** High correlations allow brands to "bundle" content. For example, if 'Entertainment' and 'Style' correlate, entertaining videos should always showcase product style.
        """)

with tab_rel:
    c1, c2 = st.columns([1, 2])
    with c1:
        x_var = st.selectbox("Select X-axis", motivation_cols, index=0)
        y_var = st.selectbox("Select Y-axis", motivation_cols, index=min(1, len(motivation_cols)-1))
        
        current_corr = df[x_var].corr(df[y_var])
        st.write(f"**Correlation Coefficient:** {current_corr:.2f}")
        
        if current_corr > 0.6:
            st.success("Analysis: **Strong Relationship**. These two factors are deeply linked in the consumer's mind.")
        elif current_corr > 0.3:
            st.warning("Analysis: **Moderate Relationship**. There is a visible trend, but other factors are also at play.")
        else:
            st.error("Analysis: **Weak Relationship**. These factors operate independently of one another.")
    
    with c2:
        try:
            import statsmodels
            t_line = "ols"
        except ImportError:
            t_line = None
            
        fig_scatter = px.scatter(
            df, x=x_var, y=y_var, 
            trendline=t_line, 
            opacity=0.4,
            title=f"Relationship: {x_var} vs {y_var}"
        )
        st.plotly_chart(center_title(fig_scatter), use_container_width=True)

st.divider()
st.markdown("✔ **Consumer Motivation Analysis Complete**")
