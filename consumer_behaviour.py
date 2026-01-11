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

st.set_page_config(page_title="Social Media Analyzer", layout="centered")

st.title("📊 Social Media Activity Tracker")

# 1. File Upload
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # 2. Configuration & Data Cleaning
    most_used_levels = [0, 1]
    platforms_to_compare = [
        'Active_Pinterest_Ordinal',
        'Active_Tiktok_Ordinal',
        'Active_Instagram_Ordinal',
        'Active_Threads_Ordinal'
    ]

    # Debug: Show found columns
    found_cols = [c for c in platforms_to_compare if c in df.columns]
    
    if not found_cols:
        st.error(f"❌ None of the required columns were found. Found: {list(df.columns)}")
    else:
        # 3. Processing Data
        plot_data = []
        for col in found_cols:
            # Filter for active users
            count = df[df[col].isin(most_used_levels)].shape[0]
            platform_name = col.replace('Active_', '').replace('_Ordinal', '')
            plot_data.append({'Platform': platform_name, 'Count': count})

        usage_df = pd.DataFrame(plot_data)

        # 4. Final Check and Render
        total_active = usage_df['Count'].sum()
        
        if total_active == 0:
            st.warning("⚠️ The columns exist, but no users matched the 'Active' criteria (0 or 1).")
            st.write("Data Preview for active columns:")
            st.write(df[found_cols].head())
        else:
            # Create the chart
            fig = px.pie(
                usage_df, 
                values='Count', 
                names='Platform', 
                hole=0.5,
                title="Distribution of Active Users",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            
            # This is the specific command to show in Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
            # Show a summary table below
            st.table(usage_df)

else:
    st.info("👋 Please upload a CSV file to begin.")
