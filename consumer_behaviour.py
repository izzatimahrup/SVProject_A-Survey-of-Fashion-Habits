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


# 1. Configuration
activity_labels = {
    0: 'Very Active', 
    1: 'Active', 
    2: 'Sometimes Active', 
    3: 'Inactive'
}

interpretations = {
    "Instagram": "Instagram is a top-tier fashion hub, showing the most balanced high-engagement profile. With roughly 35 'Very Active' and 37 'Active' users, it serves as the consistent daily 'go-to' platform for broad fashion inspiration.",
    "TikTok": "TikTok dominates high-intensity engagement, with a massive 63 respondents identifying as 'Very Active.' It is the clear powerhouse for viral fashion content and fast-paced consumer trends.",
    "Facebook": "Facebook peaks at 42 'Sometimes Active' users. It has transitioned into a secondary platform where users check for community updates rather than daily trends.",
    "Pinterest": "Pinterest is a 'Discovery' hub with 41 'Sometimes Active' users. It serves as a digital mood board for planning future purchases rather than immediate interaction.",
    "Threads": "Threads has the highest 'Inactive' count (36). While linked to Instagram, many users have yet to integrate it into their daily fashion browsing habits.",
    "YouTube": "YouTube maintains a steady 'Active' base. It remains the go-to for long-form content, such as deep-dive brand reviews and sustainable fashion documentaries."
}

# 2. Identify Columns
ordinal_activity_cols = [col for col in df.columns if col.startswith('Active_') and col.endswith('_Ordinal')]

st.header("Section C: Activity Level Distribution")

# 3. Create Columns for Layout
c1, c2 = st.columns(2)

# 4. Loop for Charts and Insights
for i, col in enumerate(ordinal_activity_cols):
    p_name = col.replace('Active_', '').replace('_Ordinal', '')
    
    # Data aggregation
    counts = df[col].value_counts().sort_index().reset_index()
    counts.columns = [col, 'count']
    counts['label'] = counts[col].map(activity_labels)
    
    # Chart Creation
    fig = px.bar(
        counts, 
        x='label', 
        y='count', 
        text='count', 
        title=f"Activity: {p_name}",
        template="plotly_white"
    )
    fig.update_traces(textposition='outside', marker_color='#0068c9')
    fig.update_layout(margin=dict(b=20), showlegend=False)
    
    # Alternate between columns
    target = c1 if i % 2 == 0 else c2
    
    with target:
        st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            st.markdown(f"**Quick Insight: {p_name}**")
            st.write(interpretations.get(p_name, "TikTok dominates high-intensity engagement, with a massive 63 respondents identifying as 'Very Active.' It is the clear powerhouse for viral fashion content and fast-paced consumer trends."))
        st.write("##")

# 5. Final Key Findings (Bottom of Section C)
st.info("""
**Key Findings:**
* **Dominant Platforms:** TikTok and Instagram are the clear leaders in fashion engagement, commanding nearly **70%** of user preference.
* **Activity Patterns:** TikTok has the highest **'Very Active'** intensity (63 respondents), while Facebook and Pinterest have shifted toward occasional usage.
""")
        
# ======================================================
# SECTION D
# ======================================================
st.divider()
st.header("Section D: Distribution of Frequency Levels")

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETUP & CONFIGURATION
frequency_labels = {
    0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Very often'
}
frequency_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']

frequency_insights = {
    "Read posts or articles": "Reading posts is a core activity, with the majority of users (40) engaging 'Sometimes'. This indicates high passive consumption of fashion information across platforms.",
    "Watch videos": "Video consumption shows a heavy skew toward 'Very often' (52). This confirms that video-first content is the most effective medium for capturing fashion consumer attention.",
    "Comment on posts": "Interaction via comments is moderate, peaking at 'Sometimes' (33). However, a significant portion (over 50 combined) 'Rarely' or 'Never' comment, suggesting many users are 'lurkers'.",
    "Share posts or photos": "Sharing behavior is centralized around 'Sometimes' (36). Users are more likely to share content occasionally rather than on a daily basis, indicating a selective curation process.",
    "Upload pictures or videos": "Uploading is the least frequent active behavior, with most users falling into 'Rarely' (35) or 'Sometimes' (34). Only 8 respondents upload 'Very often', identifying a small group of content creators."
}

