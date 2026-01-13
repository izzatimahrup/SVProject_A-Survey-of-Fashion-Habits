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

def center_title(fig):
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return fig

# ======================================================
# LOAD & MAP DATA
# ======================================================
@st.cache_data
def load_motivation_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
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
    
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].astype(str).str.strip()
        
    return data, valid_cols

df, motivation_cols = load_motivation_data()

# ======================================================
# HEADER
# ======================================================
st.title("📊 Fashion Brand Motivation Dashboard")
st.markdown("---")

# ======================================================
# SECTION A: MOTIVATION RANKING & GENDER COMPARISON
# ======================================================
st.header("Section A: Motivation Ranking & Gender Comparison")

# --- 1. Overall Ranking (Full Width) ---
motivation_means = df[motivation_cols].mean().sort_values(ascending=True).reset_index()
motivation_means.columns = ['Motivation', 'Average Score']

fig_ranking = px.bar(
    motivation_means, x='Average Score', y='Motivation',
    orientation='h', text_auto='.2f',
    color='Average Score', color_continuous_scale='Viridis',
    title="Overall Ranking: Average Agreement Score (Likert 1-5)"
)
fig_ranking.update_layout(xaxis_range=[1, 5], height=450)
st.plotly_chart(center_title(fig_ranking), use_container_width=True)

# --- 2. Summary Metrics (Intermediary insight) ---
top_m = motivation_means.iloc[-1]['Motivation']
st.info(f"💡 **Key Insight:** '{top_m}' is the strongest driver across all respondents. Below, we see how this varies by gender.")

# --- 3. Gender Comparison (Dumbbell Plot - Vertical Stack) ---
st.subheader("Gender Gap Analysis")

# Processing Gender Means
gender_mean_list = []
for gender in df['Gender'].unique():
    g_df = df[df['Gender'] == gender]
    g_means = g_df[motivation_cols].mean()
    for motivation, score in g_means.items():
        gender_mean_list.append({'Motivation': motivation, 'Gender': gender, 'Mean Score': score})

df_melted_means = pd.DataFrame(gender_mean_list)

# Build the Dumbbell Chart
fig_dumbbell = go.Figure()

# Add the "bars" (lines between dots)
for motivation in motivation_cols:
    m_data = df_melted_means[df_melted_means['Motivation'] == motivation]
    if len(m_data) >= 2:
        fig_dumbbell.add_trace(go.Scatter(
            x=m_data['Mean Score'], y=[motivation]*len(m_data),
            mode='lines', line=dict(color='rgba(100,100,100,0.3)', width=3),
            showlegend=False, hoverinfo='skip'
        ))

# Add the Gender Points
colors = {'Female': '#FF4B4B', 'Male': '#1C83E1', 'Other': '#9A9A9A'}
for gender in df['Gender'].unique():
    gender_data = df_melted_means[df_melted_means['Gender'] == gender]
    fig_dumbbell.add_trace(go.Scatter(
        x=gender_data['Mean Score'], y=gender_data['Motivation'],
        mode='markers', name=gender,
        marker=dict(color=colors.get(gender, '#333'), size=14, line=dict(width=1, color='white'))
    ))

fig_dumbbell.update_layout(
    title="Mean Motivation Scores by Gender (Dumbbell Plot)",
    xaxis_title="Average Agreement (1-5)",
    xaxis_range=[1.5, 5.0],
    height=550,
    legend_title="Gender",
    margin=dict(l=20, r=20, t=60, b=40)
)

st.plotly_chart(center_title(fig_dumbbell), use_container_width=True)


 with st.expander("📝 Detailed Interpretation: Section A"):
    st.write(f"""
    * **Ranking:** Respondents consistently prioritize **{top_m}**, suggesting that functional and aesthetic brand value outweighs community-seeking behavior.
    * **Gender Dynamics:** Look at the length of the grey lines in the dumbbell plot. A **long line** indicates a significant difference in motivation between genders, while **overlapping dots** show shared interests.
    * **Strategic Application:** If 'Discounts & Contests' shows a large gap, brand campaigns for that specific motivation should be targeted toward the high-scoring gender for better ROI.
    """)
    
# ======================================================
# SECTION B: CONSUMER SENTIMENT (DISTRIBUTIONS)
# ======================================================
st.divider()
st.header("Section B: Deep Dive into Motivations")
st.write("Analyzing the overall percentage distribution of agreement for each motivation.")

# --- 1. Data Preparation for Stacked Bar ---
likert_labels = {1: 'Strongly Disagree', 2: 'Disagree', 3: 'Neutral', 4: 'Agree', 5: 'Strongly Agree'}
plot_columns = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

# Generate 5 colors from the Plasma scale
# We sample at 0, 0.25, 0.5, 0.75, and 1.0 to get the full range
plasma_colors = px.colors.sample_colorscale("Plasma", [0, 0.25, 0.5, 0.75, 1.0])

pct_list = []
for col in motivation_cols:
    # Get normalized counts (percentages)
    counts = df[col].value_counts(normalize=True).mul(100).reindex([1, 2, 3, 4, 5], fill_value=0)
    pct_list.append(counts.values)

# Create a DataFrame for Plotly
df_pct = pd.DataFrame(pct_list, index=motivation_cols, columns=plot_columns).reset_index()
df_pct = df_pct.rename(columns={'index': 'Motivation'})

# --- 2. Create Plotly Stacked Bar Chart with Plasma Colors ---
fig_stacked = px.bar(
    df_pct, 
    y="Motivation", 
    x=plot_columns,
    title="Percentage Distribution of Responses (Plasma Scale)",
    orientation='h',
    color_discrete_sequence=plasma_colors, # Applied Plasma scale here
    text_auto='.1f'
)

fig_stacked.update_layout(
    xaxis_title="Percentage of Respondents (%)",
    yaxis_title="",
    legend_title="Response",
    barmode='stack',
    height=500,
    xaxis_range=[0, 100],
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(center_title(fig_stacked), use_container_width=True)



# --- 3. Dynamic Analysis Logic ---
st.write("### 📝 Section B Analysis:")

# Identify the motivation with the highest "Positive" (Agree + Strongly Agree) sentiment
df_pct['Positive'] = df_pct['Agree'] + df_pct['Strongly Agree']
top_positive = df_pct.sort_values('Positive', ascending=False).iloc[0]

col_left, col_right = st.columns(2)

with col_left:
    st.success(f"**Highest Agreement:** '{top_positive['Motivation']}' has the highest positive sentiment at **{top_positive['Positive']:.1f}%**.")
    st.write("""
        The color intensity in the chart (moving from dark purple to bright yellow) visualizes the shift from 
        disagreement to strong agreement. The dominance of lighter shades indicates a highly motivated follower base.
    """)

with col_right:
    # Logic for transactional vs aesthetic trends
    if any(keyword in top_positive['Motivation'] for keyword in ["Updates", "Promotions", "Discounts", "Contests"]):
        trend_type = "Transactional"
        trend_desc = "Consumers are primarily motivated by functional benefits and rewards."
    else:
        trend_type = "Relational/Aesthetic"
        trend_desc = "Consumers are driven by emotional connection, style, and brand identity."
    
    st.info(f"**Dominant Trend:** {trend_type}")
    st.write(trend_desc)

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
