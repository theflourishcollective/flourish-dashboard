"""
Flourish Collective Financial Dashboard
A Streamlit dashboard for tracking financial and community metrics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration - must be first Streamlit command
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
</style>
""", unsafe_allow_html=True)


def safe_float(val, default=0):
    """Safely convert value to float."""
    try:
        if pd.isna(val):
            return default
        return float(val)
    except (ValueError, TypeError):
        return default


def format_currency(val):
    """Format value as currency."""
    val = safe_float(val)
    if val == 0:
        return "$0"
    return f"${val:,.0f}"


def format_pct(val):
    """Format value as percentage."""
    val = safe_float(val)
    if val == 0:
        return "0%"
    if val < 1:
        return f"{val:.0%}"
    return f"{val:.0f}%"


# Sample data for demo mode
def get_demo_data():
    """Return sample data for demonstration."""
    return {
        'revenue': pd.DataFrame({
            'Category': ['Community Contributions', 'Fundraising Events', 'Learning Events', 'Annual Gathering', 'Merchandise', 'TOTAL'],
            'Budget': [375000, 100000, 10000, 20000, 2000, 507000],
            'YTD': [125000, 35000, 3500, 7000, 800, 171300],
            'Pct': [0.33, 0.35, 0.35, 0.35, 0.40, 0.34]
        }),
        'expenses': pd.DataFrame({
            'Category': ['Development', 'Programs', 'Overhead', 'Grantmaking', 'TOTAL'],
            'Budget': [185533, 173270, 70045, 50000, 478848],
            'YTD': [62000, 58000, 23000, 15000, 158000],
            'Pct': [0.33, 0.33, 0.33, 0.30, 0.33]
        }),
        'community': {
            'size': 272,
            'donors': 162,
            'avg_donation': 1364,
            'giving_pct': 60
        },
        'goals': pd.DataFrame({
            'Goal': ['Grants Given', 'Individuals Engaged', 'Active Allies', 'Impact Partners'],
            'Target': [1000000, 20000, 1000, 50],
            'Current': [310000, 1800, 224, 21],
            'Pct': [31, 9, 22, 42]
        })
    }


def load_excel_data(uploaded_file):
    """Load data from uploaded Excel file."""
    try:
        xl = pd.ExcelFile(uploaded_file)
        data = {}
        
        # Try to load each expected sheet
        sheet_names = xl.sheet_names
        
        # Load Executive Dashboard or similar
        for sheet in ['Executive Dashboard', 'Dashboard', 'Summary']:
            if sheet in sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet)
                data['dashboard'] = df
                break
        
        # Load Progress Tracker or similar for monthly data
        for sheet in ['Progress Tracker', 'Monthly Data', 'Actuals']:
            if sheet in sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet)
                data['progress'] = df
                break
        
        # Load Current Year Budget
        for sheet in ['FY26 Current Year Budget', 'Current Year Budget', 'Budget']:
            if sheet in sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet)
                data['budget'] = df
                break
        
        return data if data else None
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None


# Sidebar
st.sidebar.title("🌱 Flourish Collective")
st.sidebar.markdown("---")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Excel File (optional)",
    type=['xlsx', 'xls'],
    help="Upload your Flourish Financial Tracker file"
)

# Demo mode toggle
use_demo = st.sidebar.checkbox("Use Demo Data", value=True if not uploaded_file else False)

# Load data
if uploaded_file and not use_demo:
    data = load_excel_data(uploaded_file)
    if not data:
        st.warning("Could not load data from file. Using demo data instead.")
        data = get_demo_data()
        use_demo = True
else:
    data = get_demo_data()
    use_demo = True

if use_demo:
    st.sidebar.info("📊 Showing demo data. Upload your Excel file to see your actual data.")

# Navigation
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Executive Summary", "💰 Revenue", "📉 Expenses", "👥 Community", "🎯 2030 Goals"]
)

st.sidebar.markdown("---")
st.sidebar.caption("The Flourish Collective © 2026")

