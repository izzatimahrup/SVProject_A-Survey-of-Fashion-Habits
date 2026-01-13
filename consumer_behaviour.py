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

def show_consumer_behavior_page(df):
    st.header("🛍️ Consumer Behavior Analysis")
    st.markdown("This section explores how users interact with content, ranging from passive consumption to active creation.")

    # --- 1. DATA PRE-PROCESSING ---
    # Convert wide survey data to long format for Plotly
    ordinal_cols = [c for c in df.columns if c.startswith('Freq_') and c.endswith('_Ordinal')]
    
    df_melted = df.melt(
        id_vars=[c for c in df.columns if c not in ordinal_cols],
        value_vars=ordinal_cols,
        var_name='Activity_Type',
        value_name='Frequency_Level'
    )
    
    # Clean the activity names for the UI
    df_melted['Activity_Type'] = df_melted['Activity_Type'].str.replace('Freq_', '').str.replace('_Ordinal', '').str.replace('_', ' ')

    # --- 2. CONFIGURATION ---
    frequency_labels = {0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Very often'}
    frequency_insights = {
        "Read posts or articles": "Reading posts is a core activity, indicating high passive consumption of information.",
        "Watch videos": "Video consumption shows a heavy skew toward 'Very often', confirming video as the top medium.",
        "Comment on posts": "Interaction via comments is moderate; many users remain 'lurkers'.",
        "Share posts or photos": "Sharing is selective; users curate content before spreading it.",
        "Upload pictures or videos": "The least frequent behavior, identifying a small group of creators."
    }

    # --- 3. IN-PAGE FILTER SECTION ---
    # Using a container with a background (border) to separate filters from results
    with st.container(border=True):
        st.subheader("Filter Behavior Data")
        row1_col1, row1_col2 = st.columns([2, 1])
        
        with row1_col1:
            selected_activities = st.multiselect(
                "Select Social Media Activities",
                options=sorted(df_melted['Activity_Type'].unique()),
                default=["Read posts or articles", "Watch videos"]
            )
            
        with row1_col2:
            chart_type = st.segmented_control(
                "Visualization Style",
                options=["Box Plot", "Bar Chart"],
                default="Box Plot"
            )

    st.write("##") # Spacer

    # --- 4. VISUALIZATION GENERATOR ---
    if not selected_activities:
        st.info("Select activities above to view frequency distributions.")
    else:
        # Loop through selected activities and create a 2-column grid
        for i in range(0, len(selected_activities), 2):
            cols = st.columns(2)
            
            for j in range(2):
                if i + j < len(selected_activities):
                    activity = selected_activities[i + j]
                    plot_data = df_melted[df_melted['Activity_Type'] == activity].copy()
                    plot_data['Frequency_Label'] = plot_data['Frequency_Level'].map(frequency_labels)
                    
                    with cols[j]:
                        if chart_type == "Box Plot":
                            # 

[Image of a box plot with data points]

                            fig = px.box(
                                plot_data, 
                                x='Frequency_Label', 
                                y='Frequency_Level',
                                points="all",
                                title=f"Spread: {activity}",
                                category_orders={"Frequency_Label": list(frequency_labels.values())},
                                color_discrete_sequence=['#1f77b4']
                            )
                        else:
                            # 
                            counts = plot_data['Frequency_Label'].value_counts().reindex(list(frequency_labels.values()), fill_value=0).reset_index()
                            counts.columns = ['Label', 'Count']
                            fig = px.bar(
                                counts, x='Label', y='Count', text='Count',
                                title=f"Volume: {activity}",
                                color='Count', 
                                color_continuous_scale='Blues'
                            )

                        fig.update_layout(height=400, margin=dict(t=50, b=20, l=10, r=10))
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Insight Box
                        with st.expander(f"Analysis for {activity}", expanded=True):
                            st.write(frequency_insights.get(activity, "General behavior patterns observed."))

    # --- 5. SECTION SUMMARY ---
    st.divider()
    st.markdown("### 💡 Key Behavioral Findings")
    st.success("""
    * **Passive Dominance:** Consumers are far more likely to 'Watch' and 'Read' than to 'Post' or 'Comment'.
    * **The Creator Gap:** Only a small percentage of users reach the 'Very Often' threshold for uploading original content.
    """)

# To call this from your main app script:
# if page == "Consumer Behavior":
#     show_consumer_behavior_page(df)
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
