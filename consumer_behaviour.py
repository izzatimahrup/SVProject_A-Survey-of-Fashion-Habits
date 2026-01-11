import streamlit as st

st.title("Consumer Behaviour")
st.write("Content will be added here.")

import pandas as pd
import plotly.express as px
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv"
    return pd.read_csv(url)

df = load_data()

def plot_platform_usage_plotly(df):
    """
    Calculates high-activity users across social media platforms 
    and generates an interactive Plotly donut chart.
    """
    # 1. Configuration
    # 0: Very Active, 1: Active
    most_used_levels = [0, 1]
    
    platforms_to_compare = [
        'Active_Pinterest_Ordinal',
        'Active_Tiktok_Ordinal',
        'Active_Instagram_Ordinal',
        'Active_Threads_Ordinal'
    ]

    # 2. Data Processing
    plot_data = []

    for col in platforms_to_compare:
        if col in df.columns:
            # Count respondents who are 'Very Active' or 'Active'
            count = df[df[col].isin(most_used_levels)].shape[0]
            # Clean name for the chart
            platform_name = col.replace('Active_', '').replace('_Ordinal', '')
            plot_data.append({'Platform': platform_name, 'Active_Users': count})
        else:
            print(f"Warning: Column '{col}' not found.")

    if not plot_data:
        print("No data available to create the comparison chart.")
        return

    # Convert results to a DataFrame for Plotly Express
    usage_df = pd.DataFrame(plot_data)

    # 3. Visualization
    fig = px.pie(
        usage_df, 
        values='Active_Users', 
        names='Platform', 
        title='Comparison of Most Used Social Media Platforms',
        hole=0.4,  # Creates the donut shape
        color_discrete_sequence=px.colors.qualitative.Prism # Professional color palette
    )

    # Enhancing the layout for a clean GitHub/Portfolio look
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )

    fig.update_layout(
        title_x=0.5, # Center the title
        margin=dict(t=50, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )

    fig.show()

# To use this with your data:
# plot_platform_usage_plotly(df)
    plt.tight_layout()
    plt.show()

# Example usage (assuming 'df' is your existing DataFrame)
# plot_platform_usage(df)
