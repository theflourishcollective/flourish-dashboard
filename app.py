"""
Flourish Collective Financial Dashboard
FY26 Budget: $507,000 Revenue / $478,847 Expenses
"""

import streamlit as st

st.set_page_config(
    page_title="Flourish Collective Dashboard",
    page_icon="🌱",
    layout="wide"
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def format_currency(val):
    return f"${val:,.0f}" if val else "$0"

# ===========================================
# FY26 BUDGET DATA (from Financial Tracker)
# ===========================================
REVENUE_DATA = {
    'Category': ['Community Contributions', 'Fundraising Events', 'Annual Gathering', 'Learning Events', 'Merchandise'],
    'Budget': [375000, 100000, 20000, 10000, 2000],
    'YTD': [0, 0, 0, 0, 0]  # Update with actuals as year progresses
}

EXPENSE_DATA = {
    'Category': ['Development', 'Programs', 'Overhead', 'Grantmaking'],
    'Budget': [185533, 173269, 70045, 50000],
    'YTD': [0, 0, 0, 0]  # Update with actuals as year progresses
}

GOALS_DATA = {
    'Goal': ['Grants Given', 'Individuals Engaged', 'Active Allies', 'Impact Partners'],
    'Target': [1000000, 20000, 1000, 50],
    'Current': [310000, 1800, 224, 21],
    'Pct': [31, 9, 22, 42]
}

COMMUNITY_DATA = {
    'size': 272,
    'donors': 162,
    'avg_donation': 1364,
    'giving_pct': 60
}

# Sidebar
st.sidebar.title("🌱 Flourish Collective")
st.sidebar.markdown("---")
st.sidebar.markdown("**FY26 Financial Dashboard**")
st.sidebar.caption("Budget data from Financial Tracker. YTD will update as actuals are entered.")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Summary", "💰 Revenue", "📉 Expenses", "👥 Community", "🎯 2030 Goals"]
)

