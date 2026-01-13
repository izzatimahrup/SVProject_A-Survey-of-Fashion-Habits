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

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. DATA PREPARATION ---
# Identify the frequency columns (e.g., Freq_Read posts or articles_Ordinal)
frequency_cols = [
    col for col in df.columns 
    if col.startswith('Freq_') and col.endswith('_Ordinal')
]

# Create df_melted_frequency for the Box Plot
# We clean the names here so they match your 'frequency_insights' keys
df_melted_frequency = df.melt(
    value_vars=frequency_cols,
    var_name='Activity_Type',
    value_name='Frequency_Level'
)

# Clean the Activity_Type strings to match your labels/insights
df_melted_frequency['Activity_Type'] = df_melted_frequency['Activity_Type'].str.replace('Freq_', '').str.replace('_Ordinal', '').str.replace('_', ' ')

# --- 2. MAPPINGS ---
frequency_labels = {
    0: 'Never',
    1: 'Rarely',
    2: 'Sometimes',
    3: 'Often',
    4: 'Very often'
}

frequency_insights = {
    "Read posts or articles": "Reading posts is a core activity, with the majority of users (40) engaging 'Sometimes'. This indicates high passive consumption of fashion information across platforms.",
    "Watch videos": "Video consumption shows a heavy skew toward 'Very often' (52). This confirms that video-first content is the most effective medium for capturing fashion consumer attention.",
    "Comment on posts": "Interaction via comments is moderate, peaking at 'Sometimes' (33). However, a significant portion (over 50 combined) 'Rarely' or 'Never' comment, suggesting many users are 'lurkers'.",
    "Share posts or photos": "Sharing behavior is centralized around 'Sometimes' (36). Users are more likely to share content occasionally rather than on a daily basis, indicating a selective curation process.",
    "Upload pictures or videos": "Uploading is the least frequent active behavior, with most users falling into 'Rarely' (35) or 'Sometimes' (34). Only 8 respondents upload 'Very often', identifying a small group of content creators."
}

# --- 3. IN-PAGE FILTERING ---
st.subheader("Social Media Activity Frequency Analysis")

# Filter selection directly on page
selected_activities = st.multiselect(
    "Filter Activities:",
    options=list(frequency_insights.keys()),
    default=list(frequency_insights.keys())
)

# Apply Filter
filtered_df = df_melted_frequency[df_melted_frequency['Activity_Type'].isin(selected_activities)]

# --- 4. MAIN BOX PLOT ---
if not filtered_df.empty:
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    sns.boxplot(
        data=filtered_df,
        x='Activity_Type',
        y='Frequency_Level',
        hue='Activity_Type',
        palette='viridis',
        legend=False,
        # Ensure the order respects the selection
        order=[a for a in frequency_insights.keys() if a in selected_activities]
    )

    # Set Y-Axis labels to your custom frequency labels
    ax.set_yticks(list(frequency_labels.keys()))
    ax.set_yticklabels(list(frequency_labels.values()))
    
    plt.title('Distribution of Social Media Activity Frequencies (Box Plot)', fontsize=16)
    plt.xlabel('Social Media Activity Type', fontsize=12)
    plt.ylabel('Frequency Level', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    
    st.pyplot(fig)
else:
    st.warning("Please select at least one activity type.")

st.divider()

# --- 5. STRUCTURED INSIGHTS (Matching your Column Layout) ---
col1, col2 = st.columns(2)

for i, activity in enumerate(selected_activities):
    # Alternate between column 1 and column 2
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        # Display Insight in a Box
        with st.container(border=True):
            st.markdown(f"**Quick Insight: {activity}**")
            insight_text = frequency_insights.get(activity, "No specific analysis available.")
            st.write(insight_text)
        st.write("##") # Space between items

# --- 6. KEY FINDINGS ---
st.info("""
**Key Findings:**
* **Content Preference:** Video is the most effective medium, with the highest frequency of "Very often" engagement compared to static posts.
* **User Behavior:** Most consumers are "passive observers" who read and watch frequently but rarely upload their own content or comment.
""")
    
# ======================================================

# SECTION E

# ======================================================

st.divider()

st.header("Section E: Cross Platform Connection")

import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr

# --- 1. DATA PREPARATION ---
# List of ordinal columns for selection
activity_columns = [
    'Active_Instagram_Ordinal', 
    'Active_Tiktok_Ordinal', 
    'Active_Facebook_Ordinal', 
    'Active_Twitter_Ordinal'
]

# Ensure df is defined - using your existing dataframe
# (Assuming df contains the ordinal columns)

# --- 2. UI LAYOUT: FILTERS ---
st.subheader("Relationship Scatters")

# Create two columns for the selectors to look structured
col_select1, col_select2 = st.columns(2)

with col_select1:
    x_axis_label = st.selectbox("Select X-axis", options=activity_columns, index=0)

with col_select2:
    y_axis_label = st.selectbox("Select Y-axis", options=activity_columns, index=1)

# --- 3. DYNAMIC ANALYSIS (Correlation) ---
# Calculate correlation coefficient for the selected axes
corr_value, _ = pearsonr(df[x_axis_label], df[y_axis_label])

# Determine relationship strength for the insight box
if abs(corr_value) > 0.7:
    strength = "Strong Relationship"
    color = "green"
elif abs(corr_value) > 0.4:
    strength = "Moderate Relationship"
    color = "orange"
else:
    strength = "Weak Relationship"
    color = "gray"

# --- 4. VISUALIZATION ---
try:
    import statsmodels
    t_line = "ols"
except ImportError:
    t_line = None

fig3 = px.scatter(
    df, 
    x=x_axis_label, 
    y=y_axis_label, 
    trendline=t_line, 
    opacity=0.6, 
    title=f'Relationship: {x_axis_label.replace("_", " ")} vs {y_axis_label.replace("_", " ")}',
    labels={
        x_axis_label: f'{x_axis_label.replace("_", " ")} (0=Very Active, 3=Inactive)',
        y_axis_label: f'{y_axis_label.replace("_", " ")} (0=Very Active, 3=Inactive)'
    },
    template="plotly_white" 
)

# Apply red color to the regression line to match your style
if t_line == "ols":
    fig3.data[1].line.color = 'red'

fig3.update_layout(
    xaxis=dict(dtick=1, showgrid=True, gridcolor='LightGray'),
    yaxis=dict(dtick=1, showgrid=True, gridcolor='LightGray')
)

# Center the title (using your existing function)
if 'center_title' in globals():
    fig3 = center_title(fig3)

# --- 5. DISPLAY CHART AND INSIGHT BOX ---
col_chart, col_insight = st.columns([2, 1])

with col_chart:
    st.plotly_chart(fig3, use_container_width=True)

with col_insight:
    st.write(f"**Correlation Coefficient:** {corr_value:.2f}")
    
    # Matching the green analysis box from your screenshot
    st.success(f"""
    **Analysis: {strength}.** These two platforms are linked in the consumer's digital behavior.
    """)

st.divider()
st.info("""
**Interpretation:**
The scatter plot reveals the connection between different platforms. Users who are highly active on one platform often exhibit similar patterns on others, helping identify cross-platform "Power Users."
""")
