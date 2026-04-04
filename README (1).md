# Flourish Collective Financial Dashboard

A Streamlit dashboard for tracking financial performance, revenue trends, and community growth metrics for [The Flourish Collective](https://www.theflourishcollective.org) — a 501(c)(3) nonprofit building allies and investing in leaders for racial justice.

## Pages

- **📊 Executive Summary** — FY26 KPIs, historical P&L (FY21–FY25), revenue progress vs. budget, community growth trends
- **📋 FY26 Budget vs. Actual** — All revenue and expense accounts with budget, YTD actuals, and % of budget
- **📈 Revenue Detail & Trends** — Historical revenue by source (FY21–FY25) and quarterly comparison (FY24/FY25/FY26)
- **🔍 Functional Expense Report** — Expenses allocated by functional category (Development, Program, Overhead, Grant Making) using JD allocation percentages

## Data Source

All data reads from `Flourish_Financial_Tracker.xlsx` in the repository root. The tracker is updated monthly by the Flourish AI Agent with:
1. Expense actuals from the Income Statement
2. Revenue actuals from the Revenue Transaction Report
3. Engagement metrics from the Program & Engagement Tracker

FY26 data is live. FY21–FY25 is historical. No manual edits to the app are needed when the tracker is updated.

## Deploy to Streamlit Cloud

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click **+** → **New repository**, name it `flourish-dashboard`
3. Make it **Public** (required for free Streamlit Cloud)
4. Click **Create repository**

### Step 2: Upload Files

Upload to repository root:
- `app.py`
- `requirements.txt`
- `Flourish_Financial_Tracker.xlsx`
- `README.md`
- `.streamlit/config.toml` (create `.streamlit` folder first)

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select repository: `theflourishcollective/flourish-dashboard`
5. Branch: `main` · Main file: `app.py`
6. Click **Deploy**

Live in ~2 minutes at your Streamlit URL.

## Monthly Update Workflow

1. AI Agent receives Income Statement, Revenue Transaction Report, and Program Tracker
2. Agent updates `Flourish_Financial_Tracker.xlsx` (Progress Tracker tab only)
3. Download updated tracker and replace file in this repository
4. Commit: `[DATE] - Monthly actuals update [month year]`
5. Dashboard refreshes automatically within ~5 minutes

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Troubleshooting

- Ensure `Flourish_Financial_Tracker.xlsx` is in the repository root
- Repository must be public for free Streamlit Cloud deployment
- Check Streamlit Cloud logs if deployment fails
- Click **🔄 Refresh Data** in the sidebar to force a data reload

## License

© 2026 The Flourish Collective
