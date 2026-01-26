import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Flourish Collective Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f7f0;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #2E7D32;
    }
    .stMetric > div {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
    }
    h1 {color: #2E7D32;}
    h2 {color: #1565C0;}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data(file_path):
    """Load all sheets from the Excel file"""
    data = {}
    
    # Dashboard summary
    df = pd.read_excel(file_path, sheet_name='Dashboard_Data', header=None)
    summary = df.iloc[4:28, 0:6].copy()
    summary.columns = ['Metric', 'Current', 'Target', 'Pct_Target', 'Prior_Year', 'YoY_Change']
    summary = summary[summary['Metric'].notna()]
    data['summary'] = summary
    
    # Monthly Revenue
    df = pd.read_excel(file_path, sheet_name='Monthly_Revenue', header=None)
    revenue = df.iloc[2:12, 0:16].copy()
    revenue.columns = ['Category', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'YTD', 'Budget', 'Pct']
    revenue = revenue[revenue['Category'].notna() & (revenue['Category'] != 'Category')]
    data['revenue'] = revenue
    
    # Monthly Expenses
    df = pd.read_excel(file_path, sheet_name='Monthly_Expenses', header=None)
    expenses = df.iloc[2:8, 0:16].copy()
    expenses.columns = ['Category', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'YTD', 'Budget', 'Pct']
    expenses = expenses[expenses['Category'].notna() & (expenses['Category'] != 'Category')]
    data['expenses'] = expenses
    
    # Community Metrics
    df = pd.read_excel(file_path, sheet_name='Community_Metrics', header=None)
    community = df.iloc[2:11, 0:13].copy()
    community.columns = ['Metric', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    community = community[community['Metric'].notna() & (community['Metric'] != 'Metric')]
    data['community'] = community
    
    # Historical Data
    df = pd.read_excel(file_path, sheet_name='Historical_Data', header=None)
    historical = df.iloc[2:17, 0:6].copy()
    historical.columns = ['Metric', 'FY21', 'FY22', 'FY23', 'FY24', 'FY25']
    historical = historical[historical['Metric'].notna() & (historical['Metric'] != 'Metric')]
    data['historical'] = historical
    
    # 2030 Goals
    df = pd.read_excel(file_path, sheet_name='Goals_2030', header=None)
    goals = df.iloc[2:7, 0:5].copy()
    goals.columns = ['Goal', 'Target', 'Current', 'Pct_Complete', 'Remaining']
    goals = goals[goals['Goal'].notna() & (goals['Goal'] != 'Goal')]
    data['goals'] = goals
    
    return data

# File uploader or default file
st.sidebar.image("https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/leaflet.svg", width=50)
st.sidebar.title("🌱 Flourish Collective")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("Upload Data File", type=['xlsx'])

if uploaded_file:
    data = load_data(uploaded_file)
else:
    try:
        data = load_data('Flourish_Dashboard_Data_Template.xlsx')
    except:
        st.error("Please upload the Flourish_Dashboard_Data_Template.xlsx file")
        st.stop()

# Sidebar navigation
page = st.sidebar.radio("Navigate", [
    "📊 Executive Summary",
    "💰 Revenue Analysis", 
    "📉 Expense Analysis",
    "👥 Community Growth",
    "📈 Historical Trends",
    "🎯 2030 Goals"
])

st.sidebar.markdown("---")
st.sidebar.markdown("*Data updates when you upload a new file*")

# Helper functions
def format_currency(val):
    if pd.isna(val) or val == 0:
        return "$0"
    return f"${val:,.0f}"

def format_pct(val):
    if pd.isna(val):
        return "0%"
    return f"{val:.0%}" if val < 1 else f"{val:.0f}%"

def safe_float(val, default=0):
    try:
        if pd.isna(val):
            return default
        return float(val)
    except:
        return default

# ============================================================
# PAGE: Executive Summary
# ============================================================
if page == "📊 Executive Summary":
    st.title("📊 Executive Dashboard")
    st.markdown("### FY26 Year-to-Date Performance")
    
    summary = data['summary']
    
    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    # Get values safely
    revenue_ytd = safe_float(summary[summary['Metric'] == 'Total Revenue YTD']['Current'].values[0] if len(summary[summary['Metric'] == 'Total Revenue YTD']) > 0 else 0)
    revenue_target = safe_float(summary[summary['Metric'] == 'Total Revenue YTD']['Target'].values[0] if len(summary[summary['Metric'] == 'Total Revenue YTD']) > 0 else 507000, 507000)
    
    expense_ytd = safe_float(summary[summary['Metric'] == 'Total Expenses YTD']['Current'].values[0] if len(summary[summary['Metric'] == 'Total Expenses YTD']) > 0 else 0)
    expense_target = safe_float(summary[summary['Metric'] == 'Total Expenses YTD']['Target'].values[0] if len(summary[summary['Metric'] == 'Total Expenses YTD']) > 0 else 478848, 478848)
    
    net_income = revenue_ytd - expense_ytd
    net_target = revenue_target - expense_target
    
    community_size = safe_float(summary[summary['Metric'] == 'Active Community Size']['Current'].values[0] if len(summary[summary['Metric'] == 'Active Community Size']) > 0 else 0)
    
    with col1:
        st.metric("Total Revenue YTD", format_currency(revenue_ytd), 
                  f"{(revenue_ytd/revenue_target*100):.0f}% of target" if revenue_target > 0 else None)
    with col2:
        st.metric("Total Expenses YTD", format_currency(expense_ytd),
                  f"{(expense_ytd/expense_target*100):.0f}% of budget" if expense_target > 0 else None)
    with col3:
        st.metric("Net Income YTD", format_currency(net_income),
                  "On track" if net_income >= 0 else "Below target", 
                  delta_color="normal" if net_income >= 0 else "inverse")
    with col4:
        st.metric("Active Community", f"{community_size:,.0f}",
                  "Growing" if community_size > 272 else None)
    
    st.markdown("---")
    
    # Revenue vs Expenses chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue vs Budget")
        revenue_df = data['revenue'][data['revenue']['Category'] != 'TOTAL'].copy()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='YTD Actual',
            x=revenue_df['Category'],
            y=revenue_df['YTD'].fillna(0),
            marker_color='#2E7D32'
        ))
        fig.add_trace(go.Bar(
            name='Budget',
            x=revenue_df['Category'],
            y=revenue_df['Budget'].fillna(0),
            marker_color='#90EE90'
        ))
        fig.update_layout(barmode='group', height=400, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Expenses vs Budget")
        expense_df = data['expenses'][data['expenses']['Category'] != 'TOTAL'].copy()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='YTD Actual',
            x=expense_df['Category'],
            y=expense_df['YTD'].fillna(0),
            marker_color='#1565C0'
        ))
        fig.add_trace(go.Bar(
            name='Budget',
            x=expense_df['Category'],
            y=expense_df['Budget'].fillna(0),
            marker_color='#90CAF9'
        ))
        fig.update_layout(barmode='group', height=400, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # 2030 Goals Progress
    st.markdown("---")
    st.subheader("🎯 Progress Toward 2030 Goals")
    
    goals = data['goals']
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(goals.iterrows()):
        with cols[i % 4]:
            pct = safe_float(row['Pct_Complete'], 0)
            if pct < 1:
                pct = pct * 100
            st.markdown(f"**{row['Goal']}**")
            st.progress(min(pct/100, 1.0))
            st.caption(f"{pct:.1f}% complete")

# ============================================================
# PAGE: Revenue Analysis
# ============================================================
elif page == "💰 Revenue Analysis":
    st.title("💰 Revenue Analysis")
    
    revenue = data['revenue'].copy()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Summary metrics
    total_row = revenue[revenue['Category'] == 'TOTAL']
    if len(total_row) > 0:
        ytd_total = safe_float(total_row['YTD'].values[0])
        budget_total = safe_float(total_row['Budget'].values[0], 507000)
    else:
        ytd_total = revenue['YTD'].fillna(0).sum()
        budget_total = revenue['Budget'].fillna(0).sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("YTD Revenue", format_currency(ytd_total))
    with col2:
        st.metric("Annual Budget", format_currency(budget_total))
    with col3:
        pct = (ytd_total / budget_total * 100) if budget_total > 0 else 0
        st.metric("% of Budget", f"{pct:.1f}%")
    
    st.markdown("---")
    
    # Monthly trend
    st.subheader("Monthly Revenue Trend")
    
    revenue_detail = revenue[revenue['Category'] != 'TOTAL'].copy()
    monthly_totals = []
    for month in months:
        monthly_totals.append(revenue_detail[month].fillna(0).sum())
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=monthly_totals,
        mode='lines+markers',
        name='Monthly Revenue',
        line=dict(color='#2E7D32', width=3),
        marker=dict(size=10)
    ))
    
    # Add cumulative line
    cumulative = pd.Series(monthly_totals).cumsum()
    fig.add_trace(go.Scatter(
        x=months, y=cumulative,
        mode='lines+markers',
        name='Cumulative',
        line=dict(color='#FFA726', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=400,
        yaxis=dict(title='Monthly Revenue'),
        yaxis2=dict(title='Cumulative', overlaying='y', side='right'),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue by category
    st.subheader("Revenue by Category")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            revenue_detail, 
            values='Budget', 
            names='Category',
            title='Budget Allocation',
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        ytd_values = revenue_detail['YTD'].fillna(0)
        if ytd_values.sum() > 0:
            fig = px.pie(
                revenue_detail,
                values='YTD',
                names='Category', 
                title='YTD Actual',
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
        else:
            fig = go.Figure()
            fig.add_annotation(text="No YTD data yet", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            fig.update_layout(title='YTD Actual')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detail table
    st.subheader("Revenue Detail")
    display_df = revenue[['Category', 'YTD', 'Budget', 'Pct']].copy()
    display_df['YTD'] = display_df['YTD'].apply(lambda x: format_currency(safe_float(x)))
    display_df['Budget'] = display_df['Budget'].apply(lambda x: format_currency(safe_float(x)))
    display_df['Pct'] = display_df['Pct'].apply(lambda x: format_pct(safe_float(x)))
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ============================================================
# PAGE: Expense Analysis
# ============================================================
elif page == "📉 Expense Analysis":
    st.title("📉 Expense Analysis")
    
    expenses = data['expenses'].copy()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Summary metrics
    total_row = expenses[expenses['Category'] == 'TOTAL']
    if len(total_row) > 0:
        ytd_total = safe_float(total_row['YTD'].values[0])
        budget_total = safe_float(total_row['Budget'].values[0], 478848)
    else:
        ytd_total = expenses['YTD'].fillna(0).sum()
        budget_total = expenses['Budget'].fillna(0).sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("YTD Expenses", format_currency(ytd_total))
    with col2:
        st.metric("Annual Budget", format_currency(budget_total))
    with col3:
        remaining = budget_total - ytd_total
        st.metric("Remaining Budget", format_currency(remaining),
                  "Under budget" if remaining > 0 else "Over budget",
                  delta_color="normal" if remaining > 0 else "inverse")
    
    st.markdown("---")
    
    # Monthly trend
    st.subheader("Monthly Expense Trend")
    
    expense_detail = expenses[expenses['Category'] != 'TOTAL'].copy()
    monthly_totals = []
    for month in months:
        monthly_totals.append(expense_detail[month].fillna(0).sum())
    
    # Monthly budget line (equal distribution)
    monthly_budget = budget_total / 12
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months, y=monthly_totals,
        name='Monthly Expenses',
        marker_color='#1565C0'
    ))
    fig.add_trace(go.Scatter(
        x=months, y=[monthly_budget]*12,
        mode='lines',
        name='Monthly Budget',
        line=dict(color='#FF5722', width=2, dash='dash')
    ))
    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    # Expense breakdown
    st.subheader("Expense Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            expense_detail,
            values='Budget',
            names='Category',
            title='Budget by Category',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Budget vs Actual horizontal bar
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=expense_detail['Category'],
            x=expense_detail['YTD'].fillna(0),
            name='YTD Actual',
            orientation='h',
            marker_color='#1565C0'
        ))
        fig.add_trace(go.Bar(
            y=expense_detail['Category'],
            x=expense_detail['Budget'].fillna(0),
            name='Budget',
            orientation='h',
            marker_color='#90CAF9'
        ))
        fig.update_layout(barmode='group', height=350, title='Budget vs Actual')
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: Community Growth
# ============================================================
elif page == "👥 Community Growth":
    st.title("👥 Community Growth")
    
    community = data['community'].copy()
    summary = data['summary']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Current metrics
    col1, col2, col3, col4 = st.columns(4)
    
    comm_size = safe_float(summary[summary['Metric'] == 'Active Community Size']['Current'].values[0] if len(summary[summary['Metric'] == 'Active Community Size']) > 0 else 272)
    donors = safe_float(summary[summary['Metric'] == 'Number of Donors']['Current'].values[0] if len(summary[summary['Metric'] == 'Number of Donors']) > 0 else 162)
    avg_donation = safe_float(summary[summary['Metric'] == 'Average Donation']['Current'].values[0] if len(summary[summary['Metric'] == 'Average Donation']) > 0 else 1279)
    
    with col1:
        st.metric("Active Community", f"{comm_size:,.0f}", "Target: 330")
    with col2:
        st.metric("Number of Donors", f"{donors:,.0f}", "Target: 162")
    with col3:
        st.metric("Average Donation", f"${avg_donation:,.0f}", "Target: $1,279")
    with col4:
        giving_pct = donors / comm_size * 100 if comm_size > 0 else 0
        st.metric("% Community Giving", f"{giving_pct:.0f}%", "Target: 60%")
    
    st.markdown("---")
    
    # Community size trend
    st.subheader("Community Growth Over Time")
    
    size_row = community[community['Metric'] == 'Active Community Size']
    if len(size_row) > 0:
        monthly_sizes = [safe_float(size_row[m].values[0]) for m in months]
    else:
        monthly_sizes = [0] * 12
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=monthly_sizes,
        mode='lines+markers+text',
        name='Community Size',
        line=dict(color='#2E7D32', width=3),
        marker=dict(size=12),
        text=[f"{int(v)}" if v > 0 else "" for v in monthly_sizes],
        textposition='top center'
    ))
    fig.update_layout(height=400, yaxis_title='Active Members')
    st.plotly_chart(fig, use_container_width=True)
    
    # Engagement funnel
    st.subheader("Engagement Funnel")
    st.info("📊 **Key Insight:** 60% of people who attend 4 events become donors. 100% who attend 6+ events become regular givers.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Funnel visualization
        funnel_data = {
            'Stage': ['Event Attendees', 'Repeat Attendees (4+)', 'Donors', 'Regular Givers'],
            'Count': [190, 80, donors, donors * 0.6]
        }
        fig = go.Figure(go.Funnel(
            y=funnel_data['Stage'],
            x=funnel_data['Count'],
            marker=dict(color=['#81C784', '#66BB6A', '#4CAF50', '#2E7D32'])
        ))
        fig.update_layout(height=350, title='Engagement Funnel')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # New members trend
        new_members_row = community[community['Metric'] == 'New Members Added']
        if len(new_members_row) > 0:
            new_members = [safe_float(new_members_row[m].values[0]) for m in months]
        else:
            new_members = [0] * 12
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months, y=new_members,
            name='New Members',
            marker_color='#4CAF50'
        ))
        fig.update_layout(height=350, title='New Members by Month')
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: Historical Trends
# ============================================================
elif page == "📈 Historical Trends":
    st.title("📈 Historical Trends (FY21-FY25)")
    
    historical = data['historical'].copy()
    years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25']
    
    # Revenue & Expense trend
    st.subheader("Financial Performance")
    
    rev_row = historical[historical['Metric'] == 'Total Revenue']
    exp_row = historical[historical['Metric'] == 'Total Expenses']
    net_row = historical[historical['Metric'] == 'Net Income']
    
    revenues = [safe_float(rev_row[y].values[0]) for y in years] if len(rev_row) > 0 else [0]*5
    expenses = [safe_float(exp_row[y].values[0]) for y in years] if len(exp_row) > 0 else [0]*5
    net_income = [safe_float(net_row[y].values[0]) for y in years] if len(net_row) > 0 else [0]*5
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=years, y=revenues,
        name='Revenue',
        marker_color='#2E7D32'
    ), secondary_y=False)
    
    fig.add_trace(go.Bar(
        x=years, y=expenses,
        name='Expenses',
        marker_color='#1565C0'
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=years, y=net_income,
        name='Net Income',
        mode='lines+markers',
        line=dict(color='#FF5722', width=3),
        marker=dict(size=10)
    ), secondary_y=True)
    
    fig.update_layout(
        height=450,
        barmode='group',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    fig.update_yaxes(title_text="Revenue / Expenses ($)", secondary_y=False)
    fig.update_yaxes(title_text="Net Income ($)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Community Growth
    st.subheader("Community Growth")
    
    col1, col2 = st.columns(2)
    
    with col1:
        comm_row = historical[historical['Metric'] == 'Active Community Size']
        comm_sizes = [safe_float(comm_row[y].values[0]) for y in years] if len(comm_row) > 0 else [0]*5
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=comm_sizes,
            mode='lines+markers',
            name='Community Size',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=12),
            fill='tozeroy',
            fillcolor='rgba(76, 175, 80, 0.2)'
        ))
        fig.update_layout(height=350, title='Active Community Size')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        donor_row = historical[historical['Metric'] == 'Number of Donors']
        avg_row = historical[historical['Metric'] == 'Average Donation']
        
        donors = [safe_float(donor_row[y].values[0]) for y in years] if len(donor_row) > 0 else [0]*5
        avg_donations = [safe_float(avg_row[y].values[0]) for y in years] if len(avg_row) > 0 else [0]*5
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=years, y=donors,
            name='Donors',
            marker_color='#66BB6A'
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=years, y=avg_donations,
            name='Avg Donation',
            mode='lines+markers',
            line=dict(color='#FFA726', width=2)
        ), secondary_y=True)
        fig.update_layout(height=350, title='Donors & Average Donation')
        fig.update_yaxes(title_text="# Donors", secondary_y=False)
        fig.update_yaxes(title_text="Avg Donation ($)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Cumulative grants
    st.subheader("Cumulative Grants Awarded")
    
    grants_row = historical[historical['Metric'] == 'Cumulative Grants']
    grants = [safe_float(grants_row[y].values[0]) for y in years] if len(grants_row) > 0 else [0]*5
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=grants,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#7B1FA2', width=3),
        fillcolor='rgba(123, 31, 162, 0.2)'
    ))
    fig.add_hline(y=1000000, line_dash="dash", line_color="red", 
                  annotation_text="2030 Goal: $1M")
    fig.update_layout(height=350, yaxis_title='Cumulative Grants ($)')
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: 2030 Goals
# ============================================================
elif page == "🎯 2030 Goals":
    st.title("🎯 2030 Strategic Goals")
    
    goals = data['goals'].copy()
    
    st.markdown("""
    ### The Flourish Collective's vision for 2030:
    Building a powerful, sustainable community of allies while giving **$1 Million** in unrestricted grants to justice organizations led by people of color.
    """)
    
    st.markdown("---")
    
    # Goal cards
    for _, row in goals.iterrows():
        col1, col2 = st.columns([2, 3])
        
        target = safe_float(row['Target'])
        current = safe_float(row['Current'])
        pct = safe_float(row['Pct_Complete'])
        if pct < 1:
            pct = pct * 100
        remaining = safe_float(row['Remaining'])
        
        with col1:
            st.markdown(f"### {row['Goal']}")
            st.metric("Current", f"{current:,.0f}" if current < 100000 else f"${current:,.0f}")
            st.metric("Target", f"{target:,.0f}" if target < 100000 else f"${target:,.0f}")
        
        with col2:
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pct,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Progress"},
                delta={'reference': 100, 'relative': False},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2E7D32"},
                    'steps': [
                        {'range': [0, 33], 'color': "#FFCDD2"},
                        {'range': [33, 66], 'color': "#FFF9C4"},
                        {'range': [66, 100], 'color': "#C8E6C9"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 100
                    }
                }
            ))
            fig.update_layout(height=250, margin=dict(t=50, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
    
    # Projection to 2030
    st.subheader("📊 Projection to 2030")
    
    years_proj = ['FY25', 'FY26', 'FY27', 'FY28', 'FY29', 'FY30']
    
    # Get cumulative grants from goals
    current_grants = 303946
    grant_projections = [current_grants, 353946, 513946, 693946, 913946, 1000000]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years_proj, y=grant_projections,
        mode='lines+markers',
        name='Projected Grants',
        line=dict(color='#7B1FA2', width=3),
        marker=dict(size=12)
    ))
    fig.add_hline(y=1000000, line_dash="dash", line_color="green",
                  annotation_text="$1M Goal")
    fig.update_layout(
        height=400,
        title='Projected Path to $1M in Grants',
        yaxis_title='Cumulative Grants ($)',
        yaxis_tickformat='$,.0f'
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*🌱 The Flourish Collective — Building Allies & Investing in Leaders for Racial Justice*")
