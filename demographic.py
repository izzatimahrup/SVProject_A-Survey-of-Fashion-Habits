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


st.header("📈 Part 2: Behavioural Analysis")


# SECTION A: GENDER PERSPECTIVE
st.subheader("📍 Section A: Gender-Based Trends")
st.markdown("""
    This section examines how fashion awareness and external influences differ between Male and Female respondents.
""")

st.markdown("💡 Use the filter below to refine Gender:")
gender_choice = st.selectbox("Select Gender:", ["All", "Female", "Male"], key="gender_filter_top")

df_gender = df.copy()
if gender_choice != "All":
    df_gender = df_gender[df_gender["Gender"] == gender_choice]

# 9. Fashion Awareness - Gender
st.subheader("9. Fashion Awareness by Gender")

# 1. Define the descriptive labels
awareness_labels = {
    5: "5 - Extremely aware",
    4: "4 - Very aware",
    3: "3 - Moderately aware",
    2: "2 - Slightly aware",
    1: "1 - Not aware at all"
}

# 2. Map labels to data
fig9_df = df_gender.copy()
fig9_df["Awareness Label"] = fig9_df["Awareness of Fashion Trends"].map(awareness_labels)
fig9_data = fig9_df.groupby(["Gender", "Awareness Label"]).size().reset_index(name="Count")

# 3. Dynamic Color Logic
if gender_choice == "All":
    # Green Gradient for "All" view
    color_mapping = {
        "5 - Extremely aware": "#1B5E20", # Darkest
        "4 - Very aware": "#2E7D32",
        "3 - Moderately aware": "#4CAF50",
        "2 - Slightly aware": "#A5D6A7",
        "1 - Not aware at all": "#E8F5E9"  # Lightest
    }
    color_col = "Awareness Label"
else:
    # Pink/Blue Gradients for specific gender view
    color_mapping = {
        ("Female", "5 - Extremely aware"): "#880E4F", ("Female", "4 - Very aware"): "#E91E63",
        ("Female", "3 - Moderately aware"): "#F06292", ("Female", "2 - Slightly aware"): "#F8BBD0",
        ("Female", "1 - Not aware at all"): "#FCE4EC",
        ("Male", "5 - Extremely aware"): "#0D47A1", ("Male", "4 - Very aware"): "#2196F3",
        ("Male", "3 - Moderately aware"): "#64B5F6", ("Male", "2 - Slightly aware"): "#BBDEFB",
        ("Male", "1 - Not aware at all"): "#E3F2FD"
    }
    fig9_data["Color_Key"] = fig9_data.apply(lambda x: (x["Gender"], x["Awareness Label"]), axis=1)
    color_col = "Color_Key"

# 4. Build the Chart
fig9 = px.bar(
    fig9_data, 
    x="Gender", 
    y="Count", 
    color=color_col if gender_choice != "All" else "Awareness Label",
    color_discrete_map=color_mapping,
    # This keeps the levels in the right order (High to Low)
    category_orders={"Awareness Label": [
        "5 - Extremely aware", "4 - Very aware", "3 - Moderately aware", "2 - Slightly aware", "1 - Not aware at all"
    ]},
    barmode="stack",
    title=f"Awareness Levels: {gender_choice} Participants"
)

fig9.update_layout(height=500, bargap=0.4, legend_title="Scale (Dark = High Awareness)")
st.plotly_chart(fig9, use_container_width=True)


# 10. Shopping Influence by Gender
st.subheader("10. Shopping Influence Factors")
fig10_data = df_gender.groupby(["Gender", "Influence on Shopping"]).size().reset_index(name="Count")

color_map = {'Female': '#FFB6C1', 'Male': '#ADD8E6'}

fig10 = px.bar(
    fig10_data, 
    x="Influence on Shopping", 
    y="Count", 
    color="Gender",           
    barmode='group',          
    color_discrete_map=color_map,
    title=f"Influence Factors: Comparison for {gender_choice}"
)

