import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG (LIKE REFERENCE)
# ======================================================
st.set_page_config(
    page_title="Consumer Behaviour Dashboard",
    layout="wide"
)
# ======================================================
# HELPER: CENTER ALL PLOTLY TITLES
# ======================================================
def center_title(fig):
    fig.update_layout(
        title={
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    return fig

# ======================================================
# PAGE TITLE & DESCRIPTION
# ======================================================
st.title("📊 Consumer Behaviour Analysis")
st.markdown("""
This dashboard presents an analysis of social media engagement patterns, 
and consumer behaviour based on survey data.
""")
    
st.subheader("Objective")

st.markdown("To assess the level of activity and engagement of consumers on social media platforms in relation to fashion.")

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

df = load_data()

if df.empty:
    st.stop()

# ======================================================
# SECTION A
# ======================================================
st.header("Section A: Social Media Usage Overview")

# ------------------------------------------------------
# DONUT CHART: MOST USED PLATFORMS
# ------------------------------------------------------
most_used_levels = [0, 1]

platforms_to_compare = [
    'Active_Pinterest_Ordinal',
    'Active_Tiktok_Ordinal',
    'Active_Instagram_Ordinal',
    'Active_Threads_Ordinal'
]

most_used_counts = {}

for col in platforms_to_compare:
    if col in df.columns:
        count = df[df[col].isin(most_used_levels)].shape[0]
        platform_name = col.replace('Active_', '').replace('_Ordinal', '')
        most_used_counts[platform_name] = count

usage_df = pd.DataFrame({
    'Platform': list(most_used_counts.keys()),
    'Count': list(most_used_counts.values())
})

fig1 = px.pie(
    usage_df,
    values='Count',
    names='Platform',
    hole=0.4,
    title="Comparison of Most Used Social Media Platforms"
)

fig1.update_traces(textposition='inside', textinfo='percent+label')
fig1 = center_title(fig1)

st.plotly_chart(fig1, use_container_width=True)

st.info("""
**Interpretation:**
The survey reveals a clear preference for short-form video and visual-heavy platforms. 
* **Dominance:** TikTok and Instagram combined represent nearly **70%** of the user base.
* **Secondary Usage:** Threads (16.6%) and Pinterest (14.9%) follow as niche interests.
""")

# ======================================================
# SECTION B
# ======================================================
st.divider()
st.header("Section B: Engagement Relationships")

# ------------------------------------------------------
# CORRELATION HEATMAP
# ------------------------------------------------------
ordinal_cols = [
    col for col in df.columns
    if (col.startswith('Active_') or col.startswith('Freq_')) and col.endswith('_Ordinal')
]

social_df = df[ordinal_cols].apply(pd.to_numeric, errors='coerce')
corr_matrix = social_df.corr()

fig2 = px.imshow(
    corr_matrix,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale='RdBu_r',
    title="Correlation Heatmap of Social Media Engagement Metrics"
)

fig2.update_layout(xaxis_tickangle=-45)
fig2 = center_title(fig2)

st.plotly_chart(fig2, use_container_width=True)

st.info("""
    **Key Observations:**
    1. **Positive correlations** exist between activities on the same platforms such as higher activity on Instagram is correlated with higher engagement on Instagram-related tasks like reading posts.
    2. **Some behaviors,** like frequent sharing or commenting, show a positive correlation with various platforms such as commenting on posts correlates strongly with sharing posts or uploading pictures/videos).
    3. **Negative correlations** are observed between activities on different platforms, indicating that high activity on one platform might correlate with lower activity on others such as active Facebook usage negatively correlates with activity on other platforms like TikTok or Pinterest)
    """)


# ======================================================
# SECTION C: ACTIVITY LEVEL DISTRIBUTION
# ======================================================
st.divider()
st.header("Section C: Activity Level Distribution Across Platforms")

# 1. Configuration & Labels
activity_labels = {
    0: 'Very Active', 
    1: 'Active', 
    2: 'Sometimes Active', 
    3: 'Inactive'
}

# 2. Prepare Data for Grouped Bar Chart
# Identify the columns
ordinal_activity_cols = [col for col in df.columns if col.startswith('Active_') and col.endswith('_Ordinal')]

# Melt the dataframe from wide to long format
df_melted_activity = df.melt(
    value_vars=ordinal_activity_cols,
    var_name='Platform',
    value_name='Activity_Ordinal'
)

# Clean up Platform names and map labels
df_melted_activity['Platform'] = df_melted_activity['Platform'].str.replace('Active_', '').str.replace('_Ordinal', '')
df_melted_activity['Activity_Level'] = df_melted_activity['Activity_Ordinal'].map(activity_labels)

# Define order for consistent visualization (matching your request)
platform_order = ['Facebook', 'Threads', 'Instagram', 'Pinterest', 'Tiktok']
activity_order = ['Very Active', 'Active', 'Sometimes Active', 'Inactive']

# 3. Create the Plotly Grouped Bar Chart
# This replaces the Seaborn sns.countplot logic
fig_grouped = px.histogram(
    df_melted_activity,
    x='Platform',
    color='Activity_Level',
    barmode='group',
    category_orders={
        'Platform': platform_order,
        'Activity_Level': activity_order
    },
    color_discrete_sequence=px.colors.sequential.Viridis,
    title='Distribution of Social Media Activity Levels Across Platforms'
)

fig_grouped.update_layout(
    xaxis_title="Social Media Platform",
    yaxis_title="Number of Respondents",
    legend_title="Activity Level",
    template="plotly_white"
)

fig_grouped = center_title(fig_grouped)

# 4. Display the Chart
st.plotly_chart(fig_grouped, use_container_width=True)

# 5. Quick Insights Grid
st.markdown("### Platform Insights")
cols = st.columns(3)
insight_list = [
    ("Instagram", "Top-tier fashion hub with balanced high-engagement."),
    ("TikTok", "The powerhouse for viral content (63 'Very Active' users)."),
    ("Facebook", "Mainly 'Sometimes Active'; transitioned to a secondary platform."),
    ("Pinterest", "A 'Discovery' hub for planning and mood boarding."),
    ("Threads", "Highest 'Inactive' count; yet to be fully integrated by users."),
    ("YouTube", "Steady base for long-form reviews and documentaries.")
]

for i, (p_name, insight) in enumerate(insight_list):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"**{p_name}**")
            st.caption(insight)

# 6. Final Key Findings
st.info("""
**Key Findings:**
* **Dominant Platforms:** TikTok and Instagram are the clear leaders in fashion engagement, commanding the majority of high-activity responses.
* **Activity Patterns:** While TikTok drives high-intensity 'Very Active' usage, Pinterest and Facebook serve more as occasional or utility-based platforms.
""")
        
# ======================================================
# SECTION D: DISTRIBUTION OF FREQUENCY LEVELS
# ======================================================
st.divider()
st.header("Section D: Distribution of Frequency Levels")

# 1. Prepare Data for Box Plot
# Identify frequency columns (adjust keywords if your column names differ)
freq_cols = [col for col in df.columns if col.startswith('Freq_') and col.endswith('_Ordinal')]

# Melt the dataframe for categorical plotting
df_melted_freq = df.melt(
    value_vars=freq_cols,
    var_name='Activity_Type',
    value_name='Frequency_Level'
)

# Clean labels (e.g., 'Freq_Likes_Ordinal' -> 'Likes')
df_melted_freq['Activity_Type'] = df_melted_freq['Activity_Type'].str.replace('Freq_', '').str.replace('_Ordinal', '')

# 2. Interactive Filtering
st.markdown("Filter the activity types below to update the box plot visualization.")
all_activities = df_melted_freq['Activity_Type'].unique().tolist()
selected_activities = st.multiselect(
    'Select Activity Types:',
    options=all_activities,
    default=all_activities
)

filtered_df = df_melted_freq[df_melted_freq['Activity_Type'].isin(selected_activities)]

# 3. Create Plotly Box Plot
if not filtered_df.empty:
    # We use plotly express for a cleaner, interactive boxplot
    fig4 = px.box(
        filtered_df,
        x='Activity_Type',
        y='Frequency_Level',
        color='Activity_Type',
        color_discrete_sequence=px.colors.sequential.Viridis,
        title='Distribution of Social Media Activity Frequencies (Box Plot)'
    )

    fig4.update_layout(
        xaxis_title="Social Media Activity Type",
        yaxis_title="Frequency Level (Lower = More Frequent)",
        showlegend=False,
        template="plotly_white"
    )
    
    # Center the title using your helper function
    fig4 = center_title(fig4)
    
    st.plotly_chart(fig4, use_container_width=True)
    
    st.info("""
    **Understanding the Box Plot:**
    The chart above displays the spread of engagement frequencies. 
    * **The Box:** Represents the Interquartile Range (IQR) where the middle 50% of responses lie.
    * **The Line:** The horizontal line inside the box represents the **Median** frequency.
    * **Points:** Dots outside the whiskers indicate outliers or niche user behaviors.
    """)
    
else:
    st.warning("Please select at least one activity type to display the visualization.")
    
# ======================================================
# SECTION E
# ======================================================
st.divider()
st.header("Section E: Cross Platform Connection")

x_col = 'Active_Instagram_Ordinal'
y_col = 'Active_Tiktok_Ordinal'

try:
    import statsmodels
    t_line = "ols"
except ImportError:
    t_line = None

fig3 = px.scatter(
    df, 
    x=x_col, 
    y=y_col, 
    trendline=t_line, 
    opacity=0.6, 
    title='Relationship Between Instagram and TikTok Activity',
    labels={
        x_col: 'Instagram Activity (0=Very Active, 3=Inactive)',
        y_col: 'TikTok Activity (0=Very Active, 3=Inactive)'
    },
    # FIX: Use "plotly_white" instead of "whitegrid"
    template="plotly_white" 
)

# Apply red color to the regression line
if t_line == "ols":
    fig3.data[1].line.color = 'red'

# Style the layout and add the grid lines manually to match Seaborn
fig3.update_layout(
    xaxis=dict(dtick=1, showgrid=True, gridcolor='LightGray'),
    yaxis=dict(dtick=1, showgrid=True, gridcolor='LightGray')
)

fig3 = center_title(fig3)
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.info("""
**Interpretation:**
The scatter plot reveals a positive correlation between Instagram and TikTok activity. Users who are highly active on one platform tend to be active on the other, indicating a segment of "Power Users" who dominate fashion engagement across the ecosystem.
""")
