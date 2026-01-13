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

# --- 1. DATA MAPPING & CONFIGURATION ---
frequency_labels = {
    0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Very often'
}
frequency_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']

def show_consumer_behavior_page(df):
    st.header("📊 Consumer Behavior: Activity Distribution")
    st.markdown("Analyze the statistical significance of user engagement and respondent volume.")

    # --- 2. DEFINE df_melted_frequency ---
    # We identify columns that follow your naming convention: Freq_ActivityName_Ordinal
    ordinal_cols = [c for c in df.columns if c.startswith('Freq_') and c.endswith('_Ordinal')]
    
    if not ordinal_cols:
        st.error("Missing data: Please ensure your columns are named 'Freq_ActivityName_Ordinal'.")
        return

    # Melting the dataframe from Wide to Long format
    df_melted_frequency = df.melt(
        id_vars=[c for c in df.columns if c not in ordinal_cols],
        value_vars=ordinal_cols,
        var_name='Activity_Type',
        value_name='Frequency_Level'
    )

    # Clean the activity names for better UI display
    df_melted_frequency['Activity_Type'] = (
        df_melted_frequency['Activity_Type']
        .str.replace('Freq_', '', regex=False)
        .str.replace('_Ordinal', '', regex=False)
        .str.replace('_', ' ', regex=False)
    )

    # Map the numeric codes to their readable labels
    df_melted_frequency['Frequency_Label'] = df_melted_frequency['Frequency_Level'].map(frequency_labels)

    # --- 3. STRUCTURED FILTRATION PANEL ---
    with st.container(border=True):
        st.subheader("🛠️ Analysis Controls")
        f_col1, f_col2 = st.columns([2, 1])
        
        with f_col1:
            all_activities = sorted(df_melted_frequency['Activity_Type'].unique())
            selected_activities = st.multiselect(
                "Select Activities to Compare:",
                options=all_activities,
                default=all_activities[:2]
            )
        
        with f_col2:
            view_mode = st.radio(
                "Select Analysis Depth:",
                ["Statistical (Notched Box)", "Volume (Respondent Count)"]
            )

    st.divider()

    # --- 4. DYNAMIC VISUALIZATION GRID ---
    if not selected_activities:
        st.info("Please select at least one activity from the filters above.")
    else:
        # Create a 2-column layout for the charts
        grid_col1, grid_col2 = st.columns(2)
        
        for i, activity in enumerate(selected_activities):
            # Filter data for the specific loop item
            plot_df = df_melted_frequency[df_melted_frequency['Activity_Type'] == activity].dropna()
            total_n = len(plot_df)
            
            if "Statistical" in view_mode:
                # 
                fig = px.box(
                    plot_df,
                    y='Frequency_Label',
                    points="outliers",
                    notched=True, # Added for statistical significance
                    title=f"Distribution: {activity} (n={total_n})",
                    category_orders={"Frequency_Label": frequency_order},
                    color='Frequency_Label',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    labels={'Frequency_Label': 'Respondent Frequency'}
                )
                # Keep 'Never' at the top for intuitive reading
                fig.update_yaxes(autorange="reversed")
            
            else:
                # 
                counts = plot_df['Frequency_Label'].value_counts().reindex(frequency_order, fill_value=0).reset_index()
                counts.columns = ['Frequency', 'Respondents']
                
                fig = px.bar(
                    counts,
                    x='Frequency',
                    y='Respondents',
                    text='Respondents',
                    title=f"Total Respondents: {activity}",
                    color='Respondents',
                    color_continuous_scale='Viridis',
                    labels={'Respondents': 'Number of Respondents'}
                )
                fig.update_traces(textposition='outside')

            # Clean styling to match 'whitegrid' look
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                height=450,
                margin=dict(t=50, b=20, l=10, r=10)
            )
            fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
            fig.update_xaxes(showgrid=False)

            # Alternate placement in the grid
            target_col = grid_col1 if i % 2 == 0 else grid_col2
            
            with target_col:
                st.plotly_chart(fig, use_container_width=True)
                
                # Insight Box for each chart
                with st.container(border=True):
                    st.markdown(f"**Quick Stats: {activity}**")
                    st.write(f"This dataset contains **{total_n}** unique respondent entries.")
                st.write("##")

    # --- 5. SUMMARY SECTION ---
    st.info("""
    **Understanding the Significance:**
    * **Notched Box Plots:** The 'notches' indicate the confidence interval around the median. If notches from different activities don't overlap, the difference is statistically significant.
    * **Respondent Counts:** The bar charts show the exact volume of individuals in each category, helping identify the 'Lurker' vs 'Creator' gap.
    """)

# Call the function (assuming 'df' is your pre-loaded dataframe)
show_consumer_behavior_page(df)

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
