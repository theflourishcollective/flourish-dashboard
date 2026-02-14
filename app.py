"""
Flourish Collective Financial Dashboard
"""

import streamlit as st

# Page config must be first
st.set_page_config(
    page_title="Flourish Collective Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Import other libraries after page config
try:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError as e:
    st.error(f"Error importing libraries: {e}")
    st.stop()

# Simple helper functions
def safe_float(val, default=0):
    try:
        if pd.isna(val):
            return default
        return float(val)
    except:
        return default

def format_currency(val):
    val = safe_float(val)
    return f"${val:,.0f}" if val else "$0"

# Demo data
REVENUE_DATA = {
    'Category': ['Community Contributions', 'Fundraising Events', 'Learning Events', 'Annual Gathering', 'Merchandise'],
    'Budget': [375000, 100000, 10000, 20000, 2000],
    'YTD': [125000, 35000, 3500, 7000, 800]
}

EXPENSE_DATA = {
    'Category': ['Development', 'Programs', 'Overhead', 'Grantmaking'],
    'Budget': [185533, 173270, 70045, 50000],
    'YTD': [62000, 58000, 23000, 15000]
}

GOALS_DATA = {
    'Goal': ['Grants Given', 'Individuals Engaged', 'Active Allies', 'Impact Partners'],
    'Target': [1000000, 20000, 1000, 50],
    'Current': [310000, 1800, 224, 21],
    'Pct': [31, 9, 22, 42]
}

# Sidebar
st.sidebar.title("🌱 Flourish Collective")
st.sidebar.markdown("---")
st.sidebar.info("📊 Showing demo data")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Summary", "💰 Revenue", "📉 Expenses", "🎯 Goals"]
)

# Main content
if page == "📊 Summary":
    st.title("📊 Executive Dashboard")
    st.markdown("### FY26 Year-to-Date Performance")
    
    rev_total = sum(REVENUE_DATA['YTD'])
    rev_budget = sum(REVENUE_DATA['Budget'])
    exp_total = sum(EXPENSE_DATA['YTD'])
    exp_budget = sum(EXPENSE_DATA['Budget'])
    net = rev_total - exp_total
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Revenue YTD", format_currency(rev_total), f"{rev_total/rev_budget*100:.0f}% of budget")
    with col2:
        st.metric("Expenses YTD", format_currency(exp_total), f"{exp_total/exp_budget*100:.0f}% of budget")
    with col3:
        st.metric("Net Income", format_currency(net), "On track" if net >= 0 else "Below target")
    with col4:
        st.metric("Active Community", "272")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Category")
        df = pd.DataFrame(REVENUE_DATA)
        fig = px.bar(df, x='Category', y=['YTD', 'Budget'], barmode='group',
                     color_discrete_sequence=['#2E7D32', '#90EE90'])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Expenses by Category")
        df = pd.DataFrame(EXPENSE_DATA)
        fig = px.bar(df, x='Category', y=['YTD', 'Budget'], barmode='group',
                     color_discrete_sequence=['#1565C0', '#90CAF9'])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

elif page == "💰 Revenue":
    st.title("💰 Revenue Analysis")
    
    df = pd.DataFrame(REVENUE_DATA)
    total_ytd = df['YTD'].sum()
    total_budget = df['Budget'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("YTD Revenue", format_currency(total_ytd))
    with col2:
        st.metric("Annual Budget", format_currency(total_budget))
    with col3:
        st.metric("% of Budget", f"{total_ytd/total_budget*100:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, values='Budget', names='Category', title='Budget Allocation',
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(df, x='Category', y='YTD', title='YTD by Category',
                     color='YTD', color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Detail")
    df['% of Budget'] = (df['YTD'] / df['Budget'] * 100).round(1).astype(str) + '%'
    st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "📉 Expenses":
    st.title("📉 Expense Analysis")
    
    df = pd.DataFrame(EXPENSE_DATA)
    total_ytd = df['YTD'].sum()
    total_budget = df['Budget'].sum()
    remaining = total_budget - total_ytd
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("YTD Expenses", format_currency(total_ytd))
    with col2:
        st.metric("Annual Budget", format_currency(total_budget))
    with col3:
        st.metric("Remaining", format_currency(remaining))
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, values='Budget', names='Category', title='Budget by Category',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df['Category'], x=df['YTD'], name='YTD', orientation='h', marker_color='#1565C0'))
        fig.add_trace(go.Bar(y=df['Category'], x=df['Budget'], name='Budget', orientation='h', marker_color='#90CAF9'))
        fig.update_layout(barmode='group', title='Budget vs Actual', height=350)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Goals":
    st.title("🎯 2030 Strategic Goals")
    
    st.markdown("""
    ### Vision for 2030
    Building a powerful community while giving **$1 Million** in unrestricted grants 
    to justice organizations led by people of color.
    """)
    
    st.markdown("---")
    
    df = pd.DataFrame(GOALS_DATA)
    
    for _, row in df.iterrows():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"### {row['Goal']}")
            if row['Target'] >= 100000:
                st.metric("Current", f"${row['Current']:,}")
                st.metric("Target", f"${row['Target']:,}")
            else:
                st.metric("Current", f"{row['Current']:,}")
                st.metric("Target", f"{row['Target']:,}")
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=row['Pct'],
                domain={'x': [0, 1], 'y': [0, 1]},
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
            fig.update_layout(height=200, margin=dict(t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")

# Footer
st.markdown("---")
st.caption("🌱 The Flourish Collective — Building Allies & Investing in Leaders for Racial Justice")