fig10.update_layout(
    height=500,
    xaxis_title="Influence Factor",
    yaxis_title="Count of Respondents",
    xaxis={'categoryorder':'total descending'} 
)
st.plotly_chart(fig10, use_container_width=True)
st.divider()

# --- SECTION B: Monthly Expenses Focus
st.subheader("📍 Section B: Expenditure & Employment Trends")
st.markdown("""
    This section investigates the link between professional status and monthly fashion spending, 
    and how high-spending groups are influenced differently.
""")

st.markdown("💡 Use the filter below to refine Monthly Expenditure (RM):")

# Rename to RM
rm_expense_order = [f"RM {item}" if "RM" not in str(item) else item for item in expense_order]
expense_choice = st.selectbox("Select Monthly Expenditure:", ["All"] + rm_expense_order, key="expense_filter_mid")

df_expense = df.copy()
# Ensure we strip 'RM ' when filtering if the original data doesn't have it
if expense_choice != "All":
    actual_value = expense_choice.replace("RM ", "")
    df_expense = df_expense[df_expense["Average Monthly Expenses (RM)"] == actual_value]

# 11. Distribution by Employment
st.subheader("11. Distribution of Spending by Employment (RM)")
fig11_data = df_expense.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
# Add RM to the data labels for the chart
fig11_data["Average Monthly Expenses (RM)"] = fig11_data["Average Monthly Expenses (RM)"].apply(lambda x: f"RM {x}")

if not fig11_data.empty:
    try:
        path_logic = ["Employment Status", "Average Monthly Expenses (RM)"] if expense_choice == "All" else ["Employment Status"]
        fig11 = px.treemap(
            fig11_data,
            path=path_logic,
            values="Count",
            color="Average Monthly Expenses (RM)" if expense_choice == "All" else "Employment Status",
            # Green Scale
            color_discrete_sequence=['#E8F5E9', '#A5D6A7', '#4CAF50', '#2E7D32', '#1B5E20'],
            title=f"Spending Power Distribution: {expense_choice}"
        )
        st.plotly_chart(fig11, use_container_width=True)
    except Exception:
        st.warning("Could not render Treemap for this selection.")

# 12. Influence by Spending Level (RM Labels) 
st.subheader("12. Influence by Spending Level (RM)")
fig12_data = df_expense.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count")
fig12_data["Average Monthly Expenses (RM)"] = fig12_data["Average Monthly Expenses (RM)"].apply(lambda x: f"RM {x}")

fig12 = px.bar(
    fig12_data, x="Count", y="Influence on Shopping", color="Average Monthly Expenses (RM)",
    orientation='h', barmode='stack',
    color_discrete_sequence=['#E8F5E9', '#A5D6A7', '#4CAF50', '#2E7D32', '#1B5E20'],
    title=f"Influence for {expense_choice} Category"
)
st.plotly_chart(fig12, use_container_width=True)
# --- SECTION B: Monthly Expenses Focus ---
st.subheader("📍 Section B: Expenditure & Employment Trends")

expenditure_colors = ['#FFF3E0', '#FFCC80', '#FFB74D', '#F57C00', '#E65100']
solid_color = ["#FB8C00"]

# 11. Distribution by Employment
st.subheader("11. Spending Power by Employment")

fig11_data = df_expense.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")
fig11_data["Average Monthly Expenses (RM)"] = fig11_data["Average Monthly Expenses (RM)"].apply(lambda x: f"RM {x}")

if not fig11_data.empty:
    path_logic = ["Employment Status", "Average Monthly Expenses (RM)"] if expense_choice == "All" else ["Employment Status"]
    
    fig11 = px.treemap(
        fig11_data,
        path=path_logic,
        values="Count",
        # Color by spending level if 'All', otherwise solid gold
        color="Average Monthly Expenses (RM)" if expense_choice == "All" else None,
        color_discrete_sequence=expenditure_colors if expense_choice == "All" else solid_gold,
        title=f"Spending Power Distribution: {expense_choice}"
    )
    st.plotly_chart(fig11, use_container_width=True)

