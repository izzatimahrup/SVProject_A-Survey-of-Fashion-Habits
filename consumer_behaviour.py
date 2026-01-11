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
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Social Media Usage Tracker", layout="wide")

st.title("📱 Social Media Activity Dashboard")
st.markdown("This app visualizes high-activity users across Pinterest, TikTok, Instagram, and Threads.")

def plot_usage(df):
    # --- Data Logic ---
    most_used_levels = [0, 1]
    platforms_to_compare = [
        'Active_Pinterest_Ordinal',
        'Active_Tiktok_Ordinal',
        'Active_Instagram_Ordinal',
        'Active_Threads_Ordinal'
    ]

    plot_data = []
    for col in platforms_to_compare:
        if col in df.columns:
            count = df[df[col].isin(most_used_levels)].shape[0]
            platform_name = col.replace('Active_', '').replace('_Ordinal', '')
            plot_data.append({'Platform': platform_name, 'Active_Users': count})

    usage_df = pd.DataFrame(plot_data)

    if usage_df.empty or usage_df['Active_Users'].sum() == 0:
        st.error("No active user data found. Please check your dataset.")
        return

    # --- Plotly Visualization ---
    fig = px.pie(
        usage_df, 
        values='Active_Users', 
        names='Platform', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    
    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# 2. Sidebar for Data Input
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Show Raw Data Preview
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

    # Generate Chart
    st.subheader("Platform Usage Comparison")
    plot_usage(df)
else:
    st.info("Please upload a CSV file via the sidebar to see the visualization.")
    st.warning("Ensure your CSV contains columns like: 'Active_Tiktok_Ordinal', etc.")
