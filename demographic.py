# =========================================================
# DEMOGRAPHIC INFORMATION SECTION - IZZATI 
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fashion Trends Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF.csv"
    return pd.read_csv(url)

df = load_data()


# Updated Sort Orders to match Google Form standards
age_order = [
    "<25 years old",
    "26-34 years old",
    "35-45 years old",
    "46-55 years old",
    ">55 years old"
]

education_order = [
    "Lower secondary education",
    "Secondary education",
    "Post-secondary education",
    "Bachelor’s degree",  
    "Master’s degree",
    "Doctoral degree"
]

expense_order = ["<500", "500-1000", "1000-3000", ">3000"]


# ---------------------------------------------------------
# Page Title & Description
# ---------------------------------------------------------
st.title("📊👥 Demographic Analysis")
st.markdown(
    "This section summarises the demographic profile of the respondents, providing "
    "background information on the sample characteristics."
)

st.subheader("🎯 Objective")

st.markdown(
    "To examine how demographic factors relate to consumers’ fashion awareness, "
    "spending behaviour, and shopping influences on social media."
)

# =========================================================
# SUMMARY BOX: KEY DEMOGRAPHIC INDICATORS
# =========================================================
st.subheader("👥 Key Demographic Summary")

col1, col2, col3 = st.columns(3)

total_respondents = len(df)
col1.metric(
    label="Total Respondents",
    value=f"{total_respondents}",
    help="Total number of valid survey responses collected"
)

gender_counts = df["Gender"].value_counts()
top_gender = gender_counts.idxmax()
top_gender_pct = (gender_counts.max() / total_respondents) * 100
col2.metric(
    label="Majority Gender",
    value=top_gender,
    help=f"{top_gender_pct:.1f}% of respondents"
)

region_counts = df["Region"].value_counts()
top_region = region_counts.idxmax()
top_region_pct = (region_counts.max() / total_respondents) * 100
col3.metric(
    label="Majority Region",
    value=top_region,
    help=f"{top_region_pct:.1f}% of respondents"
)


# =========================================================
# SECTION A: DEMOGRAPHIC DATA VISUALISATION
# =========================================================
st.header(" 🧍 Part 1 : Demographic Overview")
st.markdown(
    "This section summarises the demographic profile of the respondents, providing "
    "background information on the sample characteristics."
)

# Gender and Age Distribution 
st.subheader("1. Gender and Age Composition ")
st.markdown(" 💡 Use the filters below to refine the demographic breakdown.")
# 2 columns for the filters
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    selected_gender = st.multiselect(
        "Select Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

with col_filter2:
    selected_age = st.multiselect(
        "Select Age Groups:",
        options=age_order, 
        default=age_order
    )

# Apply filter
df_filtered = df[
    (df["Gender"].isin(selected_gender)) & 
    (df["Age"].isin(selected_age))
].copy() # to avoid SettingWithCopyWarning

# Bold Formating
# To makes 'Female' and 'Male' bold for chart labels 
df_filtered["Gender"] = df_filtered["Gender"].apply(lambda x: f"<b>{x}</b>")

# Sunburst Chart for Gender and Age
fig1 = px.sunburst(
    df_filtered,
    path=["Gender", "Age"], 
    values=None,           
    color="Gender",
    color_discrete_map={'<b>Female</b>': '#FFB6C1', '<b>Male</b>': '#ADD8E6'},
    title="Demographic Proportions: Gender and Age"
)

# hover and tooltip
fig1.update_traces(
    textinfo="label+percent entry", 
    marker=dict(line=dict(color='#FFFFFF', width=2)), # Appealing white border
    hovertemplate="""
    <b>Category:</b> %{label}<br>
    <b>Total Count:</b> %{value}<br>
    <b>Share of Parent:</b> %{percentParent:.1f}%<br>
    <extra></extra>
    """
)

fig1.update_layout(
    margin=dict(t=40, l=0, r=0, b=0),
    height=400,
    paper_bgcolor='rgba(0,0,0,0)', 
)

st.plotly_chart(fig1, use_container_width=True)
st.info("""
📝 Interpretation:


""")

st.markdown("---") 

# 2. Region Distribution
st.subheader("2. Regional Distribution of Respondents")


region_counts = df["Region"].value_counts().reset_index()
region_counts.columns = ["Region", "Count"]

# Calculate percentages for the tooltip
total_n = region_counts["Count"].sum()
region_counts["Percentage"] = (region_counts["Count"] / total_n) * 100

# Bar Chart
fig2 = px.bar(
    region_counts,
    x='Region',
    y='Count',
    color='Region',
    color_discrete_map={'East Malaysia': '#A5D6A7', 'West Malaysia': '#90CAF9'},
    title="Geographic Representation: East vs. West Malaysia",
    text_auto=True
)

# Hover and tooltip
fig2.update_traces(
    width=0.5,
    textposition='outside',
    cliponaxis=False,
    hovertemplate="""
    <b>Region:</b> %{x}<br>
    <b>Respondents:</b> %{y}<br>
    <b>Percentage:</b> %{customdata:.1f}%<br>
    <extra></extra>
    """,
    customdata=region_counts["Percentage"] # Pass the percentage to the tooltip
)

fig2.update_layout(
    height=400,
    title_x=0,
    xaxis_title=None,
    yaxis_title="Total Respondents",
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14)
)