# ============================================================
# PAGE: Executive Summary
# ============================================================
if page == "📊 Executive Summary":
    st.title("📊 Executive Dashboard")
    st.markdown("### FY26 Year-to-Date Performance")
    
    # Get data
    rev = data['revenue']
    exp = data['expenses']
    
    total_rev = rev[rev['Category'] == 'TOTAL']
    total_exp = exp[exp['Category'] == 'TOTAL']
    
    rev_ytd = safe_float(total_rev['YTD'].values[0]) if len(total_rev) > 0 else 0
    rev_budget = safe_float(total_rev['Budget'].values[0]) if len(total_rev) > 0 else 507000
    exp_ytd = safe_float(total_exp['YTD'].values[0]) if len(total_exp) > 0 else 0
    exp_budget = safe_float(total_exp['Budget'].values[0]) if len(total_exp) > 0 else 478848
    
    net_income = rev_ytd - exp_ytd
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Revenue YTD",
            format_currency(rev_ytd),
            f"{rev_ytd/rev_budget*100:.0f}% of budget" if rev_budget > 0 else None
        )
    
    with col2:
        st.metric(
            "Expenses YTD",
            format_currency(exp_ytd),
            f"{exp_ytd/exp_budget*100:.0f}% of budget" if exp_budget > 0 else None
        )
    
    with col3:
        st.metric(
            "Net Income",
            format_currency(net_income),
            "On track" if net_income >= 0 else "Below target",
            delta_color="normal" if net_income >= 0 else "inverse"
        )
    
    with col4:
        comm = data.get('community', {})
        comm_size = comm.get('size', 272) if isinstance(comm, dict) else 272
        st.metric("Active Community", f"{comm_size:,}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue vs Budget")
        rev_detail = rev[rev['Category'] != 'TOTAL'].copy()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='YTD Actual',
            x=rev_detail['Category'],
            y=rev_detail['YTD'],
            marker_color='#2E7D32'
        ))
        fig.add_trace(go.Bar(
            name='Budget',
            x=rev_detail['Category'],
            y=rev_detail['Budget'],
            marker_color='#90EE90'
        ))
        fig.update_layout(barmode='group', height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Expenses vs Budget")
        exp_detail = exp[exp['Category'] != 'TOTAL'].copy()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='YTD Actual',
            x=exp_detail['Category'],
            y=exp_detail['YTD'],
            marker_color='#1565C0'
        ))
        fig.add_trace(go.Bar(
            name='Budget',
            x=exp_detail['Category'],
            y=exp_detail['Budget'],
            marker_color='#90CAF9'
        ))
        fig.update_layout(barmode='group', height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # 2030 Goals Progress
    st.markdown("---")
    st.subheader("🎯 Progress Toward 2030 Goals")
    
    goals = data['goals']
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(goals.iterrows()):
        with cols[i % 4]:
            pct = safe_float(row['Pct'])
            if pct < 1:
                pct = pct * 100
            st.markdown(f"**{row['Goal']}**")
            st.progress(min(pct/100, 1.0))
            st.caption(f"{pct:.0f}% complete")

# ============================================================
# PAGE: Revenue
# ============================================================
elif page == "💰 Revenue":
    st.title("💰 Revenue Analysis")
    
    rev = data['revenue']
    total_row = rev[rev['Category'] == 'TOTAL']
    
    ytd = safe_float(total_row['YTD'].values[0]) if len(total_row) > 0 else 0
    budget = safe_float(total_row['Budget'].values[0]) if len(total_row) > 0 else 507000
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("YTD Revenue", format_currency(ytd))
    with col2:
        st.metric("Annual Budget", format_currency(budget))
    with col3:
        pct = (ytd / budget * 100) if budget > 0 else 0
        st.metric("% of Budget", f"{pct:.1f}%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    rev_detail = rev[rev['Category'] != 'TOTAL'].copy()
    
    with col1:
        st.subheader("Budget Allocation")
        fig = px.pie(
            rev_detail,
            values='Budget',
            names='Category',
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("YTD by Category")
        fig = px.bar(
            rev_detail,
            x='Category',
            y='YTD',
            color='YTD',
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detail table
    st.subheader("Revenue Detail")
    display_df = rev.copy()
    display_df['YTD_fmt'] = display_df['YTD'].apply(format_currency)
    display_df['Budget_fmt'] = display_df['Budget'].apply(format_currency)
    display_df['Pct_fmt'] = display_df['Pct'].apply(format_pct)
    st.dataframe(
        display_df[['Category', 'YTD_fmt', 'Budget_fmt', 'Pct_fmt']].rename(
            columns={'YTD_fmt': 'YTD', 'Budget_fmt': 'Budget', 'Pct_fmt': '% of Budget'}
        ),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# PAGE: Expenses
# ============================================================
elif page == "📉 Expenses":
    st.title("📉 Expense Analysis")
    
    exp = data['expenses']
    total_row = exp[exp['Category'] == 'TOTAL']
    
    ytd = safe_float(total_row['YTD'].values[0]) if len(total_row) > 0 else 0
    budget = safe_float(total_row['Budget'].values[0]) if len(total_row) > 0 else 478848
    remaining = budget - ytd
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("YTD Expenses", format_currency(ytd))
    with col2:
        st.metric("Annual Budget", format_currency(budget))
    with col3:
        st.metric(
            "Remaining",
            format_currency(remaining),
            "Under budget" if remaining > 0 else "Over budget",
            delta_color="normal" if remaining > 0 else "inverse"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    exp_detail = exp[exp['Category'] != 'TOTAL'].copy()
    
    with col1:
        st.subheader("Budget by Category")
        fig = px.pie(
            exp_detail,
            values='Budget',
            names='Category',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Budget vs Actual")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=exp_detail['Category'],
            x=exp_detail['YTD'],
            name='YTD Actual',
            orientation='h',
            marker_color='#1565C0'
        ))
        fig.add_trace(go.Bar(
            y=exp_detail['Category'],
            x=exp_detail['Budget'],
            name='Budget',
            orientation='h',
            marker_color='#90CAF9'
        ))
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detail table
    st.subheader("Expense Detail")
    display_df = exp.copy()
    display_df['YTD_fmt'] = display_df['YTD'].apply(format_currency)
    display_df['Budget_fmt'] = display_df['Budget'].apply(format_currency)
    display_df['Pct_fmt'] = display_df['Pct'].apply(format_pct)
    st.dataframe(
        display_df[['Category', 'YTD_fmt', 'Budget_fmt', 'Pct_fmt']].rename(
            columns={'YTD_fmt': 'YTD', 'Budget_fmt': 'Budget', 'Pct_fmt': '% of Budget'}
        ),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# PAGE: Community
# ============================================================
elif page == "👥 Community":
    st.title("👥 Community Growth")
    
    comm = data.get('community', {})
    if isinstance(comm, dict):
        size = comm.get('size', 272)
        donors = comm.get('donors', 162)
        avg_donation = comm.get('avg_donation', 1364)
        giving_pct = comm.get('giving_pct', 60)
    else:
        size, donors, avg_donation, giving_pct = 272, 162, 1364, 60
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Community", f"{size:,}", "Target: 330")
    with col2:
        st.metric("Number of Donors", f"{donors:,}", "Target: 162")
    with col3:
        st.metric("Average Donation", f"${avg_donation:,}", "Target: $1,279")
    with col4:
        st.metric("% Community Giving", f"{giving_pct}%", "Target: 60%")
    
    st.markdown("---")
    
    # Key insight
    st.info("📊 **Key Insight:** 60% of people who attend 4 events become donors. 100% who attend 6+ events become regular givers.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engagement Funnel")
        funnel_data = {
            'Stage': ['Event Attendees', 'Repeat (4+)', 'Donors', 'Regular Givers'],
            'Count': [190, 80, donors, int(donors * 0.6)]
        }
        fig = go.Figure(go.Funnel(
            y=funnel_data['Stage'],
            x=funnel_data['Count'],
            marker=dict(color=['#81C784', '#66BB6A', '#4CAF50', '#2E7D32'])
        ))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Community Composition")
        fig = px.pie(
            values=[donors, size - donors],
            names=['Donors', 'Non-Donors'],
            color_discrete_sequence=['#2E7D32', '#E8F5E9']
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

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
    
    goals = data['goals']
    
    for _, row in goals.iterrows():
        col1, col2 = st.columns([2, 3])
        
        target = safe_float(row['Target'])
        current = safe_float(row['Current'])
        pct = safe_float(row['Pct'])
        if pct < 1:
            pct = pct * 100
        
        with col1:
            st.markdown(f"### {row['Goal']}")
            if target >= 100000:
                st.metric("Current", f"${current:,.0f}")
                st.metric("Target", f"${target:,.0f}")
            else:
                st.metric("Current", f"{current:,.0f}")
                st.metric("Target", f"{target:,.0f}")
        
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
    
    years = ['FY25', 'FY26', 'FY27', 'FY28', 'FY29', 'FY30']
    projections = [310000, 360000, 520000, 700000, 900000, 1000000]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=projections,
        mode='lines+markers',
        name='Projected Grants',
        line=dict(color='#7B1FA2', width=3),
        marker=dict(size=12)
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
st.markdown("*🌱 The Flourish Collective — Building Allies & Investing in Leaders for Racial Justice*")
