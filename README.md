# Pepco Day-Ahead LMP Dashboard (Dark Mode)

A fully interactive, GitHub Pages–ready dashboard for Pepco **Day-Ahead LMP** data in a **GitHub-style dark theme**.

## 🔗 Live (GitHub Pages)
1. Push this repo to GitHub (e.g. `pepco-lmp-dashboard`).
2. In **Settings → Pages**:  
   - **Branch:** `main`  
   - **Folder:** `/dashboard`  
3. Your dashboard will be available at:
```
https://<your-username>.github.io/pepco-lmp-dashboard/pepco_lmp_dashboard.html
```

## 📁 Project Layout
```
pepco-lmp-dashboard/
├── data/
│   ├── pepco_lmp_summary.csv
│   ├── pepco_lmp_daily.csv
│   ├── pepco_lmp_hourly_profile.csv
├── dashboard/
│   ├── pepco_lmp_dashboard.html
│   └── pepco_lmp_app.py
├── README.md
└── requirements.txt
```

## ▶️ View Locally
Just open `dashboard/pepco_lmp_dashboard.html` in your browser.

## 🖥️ Run the Dash App Locally
```bash
pip install -r requirements.txt
cd dashboard
python pepco_lmp_app.py
```
Then open `http://127.0.0.1:8050/`.

## 🔧 Data
The dashboard reads pre-aggregated CSVs in `data/`:
- `pepco_lmp_summary.csv` — monthly summary per node (avg, median, high, low, std, obs)
- `pepco_lmp_daily.csv` — daily summary per node
- `pepco_lmp_hourly_profile.csv` — hour-of-day averages per node

> Want to rebuild from the raw Excel? Add your ETL script or contact the author to include it in this repo.

## 🎨 Theme
Custom **GitHub Dark** palette:
- Background: `#0d1117`
- Text: `#c9d1d9`
- Gridlines: `#30363d`
- Accents: #58a6ff, #ff7b72, #d2a8ff, #7ee787, #79c0ff, #ffa657

## 🙋 Support / Enhancements
- Volatility metrics, anomaly flags, node comparisons
- CSV/PNG export buttons in charts
- Additional tabs (e.g., yearly KPIs, price spikes)