st.plotly_chart(fig2, use_container_width=True)

st.info("""
📝 Interpretation:

""")

st.markdown("---")

# 3. Education Level Distribution
st.subheader("3. Education Level Distribution")

edu_counts = (
    df["Education Level"]
    .value_counts()
    .reindex(education_order, fill_value=0)
    .reset_index(name="count")
    .rename(columns={"index": "Education Level"})
    .rename(columns={"Education Level": "Education Level"})
)

fig3 = px.bar(
    edu_counts,
    x="count",
    y="Education Level",
    orientation="h",
    color="count",
    color_continuous_scale=['#E1BEE7', '#9C27B0', '#4A148C'],
    title="Highest Education Level of Respondents",
    category_orders={"Education Level": education_order}
)

fig3.update_traces(
    texttemplate='<b>%{x}</b>', 
    textposition='outside',
    cliponaxis=False, 
    hovertemplate="<b>%{y}</b><br>Respondents: %{x}<extra></extra>"
)

fig3.update_layout(
    title_x=0, 
    height=400, 
    showlegend=False, 
    coloraxis_showscale=False,
    xaxis_title="Total Respondents", 
    yaxis_title=None,
    margin=dict(l=0, r=100), 
    xaxis_range=[0, edu_counts["count"].max() * 1.3],
    bargap=0.3,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig3, use_container_width=True)

st.info("""
📝 Interpretation:

""")

# 4. Employment Status Distribution
st.subheader("4. Employment Status Distribution")

employment_counts = df["Employment Status"].value_counts().reset_index()
employment_counts.columns = ["Status", "Count"]

fig4 = px.pie(
    employment_counts,
    values='Count',
    names='Status',
    hole=0.6,
    title="Employment Status Composition",
    color_discrete_sequence=['#D4A5A5', '#E9C46A', '#F4A261', '#E76F51']
)

fig4.update_traces(
    textinfo='percent+label', 
    marker=dict(line=dict(color='#FFFFFF', width=2)),
    hovertemplate="<b>%{label}</b><br>Total: %{value} respondents<br>Percentage: %{percent}<extra></extra>"
)

fig4.update_layout(
    title_x=0, 
    height=400,
    showlegend=True,
    margin=dict(t=80, b=20, l=20, r=20)
)

st.plotly_chart(fig4, use_container_width=True)

st.info("""
📝 Interpretation:

""")

# 5. Monthly Fashion Expenditure
st.subheader("5. Monthly Fashion Expenditure Distribution")


expense_counts = df["Average Monthly Expenses (RM)"].value_counts().reindex(expense_order).reset_index()
expense_counts.columns = ["Expense", "Count"]
expense_counts['pct'] = (expense_counts['Count'] / expense_counts['Count'].sum()) * 100


expense_rank_map = {val: i for i, val in enumerate(expense_order)}
expense_counts['rank'] = expense_counts['Expense'].map(expense_rank_map)

