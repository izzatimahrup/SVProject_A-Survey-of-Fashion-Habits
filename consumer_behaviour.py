import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Consumer Behaviour")
st.write("Content will be added here.")

def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv"
    return pd.read_csv(url)

df = load_data()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.title("Social Media Usage Visualization")

# Assuming 'df' is loaded from a CSV or passed from a session state
# If you are using a file uploader in your main app:
if 'df' in st.session_state:
    df = st.session_state['df']
else:
    # Fallback for testing: allow local upload if df isn't in state
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = None

if df is not None:
    sns.set_style("whitegrid")

    # 1. Define activity levels
    most_used_levels = [0, 1]

    # 2. Define platforms
    platforms_to_compare = [
        'Active_Pinterest_Ordinal',
        'Active_Tiktok_Ordinal',
        'Active_Instagram_Ordinal',
        'Active_Threads_Ordinal'
    ]

    # 3. Calculate counts
    most_used_counts = {}

    for col in platforms_to_compare:
        if col in df.columns:
            count = df[df[col].isin(most_used_levels)].shape[0]
            platform_name = col.replace('Active_', '').replace('_Ordinal', '')
            most_used_counts[platform_name] = count

    # 4. Visualization
    if most_used_counts:
        usage_series = pd.Series(most_used_counts)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            usage_series, 
            labels=usage_series.index, 
            autopct='%1.1f%%', 
            startangle=90, 
            wedgeprops={'width': 0.4}
        )
        ax.set_title('Most Used Social Media Platforms')
        
        # Display in Streamlit
        st.pyplot(fig)
    else:
        st.error("No data found for the selected platforms.")
