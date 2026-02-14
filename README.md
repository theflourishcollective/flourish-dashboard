[README.md](https://github.com/user-attachments/files/25316931/README.md)
# Flourish Collective Financial Dashboard

A Streamlit dashboard for tracking financial metrics, community growth, and progress toward 2030 goals.

## Features

- 📊 Executive Summary with KPIs
- 💰 Revenue Analysis
- 📉 Expense Tracking
- 👥 Community Growth Metrics
- 🎯 2030 Goals Progress

## Deploy to Streamlit Cloud

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in (or create an account)
2. Click the **+** icon → **New repository**
3. Name it `flourish-dashboard`
4. Make it **Public** (required for free Streamlit Cloud)
5. Click **Create repository**

### Step 2: Upload Files

Upload these files to your repository:
- `app.py`
- `requirements.txt`
- `.streamlit/config.toml` (create a folder named `.streamlit` first)

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **New app**
4. Select your repository: `your-username/flourish-dashboard`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **Deploy**

Your app will be live in about 2 minutes!

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Using Your Own Data

1. Upload your Flourish Financial Tracker Excel file using the sidebar
2. The dashboard will display your actual data instead of demo data

## Troubleshooting

If deployment fails:
1. Check that all files are uploaded correctly
2. Ensure the repository is public
3. Verify `requirements.txt` exists in the root directory
4. Check the Streamlit Cloud logs for specific errors

## License

© 2026 The Flourish Collective