fig5 = px.bar(
    expense_counts,
    x='Expense',
    y='Count',
    color='rank',
    color_continuous_scale=['#B2DFDB', '#4DB6AC', '#00796B', '#004D40'], 
    title="Monthly Fashion Expenditure (Respondents by Category)",
    category_orders={"Expense": expense_order}
)

fig5.update_traces(
    texttemplate='<b>%{y}</b>', 
    textposition='outside',
    cliponaxis=False,
    hovertemplate="""
    <b>Spending Range:</b> RM %{x}<br>
    <b>Total Respondents:</b> %{y}<br>
    <b>Percentage:</b> %{customdata:.1f}%<br>
    <extra></extra>
    """,
    customdata=expense_counts["pct"]
)

fig5.update_layout(
    bargap=0.4,
    yaxis_range=[0, expense_counts["Count"].max() * 1.3], 
    title_x=0, 
    height=400, 
    coloraxis_showscale=False, 
    xaxis_title="Average Monthly Expenses (RM)",
    yaxis_title="Number of Respondents",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig5, use_container_width=True)
st.info("""
📝 Interpretation:
""")


# 6. Awareness of Fashion Trends
st.subheader("6. Awareness of Fashion Trends")


awareness_counts = df["Awareness of Fashion Trends"].value_counts().sort_index().reset_index()
awareness_counts.columns = ["Level", "Count"]

# Create the labels 
awareness_map = {
    1: "1 - Not aware at all",
    2: "2 - Slightly aware",
    3: "3 - Moderately aware",
    4: "4 - Very aware",
    5: "5 - Extremely aware"
}
awareness_counts['Label'] = awareness_counts['Level'].map(awareness_map)

fig6 = px.bar(
    awareness_counts,
    x='Label',
    y='Count',
    color='Level', 
    color_continuous_scale=['#FFEBEE', '#EF9A9A', '#E53935', '#B71C1C'], 
    title="Level of Awareness: Current Fashion Trends & Styles"
)

fig6.update_traces(
    texttemplate='<b>%{y}</b>', 
    textposition='outside',
    cliponaxis=False,
    hovertemplate="<b>%{x}</b><br>Respondents: %{y}<extra></extra>"
)

fig6.update_layout(
    bargap=0.4,
    yaxis_range=[0, awareness_counts["Count"].max() * 1.2],
    title_x=0, 
    height=400, 
    coloraxis_showscale=False,
    xaxis_title=None, 
    yaxis_title="Number of Respondents",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig6, use_container_width=True)

st.info("""
📝 Interpretation:
""")

# 7. Factors Influencing Fashion Shopping Decisions
st.subheader("7. Factors Influencing Fashion Shopping Decisions")

influence_counts = df["Influence on Shopping"].value_counts().reset_index()
influence_counts.columns = ["Factor", "Count"]

fig7 = px.bar(
    influence_counts,
    x='Count',
    y='Factor',
    orientation='h',
    color='Count',
    color_continuous_scale=['#FADBD8', '#E59866', '#7B241C'], 
    title="Ranking of Influence Sources"
)

fig7.update_traces(
    width=0.7, 
    texttemplate='<b>%{x}</b>', 
    textposition='outside', 
    cliponaxis=False
)

fig7.update_layout(
    bargap=0.3,
    yaxis={'categoryorder': 'total ascending'}, 
    title_x=0, 
    height=400,
    coloraxis_showscale=False, 
    xaxis_range=[0, influence_counts["Count"].max() * 1.3], # Headroom for text
    margin=dict(l=0, r=100),
    xaxis_title="Total Respondents",
    yaxis_title=None,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig7, use_container_width=True)

st.info("""
📝 Interpretation:
""")

# =========================================================
# SECTION B: COMPARATIVE & BEHAVIOURAL ANALYSIS
# =========================================================
st.divider()
st.header("📈 Part 2: Demographic–Behavioural Relationships")
st.markdown(
    "This section examines how demographic factors are related to fashion awareness, "
    "spending behaviour, and shopping influences on social media."
)
# 9️⃣ Fashion Awareness by Gender
st.subheader("9. Fashion Awareness by Gender")

