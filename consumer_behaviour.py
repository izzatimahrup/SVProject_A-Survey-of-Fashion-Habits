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
st.markdown(
    "This dashboard presents an analysis of social media engagement patterns "
    "and consumer behaviour based on survey data."
)

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

# ======================================================
# SECTION C
# ======================================================
st.divider()
st.header("Section C: Activity Level Distribution")

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

# Display charts in 2 columns like reference
col1, col2 = st.columns(2)

for i, col in enumerate(ordinal_activity_cols):
    platform_name = col.replace('Active_', '').replace('_Ordinal', '')

    counts = df[col].value_counts().sort_index().reset_index()
    counts.columns = [col, 'count']
    counts['label'] = counts[col].map(activity_labels)

    fig = px.bar(
        counts,
        x='label',
        y='count',
        text='count',
        title=f"Distribution of Activity Levels on {platform_name}",
        labels={'label': 'Activity Level', 'count': 'Number of Respondents'}
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    fig = center_title(fig)

    if i % 2 == 0:
        col1.plotly_chart(fig, use_container_width=True)
    else:
        col2.plotly_chart(fig, use_container_width=True)

# ======================================================
# SECTION D
# ======================================================
st.divider()
st.header("Section D: Distribution of Frequency Levels")

frequency_labels = {
    0: 'Never',
    1: 'Rarely',
    2: 'Sometimes',
    3: 'Often',
    4: 'Very often'
}

ordinal_frequency_cols = [
    col for col in df.columns 
    if col.startswith('Freq_') and col.endswith('_Ordinal')
]

# Display charts in 2 columns like reference
col1, col2 = st.columns(2)

if not ordinal_frequency_cols:
    st.info("No ordinal social media frequency columns found to visualize.")
else:
    for i, col in enumerate(ordinal_Frequency_cols):
        platform_name = col.replace('Freq_', '').replace('_Ordinal', '')

        counts = df[col].value_counts().sort_index().reset_index()
        counts.columns = [col, 'count']
        counts['label'] = counts[col].map(frequency_labels)

        fig = px.bar(
            counts,
            x='label',
            y='count',
            text='count',
            title=f"Frequency of '{platform_name}' on Social Media",
            labels={'label': 'Frequency Level', 'count': 'Number of Respondents'},
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False)
        fig = center_title(fig)

    if i % 2 == 0:
        col1.plotly_chart(fig, use_container_width=True)
    else:
        col2.plotly_chart(fig, use_container_width=True)


st.divider()
st.markdown("✔ **Social Media Activity Visualizations Complete**")