def show_consumer_behavior_page(df, activity_counts):
    st.header("🛒 Consumer Behavior: Platform Activity & Engagement")

    # --- 2. STRUCTURED FILTER SECTION ---
    with st.container(border=True):
        st.subheader("Dashboard Controls")
        f_col1, f_col2 = st.columns([2, 1])
        
        with f_col1:
            # Multi-select for detailed activity filtering
            ordinal_cols = [c for c in df.columns if c.startswith('Freq_') and c.endswith('_Ordinal')]
            activity_map = {c.replace('Freq_', '').replace('_Ordinal', '').replace('_', ' '): c for c in ordinal_cols}
            
            selected_activities = st.multiselect(
                "Select Specific Activities to Analyze",
                options=list(activity_map.keys()),
                default=list(activity_map.keys())[:2]
            )

        with f_col2:
            # Toggle for visual style
            view_type = st.radio("Visualization Style", ["Box Plot (Spread)", "Bar Chart (Count)"], horizontal=True)

    # --- 3. GLOBAL TREEMAP VIEW ---
    st.subheader("Proportion of Social Media Activity Levels Across Platforms")
    
    # Pre-processing for Treemap to avoid FutureWarning
    activity_counts_for_plot = activity_counts.copy()
    activity_counts_for_plot['Platform'] = activity_counts_for_plot['Platform'].astype(str)
    activity_counts_for_plot['Activity_Level'] = activity_counts_for_plot['Activity_Level'].astype(str)

    fig_tree = px.treemap(
        activity_counts_for_plot,
        path=[px.Constant("All Platforms"), 'Platform', 'Activity_Level'],
        values='Percentage',
        color='Activity_Level',
        color_discrete_map={
            '(?)': 'lightgrey',
            'very active': '#1a9850', 
            'active': '#91cf60', 
            'sometimes active': '#ffffbf', 
            'inactive': '#fc8d59'
        },
        labels={'Platform': 'Social Media Platform', 'Activity_Level': 'Activity Level', 'Percentage': 'Percentage of Users'},
        hover_data={'Count': True, 'Percentage': ':.2f'}
    )
    fig_tree.update_layout(margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig_tree, use_container_width=True)
    
    st.divider()

    # --- 4. DETAILED ACTIVITY ANALYSIS ---
    if not selected_activities:
        st.info("Select specific activities above to view detailed engagement distributions.")
    else:
        col1, col2 = st.columns(2)
        
        for i, activity_name in enumerate(selected_activities):
            orig_col = activity_map[activity_name]
            plot_df = df[[orig_col]].copy()
            plot_df['Label'] = plot_df[orig_col].map(frequency_labels)

            if "Box Plot" in view_type:
                # Vertical Box Plot with Viridis palette to match requested style
                fig = px.box(
                    plot_df,
                    y='Label',
                    points="outliers",
                    title=f"Distribution: {activity_name}",
                    category_orders={"Label": frequency_order},
                    color='Label',
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                fig.update_yaxes(autorange="reversed", showgrid=True, gridcolor='lightgrey')
            else:
                counts = plot_df['Label'].value_counts().reindex(frequency_order, fill_value=0).reset_index()
                counts.columns = ['Label', 'count']
                fig = px.bar(
                    counts, x='Label', y='count', text='count',
                    title=f"Volume: {activity_name}",
                    color='count', color_continuous_scale='Blues'
                )
                fig.update_traces(textposition='outside')

            fig.update_layout(showlegend=False, plot_bgcolor='white', height=450, margin=dict(t=50, b=20))
            
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.plotly_chart(fig, use_container_width=True)
                with st.container(border=True):
                    st.markdown(f"**Quick Insight: {activity_name}**")
                    st.write(frequency_insights.get(activity_name, "N/A"))
                st.write("##")

    # --- 5. FINAL FINDINGS ---
    st.info("""
    **Key Findings:**
    * **Platform Dominance:** The Treemap highlights which platforms maintain the highest 'very active' user base.
    * **Passive vs Active:** Individual activity data confirms that video-first consumption is the most frequent user behavior.
    """)

# To call: show_consumer_behavior_page(df, activity_counts)
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
