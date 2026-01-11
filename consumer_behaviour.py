import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Consumer Behaviour")
st.write("Content will be added here.")

def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv"
    return pd.read_csv(url)

df = load_data()

# --- YOUR LOGIC STARTS HERE ---

# Define activity levels that count as 'most used'
# 0: Very Active, 1: Active
most_used_levels = [0, 1]

# Columns for the specific platforms requested, now including Threads
platforms_to_compare = [
    'Active_Pinterest_Ordinal',
    'Active_Tiktok_Ordinal',
    'Active_Instagram_Ordinal',
    'Active_Threads_Ordinal'
]

# Dictionary to store counts of 'most used' for each platform
most_used_counts = {}

for col in platforms_to_compare:
    # Ensure df exists in your Streamlit app's scope
    if col in df.columns:
        # Count respondents who are 'Very Active' or 'Active'
        count = df[df[col].isin(most_used_levels)].shape[0]
        platform_name = col.replace('Active_', '').replace('_Ordinal', '')
        most_used_counts[platform_name] = count
    else:
        st.warning(f"Column '{col}' not found. Skipping.")

if most_used_counts:
    # Convert to pandas DataFrame for Plotly (Plotly prefers DataFrames over Series)
    usage_df = pd.DataFrame({
        'Platform': list(most_used_counts.keys()),
        'Count': list(most_used_counts.values())
    })

    # Create the Plotly donut chart (exact logic as your matplotlib wedgeprops)
    fig = px.pie(
        usage_df, 
        values='Count', 
        names='Platform', 
        title='Comparison of Most Used Social Media Platforms (Pinterest, TikTok, Instagram, Threads)',
        hole=0.4, # This creates the 'width' effect from your original code
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    # Clean up layout to match your tight_layout and title style
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)

    # STREAMLIT DISPLAY
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("No data available to create the comparison chart.")
    
# 1. Identify all ordinally encoded social media columns
ordinal_social_media_cols = [
    col for col in df.columns
    if (col.startswith('Active_') or col.startswith('Freq_')) and col.endswith('_Ordinal')
]

if ordinal_social_media_cols:
    # 2. Create DataFrame and force numeric types
    social_media_ordinal_df = df[ordinal_social_media_cols].apply(pd.to_numeric, errors='coerce')

    # 3. Calculate the correlation matrix
    correlation_matrix = social_media_ordinal_df.corr()

    # 4. Only generate the plot if the matrix actually has data
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

        # 5. The only thing that will appear in Streamlit
        st.plotly_chart(fig, use_container_width=True)

# Define the activity level mapping for labels
activity_labels = {
    0: 'Very Active',
    1: 'Active',
    2: 'Sometimes Active',
    3: 'Inactive'
}

# Identify all the ordinally encoded social media activity columns
ordinal_activity_cols = [col for col in df.columns if col.startswith('Active_') and col.endswith('_Ordinal')]

if not ordinal_activity_cols:
    st.write("No ordinal social media activity columns found to visualize.")
else:
    for col in ordinal_activity_cols:
        platform_name = col.replace('Active_', '').replace('_Ordinal', '')

        # Prepare the data: count occurrences of each level
        # We sort by index to ensure 0, 1, 2, 3 order
        counts = df[col].value_counts().sort_index().reset_index()
        counts.columns = [col, 'count']
        
        # Map the numeric levels to your custom labels
        counts['label'] = counts[col].map(activity_labels)

        # Create the Plotly Bar Chart
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

        # Apply formatting and centering
        fig.update_traces(textposition='outside')
        fig.update_layout(
            title={
                'text': f'Distribution of Activity Levels on {platform_name}',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_tickangle=-45,
            showlegend=False
        )

        # Output to Streamlit
        st.plotly_chart(fig, use_container_width=True)

st.write("--- Social Media Activity Visualizations Complete ---")
