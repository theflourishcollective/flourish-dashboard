"""
Flourish Collective Financial Dashboard
Updated: February 2026
Reads from Flourish_Financial_Tracker.xlsx in repo
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page config
st.set_page_config(
    page_title="Flourish Collective Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stMetric > div {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
    }
    h1 {color: #2E7D32;}
    h2 {color: #1565C0;}
    h3 {color: #2E7D32;}
</style>
""", unsafe_allow_html=True)


def safe_float(val, default=0):
    """Safely convert value to float."""
    try:
        if pd.isna(val) or val is None or val == '' or val == 'NA':
            return default
        return float(val)
    except (ValueError, TypeError):
        return default


def format_currency(val):
    """Format value as currency."""
    val = safe_float(val)
    if val < 0:
        return f"-${abs(val):,.0f}"
    return f"${val:,.0f}"


def format_pct(val):
    """Format value as percentage."""
    val = safe_float(val)
    if val == 0:
        return "0%"
    if abs(val) < 1:
        return f"{val:.0%}"
    return f"{val:.0f}%"


@st.cache_data
def load_excel_data(file_path_or_buffer):
    """Load data from Excel file."""
    try:
        xl = pd.ExcelFile(file_path_or_buffer)
        data = {}
        
        # Load Executive Dashboard
        if 'Executive Dashboard' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='Executive Dashboard', header=3)
            data['executive'] = df
        
        # Load Revenue Detail
        if 'Revenue Detail' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='Revenue Detail', header=2)
            data['revenue'] = df
        
        # Load Expense Detail
        if 'Expense Detail' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='Expense Detail', header=2)
            data['expense'] = df
        
        # Load Current Year
        if 'Current Year' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='Current Year', header=3)
            data['current_year'] = df
        
        # Load Progress Tracker
        if 'Progress Tracker' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='Progress Tracker', header=3)
            data['progress'] = df
        
        return data
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None


# Sidebar
st.sidebar.title("🌱 Flourish Collective")
st.sidebar.markdown("---")

# Load data from repo file
DATA_FILE = "Flourish_Financial_Tracker.xlsx"
data = None

if os.path.exists(DATA_FILE):
    data = load_excel_data(DATA_FILE)
    if data:
        st.sidebar.success("✓ Data loaded")
    else:
        st.sidebar.error("Error loading data file")
else:
    st.sidebar.error(f"Data file not found: {DATA_FILE}")

# Navigation
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Executive Summary", "💰 Revenue Analysis", "📉 Expense Analysis", 
     "👥 Community Growth", "📈 Historical Trends", "🎯 2030 Goals"]
)

st.sidebar.markdown("---")
st.sidebar.caption("The Flourish Collective © 2026")