# 12. Influence by Spending Level
st.subheader("12. Influence by Spending Level")

fig12_data = df_expense.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count")
fig12_data["Average Monthly Expenses (RM)"] = fig12_data["Average Monthly Expenses (RM)"].apply(lambda x: f"RM {x}")

fig12 = px.bar(
    fig12_data, 
    x="Count", 
    y="Influence on Shopping", 
    color="Average Monthly Expenses (RM)" if expense_choice == "All" else None,
    orientation='h', 
    barmode='stack',
    color_discrete_sequence=expenditure_colors if expense_choice == "All" else solid_gold,
    title=f"Influence Factors for {expense_choice}"
)

fig12.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig12, use_container_width=True)


st.subheader("📍 Section B: Expenditure & Employment Trends")

exp_palette = ['#FFF3E0', '#FFCC80', '#FFB74D', '#F57C00', '#E65100']
solid_orange = ["#F57C00"]

# Filter setup
rm_expense_order = [f"RM {item}" if "RM" not in str(item) else item for item in expense_order]
expense_choice = st.selectbox("Select Monthly Expenditure:", ["All"] + rm_expense_order, key="exp_filter_final_clean")

df_expense = df.copy()
if expense_choice != "All":
    actual_val = expense_choice.replace("RM ", "")
    df_expense = df_expense[df_expense["Average Monthly Expenses (RM)"] == actual_val]

# 11.reemap - Spending Power
st.subheader("11. Spending Power by Employment")
fig11_data = df_expense.groupby(["Employment Status", "Average Monthly Expenses (RM)"]).size().reset_index(name="Count")

# Sort color
fig11_data = fig11_data.sort_values("Average Monthly Expenses (RM)")
fig11_data["Display RM"] = fig11_data["Average Monthly Expenses (RM)"].apply(lambda x: f"RM {x}")

if not fig11_data.empty:
    path_logic = ["Employment Status", "Display RM"] if expense_choice == "All" else ["Employment Status"]
    fig11 = px.treemap(
        fig11_data,
        path=path_logic,
        values="Count",
        color="Display RM" if expense_choice == "All" else None,
        color_discrete_sequence=exp_palette if expense_choice == "All" else solid_orange,
        title=f"Spending Power Distribution: {expense_choice}"
    )
    fig11.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>")
    st.plotly_chart(fig11, use_container_width=True)


# 12. Influence by Spending Level
st.subheader("12. Influence by Spending Level")

fig12_data = df_expense.groupby(["Average Monthly Expenses (RM)", "Influence on Shopping"]).size().reset_index(name="Count")
fig12_data = fig12_data.sort_values("Average Monthly Expenses (RM)")
fig12_data["Display RM"] = fig12_data["Average Monthly Expenses (RM)"].apply(lambda x: f"RM {x}")

fig12 = px.bar(
    fig12_data, 
    x="Count", 
    y="Influence on Shopping", 
    color="Display RM" if expense_choice == "All" else None,
    orientation='h', 
    barmode='stack',
    color_discrete_sequence=exp_palette if expense_choice == "All" else solid_orange,
    title=f"Influence Factors for {expense_choice}"
)

totals = fig12_data.groupby("Influence on Shopping")["Count"].sum().reset_index()

fig12.add_scatter(
    x=totals["Count"],
    y=totals["Influence on Shopping"],
    mode='text',
    text=totals["Count"],
    textposition='middle right',
    showlegend=False,
    hoverinfo='skip' 
)
fig12.update_layout(
    yaxis={'categoryorder':'total ascending'}, 
    legend={'traceorder': 'normal'},
    xaxis={'range': [0, totals["Count"].max() * 1.15]} 
)

fig12.update_traces(hovertemplate="Factor: %{y}<br>Count in Category: %{x}<extra></extra>")
st.plotly_chart(fig12, use_container_width=True)
