import streamlit as st
import pandas as pd
import plotly.express as px

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
    # Extract only the values that now exist as column names in the dataframe
    valid_cols = [v for v in column_mapping.values() if v in data.columns]
    return data, valid_cols

df, motivation_cols = load_motivation_data()

if not motivation_cols:
    st.error("Could not find the motivation columns in the CSV. Check your column mapping keys.")
    st.stop()

# ======================================================
# SECTION A: RANKING
# ======================================================
st.header("Section A: Motivation Ranking")
motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Average Score']

fig_ranking = px.bar(
    motivation_means, x='Average Score', y='Motivation',
    orientation='h', text_auto='.2f',
    color='Average Score', color_continuous_scale='Viridis',
    title="Average Agreement Score (Likert 1-5)"
)
fig_ranking.update_layout(xaxis_range=[1, 5])
st.plotly_chart(center_title(fig_ranking), use_container_width=True)

# Interpretation for Section A
top_motivation = motivation_means.iloc[-1]['Motivation']
bottom_motivation = motivation_means.iloc[0]['Motivation']

with st.expander("📝 Detailed Interpretation: Ranking Analysis"):
    st.write(f"""
    * **Primary Driver:** The highest-ranked motivation is **{top_motivation}**. This indicates that the audience is most strongly driven by tangible value and core brand identity. 
    * **Strategic Insight:** Marketing efforts should lean heavily into the highest-scoring factors to ensure maximum follower retention.
    * **Opportunity Gap:** The lowest score for **{bottom_motivation}** suggests either a lack of interest from the audience or an untapped area where brands could improve their engagement strategies.
    """)

# ======================================================
# SECTION B: AUDIENCE SENTIMENT (DISTRIBUTIONS)
# ======================================================
st.divider()
st.header("Section B: Deep Dive into Motivations")
st.write("Analyzing how 'polarized' or 'unified' your audience is regarding specific brand values.")

col1, col2 = st.columns(2)
for i, col_name in enumerate(motivation_cols):
    counts = df[col_name].value_counts().sort_index().reset_index()
    counts.columns = ['Score', 'Respondents']
    avg_score = df[col_name].mean()
    
    fig_dist = px.bar(
        counts, x='Score', y='Respondents', text='Respondents',
        title=f"Distribution: {col_name}",
        color='Score', color_continuous_scale='Plasma'
    )
    fig_dist.update_layout(showlegend=False, height=350)
    
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.plotly_chart(center_title(fig_dist), use_container_width=True)
        
        # RELEVANT INTERPRETATION LOGIC
        if col_name == "Updates & Promotions":
            st.write("💡 **Insight:** This measures 'Functional Value.' High scores mean followers use your page as a catalog. Don't post fluff; post products.")
        elif col_name == "Product & Style":
            st.write("💡 **Insight:** This measures 'Aesthetic Value.' High scores suggest your brand is a source of inspiration. Focus on high-quality photography.")
        elif col_name == "Discounts & Contests":
            st.write("💡 **Insight:** This measures 'Transactional Value.' If this is high, your followers are price-sensitive. Use 'Limited Time Offers' to trigger sales.")
        elif col_name == "Express Personality":
            st.write("💡 **Insight:** This measures 'Self-Identity.' If high, followers see your brand as a badge of who they are. Focus on lifestyle and 'vibe'.")
        else:
            if avg_score > 3.5:
                st.write(f"💡 **Insight:** A strong secondary driver. **{col_name}** helps build long-term retention beyond just products.")
            else:
                st.write(f"💡 **Insight:** Lower relevance. **{col_name}** is not a main priority for your current audience.")
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