# ============================================================
# PAGE: Executive Summary
# ============================================================
if page == "📊 Executive Summary":
    st.title("📊 Executive Dashboard")
    st.markdown("### FY26 Year-to-Date Performance")
    
    if data and 'executive' in data:
        df = data['executive']
        
        # Find key rows
        total_rev_row = df[df['Metric'] == 'TOTAL REVENUE']
        total_exp_row = df[df['Metric'] == 'TOTAL EXPENSES']
        net_income_row = df[df['Metric'] == 'NET INCOME']
        
        # Get values
        rev_budget = safe_float(total_rev_row['FY26 Budget'].values[0]) if len(total_rev_row) > 0 else 0
        rev_ytd = safe_float(total_rev_row['FY26 Actual'].values[0]) if len(total_rev_row) > 0 else 0
        exp_budget = safe_float(total_exp_row['FY26 Budget'].values[0]) if len(total_exp_row) > 0 else 0
        exp_ytd = safe_float(total_exp_row['FY26 Actual'].values[0]) if len(total_exp_row) > 0 else 0
        net_budget = safe_float(net_income_row['FY26 Budget'].values[0]) if len(net_income_row) > 0 else 0
        net_ytd = safe_float(net_income_row['FY26 Actual'].values[0]) if len(net_income_row) > 0 else 0
        
        # Community metrics
        allies_row = df[df['Metric'].str.contains('Active Allies', na=False)]
        donors_row = df[df['Metric'].str.contains('Donors', na=False)]
        
        allies = safe_float(allies_row['FY26 Actual'].values[0]) if len(allies_row) > 0 else 0
        allies_target = safe_float(allies_row['FY26 Budget'].values[0]) if len(allies_row) > 0 else 0
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pct = (rev_ytd / rev_budget * 100) if rev_budget > 0 else 0
            st.metric("Revenue Budget", format_currency(rev_budget))
            st.caption(f"YTD: {format_currency(rev_ytd)} ({pct:.0f}%)")
        
        with col2:
            pct = (exp_ytd / exp_budget * 100) if exp_budget > 0 else 0
            st.metric("Expense Budget", format_currency(exp_budget))
            st.caption(f"YTD: {format_currency(exp_ytd)} ({pct:.0f}%)")
        
        with col3:
            st.metric("Net Income Budget", format_currency(net_budget))
            st.caption(f"YTD: {format_currency(net_ytd)}")
        
        with col4:
            st.metric("Active Allies", f"{int(allies):,}" if allies > 0 else "—")
            st.caption(f"Target: {int(allies_target):,}" if allies_target > 0 else "")
        
        st.markdown("---")
        
        # Budget Overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("FY26 Budget Overview")
            budget_data = pd.DataFrame({
                'Category': ['Revenue', 'Expenses', 'Net Income'],
                'Budget': [rev_budget, exp_budget, net_budget],
                'YTD': [rev_ytd, exp_ytd, net_ytd]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Budget', x=budget_data['Category'], y=budget_data['Budget'],
                marker_color='#90CAF9'
            ))
            fig.add_trace(go.Bar(
                name='YTD Actual', x=budget_data['Category'], y=budget_data['YTD'],
                marker_color='#2E7D32'
            ))
            fig.update_layout(barmode='group', height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Revenue Budget by Category")
            # Get revenue line items (exclude totals and indented items)
            rev_items = df[df['Metric'].isin(['Community Contributions', 'Merchandise', 
                                              'Annual Gathering', 'Fundraising Events', 
                                              'Learning Events', 'Reimbursables/Misc'])]
            if len(rev_items) > 0:
                rev_items = rev_items[rev_items['FY26 Budget'] > 0]
                if len(rev_items) > 0:
                    fig = px.pie(rev_items, values='FY26 Budget', names='Metric',
                                color_discrete_sequence=px.colors.sequential.Greens_r)
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)
        
        # 2030 Goals Progress
        st.markdown("---")
        st.subheader("🎯 Progress Toward 2030 Goals")
        
        goals = [
            {'name': '$1M Grants', 'current': 310000, 'target': 1000000},
            {'name': '1K Allies', 'current': int(allies) if allies > 0 else 272, 'target': 1000},
            {'name': '50 Partners', 'current': 21, 'target': 50},
            {'name': '20K Engaged', 'current': 1800, 'target': 20000},
        ]
        
        cols = st.columns(4)
        for i, goal in enumerate(goals):
            with cols[i]:
                pct = (goal['current'] / goal['target'] * 100) if goal['target'] > 0 else 0
                st.markdown(f"**{goal['name']}**")
                st.progress(min(pct/100, 1.0))
                st.caption(f"{pct:.0f}% complete")
    
    else:
        st.warning("Unable to load Executive Dashboard data")