fig9 = px.bar(
    df.groupby(["Gender", "Awareness of Fashion Trends"]).size().reset_index(name="Count"),
    x="Gender",
    y="Count",
    color="Awareness of Fashion Trends",
    barmode="stack",
    title="Fashion Awareness by Gender"
)
st.plotly_chart(fig9, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown(""" 
This chart examines how gender differences relate to levels of awareness of current fashion trends on social media.

- Female respondents show higher concentrations at moderate to high awareness levels.
- This suggests stronger exposure to and engagement with fashion-related content among females.
- The pattern indicates that gender plays a meaningful role in shaping fashion awareness, supporting the study’s objective of examining demographic influence.
""")
st.markdown("---")


# 🔟 Monthly Fashion Expenditure by Employment Status
#st.subheader("10. Monthly Fashion Expenditure by Employment Status")

#fig10 = px.bar(
    #df.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count"),
    #x="Employment Status",
    #y="Count",
    #color="Average Monthly Expenses (RM)",
    #barmode="group",
    #title="Monthly Fashion Expenditure by Employment Status",
    #category_orders={"Average Monthly Expenses (RM)": expense_order}
#)
#st.plotly_chart(fig10, use_container_width=True)

#st.subheader("📝 Interpretation:")
#st.markdown("""

#""")
#st.markdown("---") 
# 🔟 Monthly Fashion Expenditure by Employment Status (Heatmap)
st.subheader("10. Monthly Fashion Expenditure by Employment Status (Heatmap)")

# Prepare data
heatmap_data = (
    df.groupby(["Employment Status", "Average Monthly Expenses (RM)"])
      .size()
      .reset_index(name="Count")
)

# Pivot for heatmap
heatmap_pivot = heatmap_data.pivot(
    index="Employment Status",
    columns="Average Monthly Expenses (RM)",
    values="Count"
).fillna(0)

# Ensure correct order of expense categories
heatmap_pivot = heatmap_pivot[expense_order]

# Plot heatmap
fig_heatmap = px.imshow(
    heatmap_pivot,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    labels=dict(
        x="Average Monthly Fashion Expenses (RM)",
        y="Employment Status",
        color="Number of Respondents"
    ),
    title="Monthly Fashion Expenditure by Employment Status"
)

st.plotly_chart(fig_heatmap, use_container_width=True)
st.subheader("📝 Interpretation:")
st.markdown(""" 
This chart explores how employment status relates to respondents’ monthly fashion expenditure.

- Employed respondents, particularly full-time workers, appear more frequently in higher expenditure categories.
- This reflects greater financial capacity among employed individuals to engage in fashion consumption.
- The relationship highlights employment status as a key demographic factor influencing spending behaviour on fashion items.
""")
st.markdown("---")
 

# 1️⃣1️⃣ Shopping Influence by Gender
st.subheader("11. Shopping Influence Factors by Gender")

fig11 = px.bar(
    df.groupby(["Gender", "Influence on Shopping"]).size().reset_index(name="Count"),
    x="Count",
    y="Influence on Shopping",
    color="Gender",
    orientation='h',
    barmode='group',
    title="Shopping Influence by Gender"
)
st.plotly_chart(fig11, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown("""  
This chart compares how different sources influence fashion shopping decisions across genders.

- Female respondents show stronger influence from social sources such as influencers and online communities.
- Male respondents display a more varied or neutral influence pattern.
- This suggests that gender differences affect how social recommendations shape online fashion purchasing behaviour.
""")
st.markdown("---")


# 1️⃣2️⃣ Shopping Influence by Monthly Expenditure Level
st.subheader("12. Shopping Influence by Monthly Expenditure Level")

fig13 = px.bar(
    df.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count"),
    x="Count",
    y="Influence on Shopping",
    color="Average Monthly Expenses (RM)",
    orientation='h',
    barmode='group',
    title="Shopping Influence by Monthly Expenditure Level",
    category_orders={"Average Monthly Expenses (RM)": expense_order}
)
st.plotly_chart(fig13, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown(""" 
This chart analyses how monthly fashion expenditure levels relate to shopping influence sources.

- Higher-spending respondents are more influenced by brand-driven and influencer-related recommendations.
- Lower-spending respondents rely more on personal judgment or non-commercial sources.
- This indicates that spending capacity interacts with external influence, reinforcing the link between economic demographics and shopping decisions.
""")
st.markdown("---")

# gender_expense = df.groupby(["Gender", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
# fig12 = px.bar(
#     gender_expense,
#     x="Gender",
#     y="Count",
#     color="Average Monthly Expenses (RM)",
#     title="Average Monthly Fashion Expenses by Gender",
#     barmode='group',
#     category_orders={"Average Monthly Expenses (RM)": expense_order}
# )
# st.plotly_chart(fig12, use_container_width=True)

# =========================================================
# SECTION B: COMPARATIVE & BEHAVIOURAL ANALYSIS
# =========================================================
st.divider()
st.header("📈 Part 2: Demographic–Behavioural Relationships")
st.markdown("Use the filter below to see how different regions compare across all behavioral charts.")

# 1. ADDING THE "REMOTE CONTROL" (Global Filter)
# This filter will control Fig 9, 10, 11, and 12
selected_region_b = st.multiselect(
    "Select Region to Update Analysis:",
    options=df["Region"].unique(),
    default=df["Region"].unique(),
    key="region_filter_b"
)

# Apply the filter to a new dataframe for this section
df_b = df[df["Region"].isin(selected_region_b)]

# ---------------------------------------------------------
# 9️⃣ Fashion Awareness by Gender
# ---------------------------------------------------------
st.subheader("9. Fashion Awareness by Gender")

# We use df_b here so it reacts to the filter
fig9_data = df_b.groupby(["Gender", "Awareness of Fashion Trends"]).size().reset_index(name="Count")

fig9 = px.bar(
    fig9_data,
    x="Gender",
    y="Count",
    color="Awareness of Fashion Trends",
    barmode="stack",
    color_continuous_scale=['#FFEBEE', '#EF9A9A', '#E53935', '#B71C1C'],
    title="Fashion Awareness Distribution"
)

fig9.update_traces(
    hovertemplate="<b>Gender:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>"
)

fig9.update_layout(bargap=0.5, height=450, coloraxis_showscale=False, title_x=0)
st.plotly_chart(fig9, use_container_width=True)

# ---------------------------------------------------------
# 🔟 Monthly Expenditure Heatmap
# ---------------------------------------------------------
st.subheader("10. Monthly Expenditure by Employment")

heatmap_data = df_b.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
heatmap_pivot = heatmap_data.pivot(index="Employment Status", columns="Average Monthly Expenses (RM)", values="Count").fillna(0)

# Sort columns to match your RM order
existing_cols = [c for c in expense_order if c in heatmap_pivot.columns]
heatmap_pivot = heatmap_pivot[existing_cols]

fig10 = px.imshow(
    heatmap_pivot,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    title="Spending Density Heatmap"
)
fig10.update_layout(title_x=0)
st.plotly_chart(fig10, use_container_width=True)

# ---------------------------------------------------------
# 1️⃣1️⃣ Shopping Influence by Gender
# ---------------------------------------------------------
st.subheader("11. Shopping Influence Factors by Gender")

fig11_data = df_b.groupby(["Gender", "Influence on Shopping"]).size().reset_index(name="Count")

fig11 = px.bar(
    fig11_data,
    x='Count',
    y='Influence on Shopping',
    color='Gender',
    orientation='h',
    barmode='group',
    color_discrete_map={'Female': '#FFB6C1', 'Male': '#ADD8E6'}, 
    title="Influence Sources (Male vs Female)"
)

fig11.update_traces(
    hovertemplate="<b>Group:</b> %{fullData.name}<br><b>Total:</b> %{x}<extra></extra>"
)

fig11.update_layout(bargap=0.2, height=500, title_x=0, yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig11, use_container_width=True)

# ---------------------------------------------------------
# 1️⃣2️⃣ Shopping Influence by Expenditure
# ---------------------------------------------------------
st.subheader("12. Shopping Influence by Expenditure Level")

fig12_data = df_b.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count")

fig12 = px.bar(
    fig12_data,
    x="Count",
    y="Influence on Shopping",
    color="Average Monthly Expenses (RM)",
    orientation='h',
    barmode='stack',
    color_discrete_sequence=['#B2DFDB', '#4DB6AC', '#00796B', '#004D40'],
    title="Influence Sources by Spending Power",
    category_orders={"Average Monthly Expenses (RM)": expense_order}
)

fig12.update_traces(
    hovertemplate="<b>Spend Level:</b> %{fullData.name}<br><b>Count:</b> %{x}<extra></extra>"
)

fig12.update_layout(bargap=0.3, height=500, title_x=0, margin=dict(l=150))
st.plotly_chart(fig12, use_container_width=True)

st.divider()
st.header("📈 Part 2: Behavioural Analysis")

# 1. THE DROPDOWN (The "Remote Control")
choice = st.selectbox("Select Gender to view:", ["All", "Female", "Male"])

# 2. THE LOGIC (If user picks Female, show only Female data)
if choice == "All":
    df_simple = df
else:
    df_simple = df[df["Gender"] == choice]

# ---------------------------------------------------------
# 9. Awareness Chart (Now it reacts to the choice above!)
# ---------------------------------------------------------
st.subheader(f"9. Fashion Awareness ({choice})")

fig9 = px.bar(
    df_simple.groupby("Awareness of Fashion Trends").size().reset_index(name="Count"),
    x="Awareness of Fashion Trends",
    y="Count",
    title=f"Awareness Level for {choice}"
)
st.plotly_chart(fig9, use_container_width=True)

# ---------------------------------------------------------
# 10. Spending Chart (Also reacts to the choice!)
# ---------------------------------------------------------
st.subheader(f"10. Monthly Spending ({choice})")

fig10 = px.bar(
    df_simple.groupby("Average Monthly Expenses (RM)").size().reset_index(name="Count"),
    x="Average Monthly Expenses (RM)",
    y="Count",
    title=f"Spending Distribution for {choice}",
    category_orders={"Average Monthly Expenses (RM)": expense_order}
)
st.plotly_chart(fig10, use_container_width=True)


# =========================================================
# SECTION B: COMPARATIVE & BEHAVIOURAL ANALYSIS
# =========================================================
st.divider()
st.header("📈 Part 2: Behavioural Analysis")

# 1. THE SIMPLE FILTER
# This allows the user to focus on one gender at a time
gender_choice = st.selectbox("View Analysis for:", ["All Respondents", "Female", "Male"])

# 2. FILTERING THE DATA
if gender_choice == "All Respondents":
    df_part2 = df
else:
    # This filters the data to only show the chosen gender
    df_part2 = df[df["Gender"] == gender_choice]

# ---------------------------------------------------------
# 9. Awareness by Gender (Simple & Red)
# ---------------------------------------------------------
st.subheader(f"9. Fashion Awareness Level ({gender_choice})")

fig9_data = df_part2.groupby("Awareness of Fashion Trends").size().reset_index(name="Count")

fig9 = px.bar(
    fig9_data,
    x="Awareness of Fashion Trends",
    y="Count",
    color="Count",
    color_continuous_scale=['#FFEBEE', '#B71C1C'], # Soft pink to Deep red
    title=f"Awareness Distribution: {gender_choice}"
)
fig9.update_layout(height=400, coloraxis_showscale=False, bargap=0.4)
st.plotly_chart(fig9, use_container_width=True)

# ---------------------------------------------------------
# 10. Spending Heatmap (Filtered)
# ---------------------------------------------------------
st.subheader(f"10. Spending by Employment ({gender_choice})")

heatmap_data = df_part2.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
heatmap_pivot = heatmap_data.pivot(index="Employment Status", columns="Average Monthly Expenses (RM)", values="Count").fillna(0)

# Make sure RM categories are in the right order
existing_cols = [c for c in expense_order if c in heatmap_pivot.columns]
heatmap_pivot = heatmap_pivot[existing_cols]

fig10 = px.imshow(
    heatmap_pivot,
    text_auto=True,
    color_continuous_scale="Blues",
    title=f"Where {gender_choice} Spend Money"
)
st.plotly_chart(fig10, use_container_width=True)

# ---------------------------------------------------------
# 11. Influence Ranking (Filtered)
# ---------------------------------------------------------
st.subheader(f"11. Top Influence Factors ({gender_choice})")

influence_data = df_part2.groupby("Influence on Shopping").size().reset_index(name="Count")

fig11 = px.bar(
    influence_data,
    x="Count",
    y="Influence on Shopping",
    orientation='h',
    color="Count",
    color_continuous_scale=['#FADBD8', '#7B241C'], # Soft Rose to Wine
    title=f"What Influences {gender_choice} Most?"
)
fig11.update_layout(yaxis={'categoryorder':'total ascending'}, height=450, coloraxis_showscale=False, bargap=0.4)
st.plotly_chart(fig11, use_container_width=True)





st.divider()
st.header("📈 Part 2: Behavioural Analysis")

# 1. THE FILTERS (Side-by-Side)
col_f1, col_f2 = st.columns(2)
with col_f1:
    gender_choice = st.selectbox("Select Gender:", ["All", "Female", "Male"])
with col_f2:
    region_choice = st.selectbox("Select Region:", ["All", "West Malaysia", "East Malaysia"])

# 2. FILTER LOGIC
df_filtered = df.copy()
if gender_choice != "All":
    df_filtered = df_filtered[df_filtered["Gender"] == gender_choice]
if region_choice != "All":
    df_filtered = df_filtered[df_filtered["Region"] == region_choice]




# 9. Fashion Awareness (Stacked Bar Chart)
st.subheader("9. Fashion Awareness Level")

# We use a single color scale here so "Darker" always means "Higher Level"
fig9_data = df_filtered.groupby(["Gender", "Awareness of Fashion Trends"]).size().reset_index(name="Count")

fig9 = px.bar(
    fig9_data,
    x="Gender",
    y="Count",
    color="Awareness of Fashion Trends",
    barmode="stack",
    # Using a Purple-Blue scale: Level 1 is light, Level 5 is very dark
    color_discrete_sequence=['#E8EAF6', '#C5CAE9', '#7986CB', '#3F51B5', '#1A237E'],
    title="Awareness Distribution (Darker Color = Level 5 Awareness)"
)

fig9.update_layout(bargap=0.5, height=500)

# Create two columns to show the chart and the Level Table side-by-side
c1, c2 = st.columns([3, 1])
with c1:
    st.plotly_chart(fig9, use_container_width=True)
with c2:
    st.write("🔍 **Awareness Key**")
    st.markdown("""
    | Level | Intensity |
    | :--- | :--- |
    | **5** | ⬛ Darkest |
    | **4** | 🟦 Dark |
    | **3** | 🟦 Medium |
    | **2** | 🧊 Light |
    | **1** | ⬜ Lightest |
    """)

# ---------------------------------------------------------
# 10. Spending Heatmap
# ---------------------------------------------------------
st.subheader("10. Spending by Employment Status")

heatmap_data = df_filtered.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
heatmap_pivot = heatmap_data.pivot(index="Employment Status", columns="Average Monthly Expenses (RM)", values="Count").fillna(0)

# Sort columns to match your RM order
existing_cols = [c for c in expense_order if c in heatmap_pivot.columns]
heatmap_pivot = heatmap_pivot[existing_cols]

fig10 = px.imshow(
    heatmap_pivot,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Spending Density"
)
st.plotly_chart(fig10, use_container_width=True)

# ---------------------------------------------------------
# 11. Shopping Influence by Gender
# ---------------------------------------------------------
st.subheader("11. Shopping Influence Factors")

fig11_data = df_filtered.groupby(["Gender", "Influence on Shopping"]).size().reset_index(name="Count")

fig11 = px.bar(
    fig11_data,
    x="Count",
    y="Influence on Shopping",
    color="Gender",
    orientation='h',
    barmode='group', # Side-by-side for easy comparison
    color_discrete_map={'Female': '#FFB6C1', 'Male': '#ADD8E6'},
    title="Influence Sources: Male vs Female"
)
fig11.update_layout(yaxis={'categoryorder':'total ascending'}, height=500, title_x=0)
st.plotly_chart(fig11, use_container_width=True)

# ---------------------------------------------------------
# 12. Shopping Influence by Expenditure Level
# ---------------------------------------------------------
st.subheader("12. Shopping Influence by Spending Power")

fig12_data = df_filtered.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count")

fig12 = px.bar(
    fig12_data,
    x="Count",
    y="Influence on Shopping",
    color="Average Monthly Expenses (RM)",
    orientation='h',
    barmode='stack', # Stacked to see the "mix" of spenders for each factor
    color_discrete_sequence=['#B2DFDB', '#4DB6AC', '#00796B', '#004D40'],
    category_orders={"Average Monthly Expenses (RM)": expense_order},
    title="Influence Sources by Spending Level"
)
fig12.update_layout(height=500, margin=dict(l=150), title_x=0)
st.plotly_chart(fig12, use_container_width=True)


st.divider()
st.header("📈 Part 2: Behavioural Analysis")

# --- TWO SEPARATE FILTERS ---
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    gender_choice = st.selectbox("Filter Awareness & Influence (Fig 9, 11):", ["All", "Female", "Male"])

with col_filter2:
    expense_choice = st.selectbox("Filter Spending Behavior (Fig 10, 12):", ["All"] + expense_order)

# ---------------------------------------------------------
# 9 & 11: GENDER-BASED ANALYSIS
# ---------------------------------------------------------
df_gender = df.copy()
if gender_choice != "All":
    df_gender = df_gender[df_gender["Gender"] == gender_choice]

st.subheader("9. Fashion Awareness Level")
c1, c2 = st.columns([3, 1])
with c1:
    fig9_data = df_gender.groupby(["Gender", "Awareness of Fashion Trends"]).size().reset_index(name="Count")
    fig9 = px.bar(
        fig9_data, x="Gender", y="Count", color="Awareness of Fashion Trends",
        barmode="stack",
        color_discrete_sequence=['#E8EAF6', '#C5CAE9', '#7986CB', '#3F51B5', '#1A237E'],
        title=f"Awareness for {gender_choice}"
    )
    fig9.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)
with c2:
    st.write("### 🔍 Key")
    st.markdown("| Lvl | Color |\n| :--- | :--- |\n| 5 | 🟦 Dark |\n| ... | ... |\n| 1 | ⬜ Light |")

st.subheader("11. Shopping Influence Factors")
fig11_data = df_gender.groupby(["Gender", "Influence on Shopping"]).size().reset_index(name="Count")
fig11 = px.bar(
    fig11_data, x="Count", y="Influence on Shopping", color="Gender",
    orientation='h', barmode='group',
    color_discrete_map={'Female': '#FFB6C1', 'Male': '#ADD8E6'},
    title=f"Influence by Gender: {gender_choice}"
)
st.plotly_chart(fig11, use_container_width=True)

# ---------------------------------------------------------
# 10 & 12: EXPENDITURE-BASED ANALYSIS
# ---------------------------------------------------------
df_expense = df.copy()
if expense_choice != "All":
    df_expense = df_expense[df_expense["Average Monthly Expenses (RM)"] == expense_choice]

st.subheader("10. Spending vs Employment")
heatmap_data = df_expense.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
fig10 = px.density_heatmap(
    heatmap_data, x="Average Monthly Expenses (RM)", y="Employment Status", z="Count",
    color_continuous_scale="Greens", title=f"Spending Power: {expense_choice}"
)
st.plotly_chart(fig10, use_container_width=True)

st.subheader("12. Influence by Spending Level")
fig12_data = df_expense.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count")
fig12 = px.bar(
    fig12_data, x="Count", y="Influence on Shopping", color="Average Monthly Expenses (RM)",
    orientation='h', barmode='stack',
    color_discrete_sequence=['#E8F5E9', '#A5D6A7', '#4CAF50', '#2E7D32', '#1B5E20'],
    title=f"Influence for {expense_choice} Spenders"
)
st.plotly_chart(fig12, use_container_width=True)