# ===========================================
# SUMMARY PAGE
# ===========================================
if page == "📊 Summary":
    st.title("📊 Executive Dashboard")
    st.markdown("### FY26 Financial Overview")
    
    rev_budget = sum(REVENUE_DATA['Budget'])  # $507,000
    rev_ytd = sum(REVENUE_DATA['YTD'])
    exp_budget = sum(EXPENSE_DATA['Budget'])  # $478,847
    exp_ytd = sum(EXPENSE_DATA['YTD'])
    net_budget = rev_budget - exp_budget  # $28,153
    net_ytd = rev_ytd - exp_ytd
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Revenue Budget", format_currency(rev_budget))
        st.caption(f"YTD: {format_currency(rev_ytd)}")
    with col2:
        st.metric("Expense Budget", format_currency(exp_budget))
        st.caption(f"YTD: {format_currency(exp_ytd)}")
    with col3:
        st.metric("Net Income Budget", format_currency(net_budget))
        st.caption(f"YTD: {format_currency(net_ytd)}")
    with col4:
        st.metric("Active Community", f"{COMMUNITY_DATA['size']:,}")
        st.caption(f"{COMMUNITY_DATA['giving_pct']}% giving rate")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Budget by Category")
        df = pd.DataFrame(REVENUE_DATA)
        fig = px.pie(df, values='Budget', names='Category',
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Expense Budget by Category")
        df = pd.DataFrame(EXPENSE_DATA)
        fig = px.pie(df, values='Budget', names='Category',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # 2030 Goals
    st.markdown("---")
    st.subheader("🎯 Progress Toward 2030 Goals")
    
    goals_df = pd.DataFrame(GOALS_DATA)
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(goals_df.iterrows()):
        with cols[i]:
            st.markdown(f"**{row['Goal']}**")
            st.progress(min(row['Pct']/100, 1.0))
            st.caption(f"{row['Pct']}% complete")

# ===========================================
# REVENUE PAGE
# ===========================================
elif page == "💰 Revenue":
    st.title("💰 Revenue Analysis")
    
    df = pd.DataFrame(REVENUE_DATA)
    total_budget = df['Budget'].sum()
    total_ytd = df['YTD'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Annual Budget", format_currency(total_budget))
    with col2:
        st.metric("YTD Actual", format_currency(total_ytd))
    with col3:
        pct = (total_ytd / total_budget * 100) if total_budget > 0 else 0
        st.metric("% of Budget", f"{pct:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Budget Allocation")
        fig = px.pie(df, values='Budget', names='Category',
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Budget by Category")
        fig = px.bar(df, x='Category', y='Budget', color='Budget',
                     color_continuous_scale='Greens')
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Revenue Detail")
    df['% of Total'] = (df['Budget'] / total_budget * 100).round(1).astype(str) + '%'
    display_df = df.copy()
    display_df['Budget'] = display_df['Budget'].apply(format_currency)
    display_df['YTD'] = display_df['YTD'].apply(format_currency)
    st.dataframe(display_df[['Category', 'Budget', 'YTD', '% of Total']], 
                 use_container_width=True, hide_index=True)

# ===========================================
# EXPENSES PAGE
# ===========================================
elif page == "📉 Expenses":
    st.title("📉 Expense Analysis")
    
    df = pd.DataFrame(EXPENSE_DATA)
    total_budget = df['Budget'].sum()
    total_ytd = df['YTD'].sum()
    remaining = total_budget - total_ytd
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Annual Budget", format_currency(total_budget))
    with col2:
        st.metric("YTD Actual", format_currency(total_ytd))
    with col3:
        st.metric("Remaining", format_currency(remaining))
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Budget by Category")
        fig = px.pie(df, values='Budget', names='Category',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Category Breakdown")
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df['Category'], x=df['Budget'], name='Budget', 
                            orientation='h', marker_color='#1565C0'))
        if total_ytd > 0:
            fig.add_trace(go.Bar(y=df['Category'], x=df['YTD'], name='YTD', 
                                orientation='h', marker_color='#90CAF9'))
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Expense Detail")
    df['% of Total'] = (df['Budget'] / total_budget * 100).round(1).astype(str) + '%'
    display_df = df.copy()
    display_df['Budget'] = display_df['Budget'].apply(format_currency)
    display_df['YTD'] = display_df['YTD'].apply(format_currency)
    st.dataframe(display_df[['Category', 'Budget', 'YTD', '% of Total']], 
                 use_container_width=True, hide_index=True)

# ===========================================
# COMMUNITY PAGE
# ===========================================
elif page == "👥 Community":
    st.title("👥 Community Growth")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Community", f"{COMMUNITY_DATA['size']:,}")
        st.caption("Target: 330")
    with col2:
        st.metric("Number of Donors", f"{COMMUNITY_DATA['donors']:,}")
        st.caption("Target: 162")
    with col3:
        st.metric("Average Donation", f"${COMMUNITY_DATA['avg_donation']:,}")
        st.caption("Target: $1,279")
    with col4:
        st.metric("% Giving", f"{COMMUNITY_DATA['giving_pct']}%")
        st.caption("Target: 60%")
    
    st.markdown("---")
    
    st.info("📊 **Key Insight:** 60% of people who attend 4 events become donors. 100% who attend 6+ events become regular givers.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engagement Funnel")
        funnel_data = {
            'Stage': ['Event Attendees', 'Repeat (4+)', 'Donors', 'Regular Givers'],
            'Count': [190, 80, COMMUNITY_DATA['donors'], int(COMMUNITY_DATA['donors'] * 0.6)]
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
            values=[COMMUNITY_DATA['donors'], COMMUNITY_DATA['size'] - COMMUNITY_DATA['donors']],
            names=['Donors', 'Non-Donors'],
            color_discrete_sequence=['#2E7D32', '#E8F5E9']
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ===========================================
# 2030 GOALS PAGE
# ===========================================
elif page == "🎯 2030 Goals":
    st.title("🎯 2030 Strategic Goals")
    
    st.markdown("""
    ### The Flourish Collective's Vision for 2030
    Building a powerful, sustainable community of allies while giving **$1 Million** 
    in unrestricted grants to justice organizations led by people of color.
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
            fig.update_layout(height=200, margin=dict(t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
    
    # Projection
    st.subheader("📈 Projected Path to $1M in Grants")
    
    years = ['FY25', 'FY26', 'FY27', 'FY28', 'FY29', 'FY30']
    projections = [310000, 360000, 520000, 700000, 900000, 1000000]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=projections,
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
st.caption("🌱 The Flourish Collective — Building Allies & Investing in Leaders for Racial Justice")