# ============================================================
# PAGE: Revenue Analysis
# ============================================================
elif page == "💰 Revenue Analysis":
    st.title("💰 Revenue Analysis")
    
    if data and 'revenue' in data:
        df = data['revenue']
        
        # Find total row
        total_row = df[df['Revenue Source'] == 'TOTAL REVENUE']
        
        if len(total_row) > 0:
            budget = safe_float(total_row['FY26 Budget'].values[0])
            ytd = safe_float(total_row['FY26 YTD'].values[0])
            pct = (ytd / budget * 100) if budget > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("FY26 Budget", format_currency(budget))
            with col2:
                st.metric("YTD Actual", format_currency(ytd))
            with col3:
                st.metric("% of Budget", f"{pct:.1f}%")
        
        st.markdown("---")
        
        # Revenue breakdown
        col1, col2 = st.columns(2)
        
        # Filter to parent accounts only (not indented)
        parent_accounts = df[~df['Revenue Source'].str.startswith('  ', na=False)]
        parent_accounts = parent_accounts[parent_accounts['Revenue Source'] != 'TOTAL REVENUE']
        parent_accounts = parent_accounts.dropna(subset=['Revenue Source'])
        parent_accounts = parent_accounts[parent_accounts['FY26 Budget'] > 0]
        
        with col1:
            st.subheader("Budget Allocation")
            if len(parent_accounts) > 0:
                fig = px.pie(parent_accounts, values='FY26 Budget', names='Revenue Source',
                            color_discrete_sequence=px.colors.sequential.Greens_r)
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Budget vs YTD")
            if len(parent_accounts) > 0:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='Budget', x=parent_accounts['Revenue Source'], 
                    y=parent_accounts['FY26 Budget'], marker_color='#90EE90'
                ))
                fig.add_trace(go.Bar(
                    name='YTD', x=parent_accounts['Revenue Source'], 
                    y=parent_accounts['FY26 YTD'], marker_color='#2E7D32'
                ))
                fig.update_layout(barmode='group', height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        # Historical trend
        st.markdown("---")
        st.subheader("Historical Revenue Trend")
        
        if 'TOTAL REVENUE' in df['Revenue Source'].values:
            total_row = df[df['Revenue Source'] == 'TOTAL REVENUE'].iloc[0]
            years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25']
            col_names = ['FY21 Actual', 'FY22 Actual', 'FY23 Actual', 'FY24 Actual', 'FY25 Actual']
            values = [safe_float(total_row.get(c, 0)) for c in col_names]
            values.append(safe_float(total_row.get('FY26 Budget', 0)))
            years.append('FY26 Budget')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=values, mode='lines+markers',
                                    line=dict(color='#2E7D32', width=3),
                                    marker=dict(size=10)))
            fig.update_layout(height=300, yaxis_tickformat='$,.0f')
            st.plotly_chart(fig, use_container_width=True)
        
        # Detail table
        st.subheader("Revenue Detail")
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    else:
        st.warning("Unable to load Revenue Detail data")


