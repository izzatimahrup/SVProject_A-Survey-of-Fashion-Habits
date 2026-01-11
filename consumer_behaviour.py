import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Consumer Behaviour")
st.write("Content will be added here.")

def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv"
    return pd.read_csv(url)

df = load_data()
uploaded_file = st.file_uploader("Upload your Social Media CSV", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
sns.set_style("whitegrid")

    # Define activity levels that count as 'most used'
    # 0: Very Active, 1: Active
    most_used_levels = [0, 1]

    # Columns for the specific platforms requested, now including Threads
    platforms_to_compare = [
        'Active_Pinterest_Ordinal',
        'Active_Tiktok_Ordinal',
        'Active_Instagram_Ordinal',
        'Active_Threads_Ordinal' # Added Threads
    ]

    # Dictionary to store counts of 'most used' for each platform
    most_used_counts = {}

    for col in platforms_to_compare:
        if col in df.columns:
            # Count respondents who are 'Very Active' or 'Active'
            count = df[df[col].isin(most_used_levels)].shape[0]
            platform_name = col.replace('Active_', '').replace('_Ordinal', '')
            most_used_counts[platform_name] = count
        else:
            st.warning(f"Warning: Column '{col}' not found. Skipping.")

    if most_used_counts:
        # Convert to pandas Series for easier plotting
        usage_series = pd.Series(most_used_counts)

        fig, ax = plt.subplots(figsize=(8, 8)) # Streamlit works best with fig, ax
        ax.pie(usage_series, labels=usage_series.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
        plt.title('Comparison of Most Used Social Media Platforms (Pinterest, TikTok, Instagram, Threads)', fontsize=16)
        plt.tight_layout()
        
        # --- STREAMLIT SPECIFIC OUTPUT ---
        st.pyplot(fig) 
        # --- END OF YOUR EXACT CODE ---
        
    else:
        st.error("No data available to create the comparison pie chart.")

else:
    st.info("Please upload a CSV file to generate the visualization.")
