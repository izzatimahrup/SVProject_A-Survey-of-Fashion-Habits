# =========================================================
# STREAMLIT APP: Interactive Fashion Analysis (Plotly)
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
# 3. REGIONAL DISTRIBUTION
# ---------------------------------------------------------
st.subheader("3. Regional Distribution of Respondents")

# 1. Prepare Data
region_counts = df["Region"].value_counts().reset_index()
region_counts.columns = ["Region", "Count"]

# Calculate percentages for the tooltip
total_n = region_counts["Count"].sum()
region_counts["Percentage"] = (region_counts["Count"] / total_n) * 100

# 2. Create the Bar Chart
fig3 = px.bar(
    region_counts,
    x='Region',
    y='Count',
    color='Region',
    # Using Teal and Purple: Modern and distinct from Gender colors
    color_discrete_map={'East Malaysia': '#008080', 'West Malaysia': '#6A5ACD'},
    title="Geographic Representation: East vs. West Malaysia",
    text_auto=True
)

# 3. Custom Hover Tooltip and Styling
fig3.update_traces(
    textposition='outside',
    # This customizes what you see when you hover your mouse
    hovertemplate="""
    <b>Region:</b> %{x}<br>
    <b>Respondents:</b> %{y}<br>
    <b>Percentage:</b> %{customdata:.1f}%<br>
    <extra></extra>
    """,
    customdata=region_counts["Percentage"] # Pass the percentage to the tooltip
)

fig3.update_layout(
    height=500,
    title_x=0.5,
    xaxis_title=None,
    yaxis_title="Total Respondents",
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14)
)

st.plotly_chart(fig3, use_container_width=True)

# 4. Blue Interpretation Box (Replaces the markdown text)
st.info("""
### 📝 Interpretation:

This chart compares respondents from East and West Malaysia to assess geographic representation.

* **East Malaysia vs. West Malaysia:** Respondents from East Malaysia slightly outnumber those from West Malaysia.
* **Urban vs. Rural Engagement:** This suggests that fashion engagement through social media is not confined to highly urbanised regions.
* **Digital Inclusion:** The result indicates that social media effectively reduces geographic barriers in shaping fashion awareness and shopping behaviour.
""")

st.markdown("---")
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

# 1️⃣ Gender and Age Distribution 
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
fig_sun = px.sunburst(
    df_filtered,
    path=["Gender", "Age"], 
    values=None,           
    color="Gender",
    color_discrete_map={'<b>Female</b>': '#FFB6C1', '<b>Male</b>': '#ADD8E6'},
    title="Demographic Proportions: Gender and Age"
)

# hover and tooltip
fig_sun.update_traces(
    textinfo="label+percent entry", 
    marker=dict(line=dict(color='#FFFFFF', width=2)), # Appealing white border
    hovertemplate="""
    <b>Category:</b> %{label}<br>
    <b>Total Count:</b> %{value}<br>
    <b>Share of Parent:</b> %{percentParent:.1f}%<br>
    <extra></extra>
    """
)

fig_sun.update_layout(
    margin=dict(t=40, l=0, r=0, b=0),
    height=400,
    paper_bgcolor='rgba(0,0,0,0)', 
)

st.plotly_chart(fig_sun, use_container_width=True)
st.info("""
📝 Interpretation:


""")

st.markdown("---") 

# 3️⃣ Regional Distribution
st.subheader("3. Regional Distribution of Respondents")