# ============================================================
# PAGE: Expense Analysis
# ============================================================
elif page == "📉 Expense Analysis":
    st.title("📉 Expense Analysis")
    
    if data and 'expense' in data:
        df = data['expense']
        
        # Find total row
        total_row = df[df['Expense Category'] == 'TOTAL EXPENSES']
        
        if len(total_row) > 0:
            budget = safe_float(total_row['FY26 Budget'].values[0])
            ytd = safe_float(total_row['FY26 YTD'].values[0])
            remaining = budget - ytd
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("FY26 Budget", format_currency(budget))
            with col2:
                st.metric("YTD Actual", format_currency(ytd))
            with col3:
                st.metric("Remaining", format_currency(remaining),
                         "Under budget" if remaining > 0 else "Over budget",
                         delta_color="normal" if remaining > 0 else "inverse")
        
        st.markdown("---")
        
        # Expense breakdown by category
        col1, col2 = st.columns(2)
        
        # Get category subtotals
        subtotals = df[df['Expense Category'].str.contains('Subtotal', na=False)]
        
        with col1:
            st.subheader("Budget by Category")
            if len(subtotals) > 0:
                fig = px.pie(subtotals, values='FY26 Budget', names='Expense Category',
                            color_discrete_sequence=px.colors.sequential.Blues_r)
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Budget vs YTD by Category")
            if len(subtotals) > 0:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    y=subtotals['Expense Category'], x=subtotals['FY26 Budget'],
                    name='Budget', orientation='h', marker_color='#90CAF9'
                ))
                fig.add_trace(go.Bar(
                    y=subtotals['Expense Category'], x=subtotals['FY26 YTD'],
                    name='YTD', orientation='h', marker_color='#1565C0'
                ))
                fig.update_layout(barmode='group', height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        # Detail table
        st.markdown("---")
        st.subheader("Expense Detail")
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    else:
        st.warning("Unable to load Expense Detail data")


# ============================================================
# PAGE: Community Growth
# ============================================================
elif page == "👥 Community Growth":
    st.title("👥 Community Growth")
    
    if data and 'executive' in data:
        df = data['executive']
        
        # Get community metrics
        def get_metric(search_term, col):
            row = df[df['Metric'].str.contains(search_term, na=False)]
            if len(row) > 0 and col in row.columns:
                return safe_float(row[col].values[0])
            return 0
        
        allies_actual = get_metric('Active Allies', 'FY26 Actual')
        allies_target = get_metric('Active Allies', 'FY26 Budget')
        donors_actual = get_metric('Donors', 'FY26 Actual')
        donors_target = get_metric('Donors', 'FY26 Budget')
        avg_donation_actual = get_metric('Average Donation', 'FY26 Actual')
        avg_donation_target = get_metric('Average Donation', 'FY26 Budget')
        giving_pct_actual = get_metric('Community Giving', 'FY26 Actual')
        giving_pct_target = get_metric('Community Giving', 'FY26 Budget')
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Allies", 
                     f"{int(allies_actual):,}" if allies_actual > 0 else "—",
                     f"Target: {int(allies_target):,}" if allies_target > 0 else None)
        
        with col2:
            st.metric("Number of Donors",
                     f"{int(donors_actual):,}" if donors_actual > 0 else "—",
                     f"Target: {int(donors_target):,}" if donors_target > 0 else None)
        
        with col3:
            st.metric("Average Donation",
                     f"${int(avg_donation_actual):,}" if avg_donation_actual > 0 else "—",
                     f"Target: ${int(avg_donation_target):,}" if avg_donation_target > 0 else None)
        
        with col4:
            st.metric("% Giving",
                     f"{int(giving_pct_actual)}%" if giving_pct_actual > 0 else "—",
                     f"Target: {int(giving_pct_target)}%" if giving_pct_target > 0 else None)
        
        st.markdown("---")
        
        # Key insight
        st.info("📊 **Key Insight:** 60% of people who attend 4 events become donors. 100% who attend 6+ events become regular givers.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Community Growth Over Time")
            # Historical data
            community_row = df[df['Metric'].str.contains('Active Allies', na=False)]
            if len(community_row) > 0:
                row = community_row.iloc[0]
                years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26']
                hist_values = [safe_float(row.get(y, 0)) for y in years[:-1]]
                hist_values.append(safe_float(row.get('FY26 Actual', 0)))
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=years, y=hist_values, marker_color='#2E7D32'))
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Engagement Funnel")
            allies = allies_actual if allies_actual > 0 else 272
            donors = donors_actual if donors_actual > 0 else 162
            
            funnel_data = {
                'Stage': ['Community Members', 'Active Allies', 'Donors', 'Regular Givers'],
                'Count': [int(allies * 1.5), int(allies), int(donors), int(donors * 0.6)]
            }
            fig = go.Figure(go.Funnel(
                y=funnel_data['Stage'],
                x=funnel_data['Count'],
                marker=dict(color=['#81C784', '#66BB6A', '#4CAF50', '#2E7D32'])
            ))
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Unable to load Community Growth data")


# ============================================================
# PAGE: Historical Trends
# ============================================================
elif page == "📈 Historical Trends":
    st.title("📈 Historical Trends")
    
    if data and 'executive' in data:
        df = data['executive']
        
        st.subheader("Revenue & Expense Trends (FY21-FY26)")
        
        years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26']
        
        total_rev = df[df['Metric'] == 'TOTAL REVENUE']
        total_exp = df[df['Metric'] == 'TOTAL EXPENSES']
        net_income = df[df['Metric'] == 'NET INCOME']
        
        if len(total_rev) > 0 and len(total_exp) > 0:
            rev_row = total_rev.iloc[0]
            exp_row = total_exp.iloc[0]
            net_row = net_income.iloc[0] if len(net_income) > 0 else None
            
            rev_values = [safe_float(rev_row.get(y, 0)) for y in years[:-1]]
            rev_values.append(safe_float(rev_row.get('FY26 Budget', 0)))
            
            exp_values = [safe_float(exp_row.get(y, 0)) for y in years[:-1]]
            exp_values.append(safe_float(exp_row.get('FY26 Budget', 0)))
            
            net_values = []
            if net_row is not None:
                net_values = [safe_float(net_row.get(y, 0)) for y in years[:-1]]
                net_values.append(safe_float(net_row.get('FY26 Budget', 0)))
            
            display_years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26 Budget']
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=display_years, y=rev_values, mode='lines+markers',
                                    name='Revenue', line=dict(color='#2E7D32', width=3)))
            fig.add_trace(go.Scatter(x=display_years, y=exp_values, mode='lines+markers',
                                    name='Expenses', line=dict(color='#1565C0', width=3)))
            if net_values:
                fig.add_trace(go.Scatter(x=display_years, y=net_values, mode='lines+markers',
                                        name='Net Income', line=dict(color='#FFA000', width=3)))
            fig.update_layout(height=400, yaxis_tickformat='$,.0f',
                            legend=dict(orientation="h", yanchor="bottom", y=1.02))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Revenue breakdown over time
        st.subheader("Revenue Sources Over Time")
        
        rev_categories = ['Community Contributions', 'Fundraising Events', 'Annual Gathering', 
                         'Learning Events', 'Merchandise']
        
        fig = go.Figure()
        colors = ['#2E7D32', '#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9']
        display_years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26 Budget']
        
        for i, cat in enumerate(rev_categories):
            cat_row = df[df['Metric'] == cat]
            if len(cat_row) > 0:
                row = cat_row.iloc[0]
                values = [safe_float(row.get(y, 0)) for y in years[:-1]]
                values.append(safe_float(row.get('FY26 Budget', 0)))
                fig.add_trace(go.Bar(x=display_years, y=values, name=cat, marker_color=colors[i % len(colors)]))
        
        fig.update_layout(barmode='stack', height=400, yaxis_tickformat='$,.0f')
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Unable to load Historical data")


