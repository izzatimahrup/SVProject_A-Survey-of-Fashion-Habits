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

# 1. Column Selection Logic
ordinal_social_media_cols = [
    col for col in df.columns
    if (col.startswith('Active_') or col.startswith('Freq_')) and col.endswith('_Ordinal')
]

# DEBUG: Check if columns were actually found
if not ordinal_social_media_cols:
    st.error("❌ No columns found! Check your CSV headers.")
    st.write("Your CSV has these columns:", list(df.columns))
else:
    # 2. Data Cleaning (Force numbers)
    # This ensures correlations can be calculated even if data looks like strings
    social_media_ordinal_df = df[ordinal_social_media_cols].apply(pd.to_numeric, errors='coerce')

    # 3. Calculate Correlation
    correlation_matrix = social_media_ordinal_df.corr()

        # 4. Generate Plotly Heatmap
        fig = px.imshow(
            correlation_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title='Correlation Heatmap of Social Media Engagement'
        )

        fig.update_layout(
            width=800, 
            height=800,
            xaxis_tickangle=-45
        )

        # 5. THE OUTPUT COMMAND
        # If this line runs, the chart MUST appear
        st.plotly_chart(fig, use_container_width=True)

st.write("--- Process Finished ---")