region_counts = df["Region"].value_counts().reset_index()
fig3 = px.bar(
    region_counts,
    x='Region',
    y='count',
    text_auto=True,
    title="Regional Distribution"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown("""  
This chart compares respondents from East and West Malaysia to assess geographic representation.

- Respondents from East Malaysia slightly outnumber those from West Malaysia.
- This suggests that fashion engagement through social media is not confined to highly urbanised regions.
- The result indicates that social media reduces geographic barriers in shaping fashion awareness and shopping behaviour.
""")
st.markdown("---")

st.markdown("---") 

# 4️⃣ Education Level Distribution
st.subheader("4. Education Level Distribution of Respondents")

edu_counts = (
    df["Education Level"]
    .value_counts()
    .reindex(education_order, fill_value=0)
    .reset_index(name="count")
    .rename(columns={"index": "Education Level"})
)

fig4 = px.bar(
    edu_counts,
    x="count",
    y="Education Level",
    orientation="h",
    text_auto=True,
    title="Education Level of Respondents",
    category_orders={"Education Level": education_order}
)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown(""" 
This chart shows respondents’ highest education levels, which may influence information processing and decision-making.

- Most respondents possess post-secondary or tertiary education.
- Higher education levels are often associated with greater exposure to digital content and brand information.
- This distribution suggests that educational background may influence how individuals interpret fashion trends and make informed shopping decisions online.
""")
st.markdown("---")


# 5️⃣ Employment Status Distribution
st.subheader("5. Employment Status Distribution")

employment_counts = df["Employment Status"].value_counts().reset_index()
fig5 = px.pie(
    employment_counts,
    values='count',
    names='Employment Status',
    title="Employment Status Distribution"
)
st.plotly_chart(fig5, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown("""
This chart presents respondents’ employment status to understand their economic positioning.

- A large proportion of respondents are employed either full-time or part-time.
- Employment status reflects financial stability, which directly affects purchasing capacity.
- This highlights employment as a relevant demographic factor influencing fashion spending behaviour on social media.
""")
st.markdown("---")
 
# 6️⃣ Monthly Fashion Expenditure
st.subheader("6. Monthly Fashion Expenditure Distribution")

expense_counts = df["Average Monthly Expenses (RM)"].value_counts().reindex(expense_order).reset_index()
expense_counts['percentage'] = (expense_counts['count'] / expense_counts['count'].sum()) * 100

fig6 = px.bar(
    expense_counts,
    x='Average Monthly Expenses (RM)',
    y='percentage',
    text=expense_counts['percentage'].apply(lambda x: f'{x:.1f}%'),
    title="Distribution of Monthly Fashion Expenses (%)",
    category_orders={"Average Monthly Expenses (RM)": expense_order}
)
st.plotly_chart(fig6, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown(""" 
This chart examines respondents’ average monthly spending on fashion items.

- Most respondents fall within low to middle expenditure categories.
- This indicates cautious but consistent fashion consumption behaviour.
- The spending pattern suggests that affordability and perceived value influence online fashion purchasing decisions.
""")
st.markdown("---")


# 7️⃣ Awareness of Fashion Trends
st.subheader("7. Awareness of Fashion Trends")

awareness_counts = df["Awareness of Fashion Trends"].value_counts().sort_index().reset_index()
awareness_counts['percentage'] = (awareness_counts['count'] / awareness_counts['count'].sum()) * 100

fig7 = px.bar(
    awareness_counts,
    x='Awareness of Fashion Trends',
    y='percentage',
    text=awareness_counts['percentage'].apply(lambda x: f'{x:.1f}%'),
    title="Awareness of Current Fashion Trends (%)"
)
st.plotly_chart(fig7, use_container_width=True)

st.subheader("📝 Interpretation:")
st.markdown(""" 
This chart reflects respondents’ self-reported awareness of current fashion trends.

- A majority of respondents report moderate to high awareness of fashion trends.
- This indicates frequent exposure to fashion-related content on social media platforms.
- The finding supports the study’s objective of examining how demographic characteristics relate to fashion awareness.
""")
st.markdown("---")

# 8️⃣ Factors Influencing Shopping Decisions
st.subheader("8. Factors Influencing Fashion Shopping Decisions")

influence_counts = df["Influence on Shopping"].value_counts().reset_index()
fig8 = px.bar(
    influence_counts,
    x='count',
    y='Influence on Shopping',
    orientation='h',
    text_auto=True,
    title="Factors Influencing Shopping Decisions"
)
fig8.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig8, use_container_width=True) 
st.subheader("📝 Interpretation:")
st.markdown("""
This chart ranks the sources influencing respondents’ fashion shopping decisions.

- Social influences such as influencers, peers, and online content emerge as dominant factors.
- This highlights the interaction between demographic characteristics and external recommendation sources.
- The result aligns with the study’s focus on understanding how demographics shape online fashion decision-making.
""")
st.markdown("---")

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