# ============================================================
# PAGE: 2030 Goals
# ============================================================
elif page == "🎯 2030 Goals":
    st.title("🎯 2030 Strategic Goals")
    
    st.markdown("""
    ### The Flourish Collective's Vision for 2030
    Building a powerful, sustainable community of allies while giving **$1 Million** 
    in unrestricted grants to justice organizations led by people of color.
    """)
    
    st.markdown("---")
    
    # Get current allies count if available
    allies_current = 272
    if data and 'executive' in data:
        df = data['executive']
        allies_row = df[df['Metric'].str.contains('Active Allies', na=False)]
        if len(allies_row) > 0:
            val = safe_float(allies_row['FY26 Actual'].values[0])
            if val > 0:
                allies_current = int(val)
    
    # 2030 Goals with current progress
    goals = [
        {'name': '$1M+ Grants Given', 'target': 1000000, 'current': 310000, 'unit': '$'},
        {'name': '1,000+ Active Allies', 'target': 1000, 'current': allies_current, 'unit': ''},
        {'name': '50 Impact Partners', 'target': 50, 'current': 21, 'unit': ''},
        {'name': '20,000 Individuals Engaged', 'target': 20000, 'current': 1800, 'unit': ''},
    ]
    
    for goal in goals:
        pct = (goal['current'] / goal['target']) * 100 if goal['target'] > 0 else 0
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"### {goal['name']}")
            if goal['unit'] == '$':
                st.metric("Current", f"${goal['current']:,}")
                st.metric("Target", f"${goal['target']:,}")
            else:
                st.metric("Current", f"{goal['current']:,}")
                st.metric("Target", f"{goal['target']:,}")
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Progress %"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2E7D32"},
                    'steps': [
                        {'range': [0, 33], 'color': "#FFCDD2"},
                        {'range': [33, 66], 'color': "#FFF9C4"},
                        {'range': [66, 100], 'color': "#C8E6C9"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(t=50, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
    
    # Projection chart
    st.subheader("📈 Projected Path to $1M in Grants")
    
    years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26', 'FY27', 'FY28', 'FY29', 'FY30']
    cumulative = [80000, 136000, 193000, 273000, 310000, 360000, 520000, 700000, 900000, 1000000]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=cumulative,
        mode='lines+markers',
        name='Cumulative Grants',
        line=dict(color='#7B1FA2', width=3),
        marker=dict(size=10)
    ))
    fig.add_hline(y=1000000, line_dash="dash", line_color="green",
                  annotation_text="$1M Goal")
    fig.update_layout(
        height=400,
        yaxis_title='Cumulative Grants ($)',
        yaxis_tickformat='$,.0f'
    )
    st.plotly_chart(fig, use_container_width=True)


# Footer
st.markdown("---")
st.caption("🌱 The Flourish Collective — Building Allies & Investing in Leaders for Racial Justice")
