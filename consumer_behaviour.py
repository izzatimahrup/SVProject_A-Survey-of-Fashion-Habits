import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE TITLE (CENTERED)
# ======================================================
st.markdown(
    "<h1 style='text-align: center;'>Consumer Behaviour</h1>",
    unsafe_allow_html=True
)

st.write("Content will be added here.")

# ======================================================
# LOAD DATA (SAFE FOR STREAMLIT CLOUD)
# ======================================================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/main/Cleaned_FashionHabitGF%20(1).csv"
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error("Failed to load data from GitHub.")
        st.exception(e)
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# ======================================================
# DONUT CHART: MOST USED SOCIAL MEDIA PLATFORMS
# ======================================================
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
    else:
        st.warning(f"Column '{col}' not found. Skipping.")

if most_used_counts:
    usage_df = pd.DataFrame({
        'Platform': list(most_used_counts.keys()),
        'Count': list(most_used_counts.values())
    })

    fig = px.pie(
        usage_df,
        values='Count',
        names='Platform',
        title='Comparison of Most Used Social Media Platforms (Pinterest, TikTok, Instagram, Threads)',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No data available to create the comparison chart.")

# ======================================================
# CORRELATION HEATMAP
# ======================================================
ordinal_social_media_cols = [
    col for col in df.columns
    if (col.startswith('Active_') or col.startswith('Freq_')) and col.endswith('_Ordinal')
]

if ordinal_social_media_cols:
    social_media_ordinal_df = df[ordinal_social_media_cols].apply(pd.to_numeric, errors='coerce')
    correlation_matrix = social_media_ordinal_df.corr()

    if not (correlation_matrix.empty or correlation_matrix.isnull().all().all()):
        fig = px.imshow(
            correlation_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title='Correlation Heatmap of Ordinal Social Media Engagement Metrics'
        )

        fig.update_layout(
            width=900,
            height=700,
            title_x=0.5,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig, use_container_width=True)

# ======================================================
# BAR CHARTS: DISTRIBUTION OF ACTIVITY LEVELS
# ======================================================
activity_labels = {
    0: 'Very Active',
    1: 'Active',
    2: 'Sometimes Active',
    3: 'Inactive'
}

ordinal_activity_cols = [
    col for col in df.columns
    if col.startswith('Active_') and col.endswith('_Ordinal')
]

if not ordinal_activity_cols:
    st.info("No ordinal social media activity columns found to visualize.")
else:
    for col in ordinal_activity_cols:
        platform_name = col.replace('Active_', '').replace('_Ordinal', '')

        counts = df[col].value_counts().sort_index().reset_index()
        counts.columns = [col, 'count']
        counts['label'] = counts[col].map(activity_labels)

        fig = px.bar(
            counts,
            x='label',
            y='count',
            text='count',
            title=f'Distribution of Activity Levels on {platform_name}',
            labels={'label': 'Activity Level', 'count': 'Number of Respondents'},
            color='count',
            color_continuous_scale='Viridis'
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(
            title_x=0.5,
            xaxis_tickangle=-45,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )

        st.plotly_chart(fig, use_container_width=True)

st.write("--- Social Media Activity Visualizations Complete ---")
