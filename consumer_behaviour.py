import streamlit as st

st.title("Consumer Behaviour")
st.write("Content will be added here.")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_platform_usage(df):
    """
    Calculates high-activity users across specific social media platforms
    and generates a donut chart comparison.
    """
    # 1. Configuration
    sns.set_style("whitegrid")
    
    # 0: Very Active, 1: Active
    most_used_levels = [0, 1]
    
    platforms_to_compare = [
        'Active_Pinterest_Ordinal',
        'Active_Tiktok_Ordinal',
        'Active_Instagram_Ordinal',
        'Active_Threads_Ordinal'
    ]

    # 2. Data Processing
    most_used_counts = {}

    for col in platforms_to_compare:
        if col in df.columns:
            # Filter for active users and count rows
            count = df[df[col].isin(most_used_levels)].shape[0]
            # Clean up the name for the chart (e.g., 'Active_Tiktok_Ordinal' -> 'Tiktok')
            platform_name = col.replace('Active_', '').replace('_Ordinal', '')
            most_used_counts[platform_name] = count
        else:
            print(f"Warning: Column '{col}' not found in DataFrame.")

    # 3. Visualization
    if not most_used_counts:
        print("No data available to create the comparison chart.")
        return

    usage_series = pd.Series(most_used_counts)
    
    plt.figure(figsize=(10, 7))
    
    # Creating the Donut Chart
    plt.pie(
        usage_series, 
        labels=usage_series.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=sns.color_palette("viridis", len(usage_series)),
        wedgeprops={'width': 0.4, 'edgecolor': 'w'}
    )

    plt.title('Market Share of Active Users by Platform', fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()

# Example usage (assuming 'df' is your existing DataFrame)
# plot_platform_usage(df)
