import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Social Media Platform Analysis", layout="centered")

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

df = load_data()

# Title with better styling
st.markdown("<h1 style='text-align: center; color: #2E86AB; margin-bottom: 30px;'>Social Media Platform Engagement</h1>", unsafe_allow_html=True)

# --- CORE LOGIC ---
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

# Only proceed if we have data
if most_used_counts:
    # Create DataFrame
    usage_df = pd.DataFrame({
        'Platform': list(most_used_counts.keys()),
        'Count': list(most_used_counts.values())
    }).sort_values('Count', ascending=False)
    
    total = usage_df['Count'].sum()
    
    # Add percentage column
    usage_df['Percentage'] = (usage_df['Count'] / total * 100).round(1)
    
    # --- ENHANCED VISUALIZATION ---
    
    # Custom color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']  # Modern, vibrant colors
    
    # Create the donut chart with better styling
    fig = px.pie(
        usage_df, 
        values='Count', 
        names='Platform', 
        title='Most Used Social Media Platforms',
        hole=0.5,
        color_discrete_sequence=colors
    )
    
    # Enhanced traces
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                     "Active Users: %{value:,}<br>" +
                     "Percentage: %{percent:.1%}<br>" +
                     "<extra></extra>",
        textfont=dict(
            size=14,
            family="Arial, sans-serif",
            color="white"
        ),
        marker=dict(
            line=dict(
                color='white',
                width=3
            )
        ),
        pull=[0.03 if i == usage_df['Count'].idxmax() else 0 for i in range(len(usage_df))]  # Slight pull for top platform
    )
    
    # Perfectly centered title with better styling
    fig.update_layout(
        title={
            'text': '<b>Most Used Social Media Platforms</b><br><span style="font-size:14px; color:#666">Active Users Distribution</span>',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 24,
                'family': "Arial, sans-serif",
                'color': '#2E86AB'
            },
            'y': 0.95
        },
        showlegend=False,
        height=500,
        margin=dict(t=100, b=50, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        annotations=[
            dict(
                text=f'<b>Total<br>{total:,}<br>Users</b>',
                x=0.5,
                y=0.5,
                font=dict(size=16, color='#666'),
                showarrow=False
            )
        ]
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # --- ADDITIONAL MINI VISUALIZATION ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create a mini bar chart for quick comparison
    fig_bar = go.Figure()
    
    for i, (_, row) in enumerate(usage_df.iterrows()):
        fig_bar.add_trace(go.Bar(
            x=[row['Platform']],
            y=[row['Count']],
            name=row['Platform'],
            marker_color=colors[i],
            text=[f"{row['Count']:,}"],
            textposition='auto',
            hovertemplate=f"<b>{row['Platform']}</b><br>" +
                         f"Active Users: {row['Count']:,}<br>" +
                         f"Percentage: {row['Percentage']}%<extra></extra>"
        ))
    
    fig_bar.update_layout(
        title={
            'text': '<b>Platform Comparison</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#2E86AB'}
        },
        showlegend=False,
        height=300,
        margin=dict(t=60, b=30, l=30, r=30),
        plot_bgcolor='rgba(240,240,240,0.1)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            title='Number of Active Users',
            gridcolor='rgba(200,200,200,0.2)'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=12)
        )
    )
    
    # Display the bar chart
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # --- QUICK STATS ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Quick Statistics")
    
    # Create metrics in columns
    cols = st.columns(4)
    for i, (_, row) in enumerate(usage_df.iterrows()):
        with cols[i]:
            st.metric(
                label=row['Platform'],
                value=f"{row['Count']:,}",
                delta=f"{row['Percentage']}%"
            )
    
    # Platform comparison insight
    st.markdown("<br>", unsafe_allow_html=True)
    max_platform = usage_df.iloc[0]['Platform']
    max_percent = usage_df.iloc[0]['Percentage']
    
    st.info(f"💡 **Insight:** {max_platform} leads with **{max_percent}%** of active users among the platforms analyzed.")
    
    # --- DATA TABLE ---
    with st.expander("📋 View Detailed Data", expanded=False):
        # Format the dataframe for display
        display_df = usage_df.copy()
        display_df['Count'] = display_df['Count'].apply(lambda x: f"{x:,}")
        display_df['Percentage'] = display_df['Percentage'].apply(lambda x: f"{x}%")
        st.dataframe(
            display_df,
            column_config={
                "Platform": "Platform",
                "Count": "Active Users",
                "Percentage": "Share"
            },
            hide_index=True,
            use_container_width=True
        )
    
else:
    st.error("❌ Unable to generate visualization. Please check if the required columns exist in your dataset.")
    
# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 12px;'>Data Source: Fashion Habits Survey | Visualization created with Streamlit & Plotly</p>", unsafe_allow_html=True)
