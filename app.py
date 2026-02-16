"""
Flourish Collective Financial Dashboard
Updated: February 2026
Reads from Flourish_Financial_Tracker_2026_2030.xlsx
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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


def load_excel_data(uploaded_file):
    """Load data from uploaded Excel file."""
    try:
        xl = pd.ExcelFile(uploaded_file)
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

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Financial Tracker",
    type=['xlsx', 'xls'],
    help="Upload your Flourish_Financial_Tracker_2026_2030.xlsx file"
)

# Load data
if uploaded_file:
    data = load_excel_data(uploaded_file)
    if data:
        st.sidebar.success("✓ Data loaded successfully")
    else:
        st.sidebar.error("Failed to load data")
        data = None
else:
    data = None
    st.sidebar.info("📊 Upload your Financial Tracker to see your data")

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
        donors = safe_float(donors_row['FY26 Actual'].values[0]) if len(donors_row) > 0 else 0
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pct = (rev_ytd / rev_budget * 100) if rev_budget > 0 else 0
            st.metric("Revenue YTD", format_currency(rev_ytd), f"{pct:.0f}% of budget")
        
        with col2:
            pct = (exp_ytd / exp_budget * 100) if exp_budget > 0 else 0
            st.metric("Expenses YTD", format_currency(exp_ytd), f"{pct:.0f}% of budget")
        
        with col3:
            st.metric("Net Income YTD", format_currency(net_ytd),
                     "On track" if net_ytd >= 0 else "Below target",
                     delta_color="normal" if net_ytd >= 0 else "inverse")
        
        with col4:
            st.metric("Active Allies", f"{int(allies):,}" if allies > 0 else "—")
        
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
            st.subheader("Revenue by Category")
            # Get revenue line items (exclude totals)
            rev_items = df[df['Metric'].isin(['Community Contributions', 'Merchandise', 
                                              'Annual Gathering', 'Fundraising Events', 
                                              'Learning Events', 'Reimbursables/Misc'])]
            if len(rev_items) > 0:
                fig = px.pie(rev_items, values='FY26 Budget', names='Metric',
                            color_discrete_sequence=px.colors.sequential.Greens_r)
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        # Financial Summary Table
        st.markdown("---")
        st.subheader("Financial Summary")
        
        # Filter to main financial rows
        financial_rows = df[df['Metric'].isin([
            'Community Contributions', 'Merchandise', 'Annual Gathering', 
            'Fundraising Events', 'Learning Events', 'Reimbursables/Misc',
            'TOTAL REVENUE', '  Grantmaking', '  Development/Donor Care',
            '  Programs/Education', '  Overhead', 'TOTAL EXPENSES', 'NET INCOME'
        ])]
        
        if len(financial_rows) > 0:
            display_cols = ['Metric', 'FY26 Budget', 'FY26 Actual', 'FY26 % Plan']
            display_df = financial_rows[display_cols].copy()
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    else:
        st.info("👆 Upload your Financial Tracker file to see the Executive Dashboard")


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
            pct = safe_float(total_row['FY26 % Plan'].values[0])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("FY26 Budget", format_currency(budget))
            with col2:
                st.metric("YTD Actual", format_currency(ytd))
            with col3:
                st.metric("% of Budget", format_pct(pct))
        
        st.markdown("---")
        
        # Revenue breakdown
        col1, col2 = st.columns(2)
        
        # Filter to parent accounts only (not indented)
        parent_accounts = df[~df['Revenue Source'].str.startswith('  ', na=False)]
        parent_accounts = parent_accounts[parent_accounts['Revenue Source'] != 'TOTAL REVENUE']
        parent_accounts = parent_accounts.dropna(subset=['Revenue Source'])
        
        with col1:
            st.subheader("Budget Allocation")
            if len(parent_accounts) > 0:
                fig = px.pie(parent_accounts, values='FY26 Budget', names='Revenue Source',
                            color_discrete_sequence=px.colors.sequential.Greens_r)
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("YTD by Category")
            if len(parent_accounts) > 0:
                fig = px.bar(parent_accounts, x='Revenue Source', y='FY26 YTD',
                            color='FY26 YTD', color_continuous_scale='Greens')
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Historical trend
        st.markdown("---")
        st.subheader("Historical Revenue Trend")
        
        if 'TOTAL REVENUE' in df['Revenue Source'].values:
            total_row = df[df['Revenue Source'] == 'TOTAL REVENUE'].iloc[0]
            years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25']
            values = [safe_float(total_row.get(f'{y} Actual', 0)) for y in years]
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
        st.info("👆 Upload your Financial Tracker file to see Revenue Analysis")


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
            st.subheader("YTD by Category")
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
        st.info("👆 Upload your Financial Tracker file to see Expense Analysis")


# ============================================================
# PAGE: Community Growth
# ============================================================
elif page == "👥 Community Growth":
    st.title("👥 Community Growth")
    
    if data and 'executive' in data:
        df = data['executive']
        
        # Get community metrics
        metrics = {
            'Active Allies': '# Active Allies',
            'Donors': '# Donors',
            'Avg Donation': 'Average Donation ($)',
            '% Giving': '% Community Giving',
            'Growth %': 'Community Growth %'
        }
        
        values = {}
        for key, search in metrics.items():
            row = df[df['Metric'].str.contains(search, na=False)]
            if len(row) > 0:
                values[key] = {
                    'FY25': safe_float(row['FY25 Actual'].values[0]),
                    'FY26_Budget': safe_float(row['FY26 Budget'].values[0]) if 'FY26 Budget' in row.columns else 0,
                    'FY26_Actual': safe_float(row['FY26 Actual'].values[0]) if 'FY26 Actual' in row.columns else 0
                }
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            v = values.get('Active Allies', {})
            st.metric("Active Allies", 
                     f"{int(v.get('FY26_Actual', 0)):,}" if v.get('FY26_Actual', 0) > 0 else "—",
                     f"Target: {int(v.get('FY26_Budget', 0)):,}" if v.get('FY26_Budget', 0) > 0 else None)
        
        with col2:
            v = values.get('Donors', {})
            st.metric("Number of Donors",
                     f"{int(v.get('FY26_Actual', 0)):,}" if v.get('FY26_Actual', 0) > 0 else "—",
                     f"Target: {int(v.get('FY26_Budget', 0)):,}" if v.get('FY26_Budget', 0) > 0 else None)
        
        with col3:
            v = values.get('Avg Donation', {})
            st.metric("Average Donation",
                     f"${int(v.get('FY26_Actual', 0)):,}" if v.get('FY26_Actual', 0) > 0 else "—",
                     f"Target: ${int(v.get('FY26_Budget', 0)):,}" if v.get('FY26_Budget', 0) > 0 else None)
        
        with col4:
            v = values.get('% Giving', {})
            st.metric("% Giving",
                     f"{int(v.get('FY26_Actual', 0))}%" if v.get('FY26_Actual', 0) > 0 else "—",
                     f"Target: {int(v.get('FY26_Budget', 0))}%" if v.get('FY26_Budget', 0) > 0 else None)
        
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
                years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25']
                hist_values = [safe_float(row.get(y, 0)) for y in years]
                hist_values.append(safe_float(row.get('FY26 Actual', 0)))
                years.append('FY26 YTD')
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=years, y=hist_values, marker_color='#2E7D32'))
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Engagement Funnel")
            allies = values.get('Active Allies', {}).get('FY26_Actual', 0)
            donors = values.get('Donors', {}).get('FY26_Actual', 0)
            
            if allies > 0 or donors > 0:
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
                st.caption("Upload data to see engagement funnel")
    
    else:
        st.info("👆 Upload your Financial Tracker file to see Community Growth")


# ============================================================
# PAGE: Historical Trends
# ============================================================
elif page == "📈 Historical Trends":
    st.title("📈 Historical Trends")
    
    if data and 'executive' in data:
        df = data['executive']
        
        st.subheader("Revenue & Expense Trends (FY21-FY26)")
        
        years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25 Actual', 'FY26 Budget']
        year_cols = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25 Actual', 'FY26 Budget']
        
        total_rev = df[df['Metric'] == 'TOTAL REVENUE']
        total_exp = df[df['Metric'] == 'TOTAL EXPENSES']
        net_income = df[df['Metric'] == 'NET INCOME']
        
        if len(total_rev) > 0 and len(total_exp) > 0:
            rev_values = [safe_float(total_rev[c].values[0]) if c in total_rev.columns else 0 for c in year_cols]
            exp_values = [safe_float(total_exp[c].values[0]) if c in total_exp.columns else 0 for c in year_cols]
            net_values = [safe_float(net_income[c].values[0]) if c in net_income.columns else 0 for c in year_cols]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=rev_values, mode='lines+markers',
                                    name='Revenue', line=dict(color='#2E7D32', width=3)))
            fig.add_trace(go.Scatter(x=years, y=exp_values, mode='lines+markers',
                                    name='Expenses', line=dict(color='#1565C0', width=3)))
            fig.add_trace(go.Scatter(x=years, y=net_values, mode='lines+markers',
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
        
        for i, cat in enumerate(rev_categories):
            cat_row = df[df['Metric'] == cat]
            if len(cat_row) > 0:
                values = [safe_float(cat_row[c].values[0]) if c in cat_row.columns else 0 for c in year_cols]
                fig.add_trace(go.Bar(x=years, y=values, name=cat, marker_color=colors[i % len(colors)]))
        
        fig.update_layout(barmode='stack', height=400, yaxis_tickformat='$,.0f')
        st.plotly_chart(fig, use_container_width=True)
        
        # YoY Growth
        st.markdown("---")
        st.subheader("Year-over-Year Growth")
        
        if len(total_rev) > 0:
            row = total_rev.iloc[0]
            growth_data = []
            prev_val = None
            for i, (year, col) in enumerate(zip(years[:-1], year_cols[:-1])):
                val = safe_float(row.get(col, 0))
                if prev_val and prev_val > 0:
                    growth = ((val - prev_val) / prev_val) * 100
                    growth_data.append({'Year': year, 'Growth': growth})
                prev_val = val
            
            if growth_data:
                growth_df = pd.DataFrame(growth_data)
                fig = px.bar(growth_df, x='Year', y='Growth', 
                            color='Growth', color_continuous_scale='RdYlGn',
                            color_continuous_midpoint=0)
                fig.update_layout(height=300, yaxis_tickformat='.0f',
                                 yaxis_title='Growth %')
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("👆 Upload your Financial Tracker file to see Historical Trends")


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
    
    # 2030 Goals with current progress
    goals = [
        {'name': '$1M+ Grants Given', 'target': 1000000, 'current': 310000, 'unit': '$'},
        {'name': '1,000+ Active Allies', 'target': 1000, 'current': 272, 'unit': ''},
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
