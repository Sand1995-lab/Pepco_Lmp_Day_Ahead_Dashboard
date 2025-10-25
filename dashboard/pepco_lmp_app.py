# Dark-mode Pepco LMP Dash App
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

BG = "#0d1117"
PLOT = "#0d1117"
FG = "#c9d1d9"
GRID = "#30363d"
ACCENTS = ['#58a6ff', '#ff7b72', '#d2a8ff', '#7ee787', '#79c0ff', '#ffa657']

def apply_dark(fig, title):
    fig.update_layout(
        title=title,
        paper_bgcolor=BG, plot_bgcolor=PLOT, font=dict(color=FG),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont=dict(color=FG)),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont=dict(color=FG)),
        legend=dict(bgcolor="rgba(13,17,23,0.6)", bordercolor=GRID, borderwidth=1)
    )
    return fig

monthly = pd.read_csv("../data/pepco_lmp_summary.csv")
daily = pd.read_csv("../data/pepco_lmp_daily.csv")
hourly = pd.read_csv("../data/pepco_lmp_hourly_profile.csv")
daily["date"] = pd.to_datetime(daily["date"], errors="coerce")

# Detect node column
node_col = None
for c in ["Node","node","location","pnode","name","zone","bus","trading_node","load_zone","constraint_node"]:
    if c in monthly.columns:
        node_col = c; break
if node_col is None:
    node_col = monthly.columns[0]

nodes = sorted(daily[node_col].astype(str).unique())

app = Dash(__name__)
app.title = "Pepco LMP — Dark"

def kpi_card(label, value, color=FG):
    return html.Div(style={"background":"#161b22","padding":"10px","borderRadius":"12px","border":"1px solid #30363d"}, children=[
        html.Div(label, style={"fontSize":"12px","color":"#8b949e"}),
        html.Div(value, style={"fontSize":"22px","fontWeight":"700","color":color}),
    ])

overall_avg = daily["avg"].mean()
overall_median = daily["median"].median() if "median" in daily.columns else daily["avg"].median()
overall_min = daily["low"].min() if "low" in daily.columns else daily["avg"].min()
overall_max = daily["high"].max() if "high" in daily.columns else daily["avg"].max()
n_obs = int(daily["obs"].sum()) if "obs" in daily.columns else int(len(daily))

app.layout = html.Div(style={"fontFamily":"Inter, system-ui, Arial, sans-serif","margin":"18px","background":BG,"color":FG}, children=[
    html.H1("Pepco Day-Ahead LMP Dashboard", style={"marginBottom":"6px"}),
    html.Div("Dark mode — GitHub style.", style={"color":"#8b949e","marginBottom":"8px"}),
    html.Div(style={"display":"flex","gap":"10px","flexWrap":"wrap","marginBottom":"12px"}, children=[
        kpi_card("Observations", f"{n_obs:,}"),
        kpi_card("Average LMP", f"{overall_avg:.2f}", "#58a6ff"),
        kpi_card("Median LMP", f"{overall_median:.2f}", "#7ee787"),
        kpi_card("Min LMP", f"{overall_min:.2f}", "#ff7b72"),
        kpi_card("Max LMP", f"{overall_max:.2f}", "#d2a8ff"),
    ]),
    html.Div(style={"display":"flex","gap":"10px","alignItems":"center","margin":"10px 0"}, children=[
        html.Div("Node:", style={"fontWeight":"600"}),
        dcc.Dropdown(options=[{"label": n, "value": n} for n in nodes], value=nodes[0], id="node", style={"minWidth":"260px","color":"#111"}),
        dcc.DatePickerRange(id="date_range", display_format="YYYY-MM-DD",
                            start_date=str(daily["date"].min().date()), end_date=str(daily["date"].max().date()))
    ]),
    dcc.Graph(id="daily_ts"),
    dcc.Graph(id="monthly_bar"),
    dcc.Graph(id="heatmap"),
    html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"12px"}, children=[
        dcc.Graph(id="hourly_profile"),
        dcc.Graph(id="box_month"),
    ]),
    dcc.Graph(id="hist"),
])

@app.callback(
    Output("daily_ts","figure"),
    Output("monthly_bar","figure"),
    Output("heatmap","figure"),
    Output("hourly_profile","figure"),
    Output("box_month","figure"),
    Output("hist","figure"),
    Input("node","value"),
    Input("date_range","start_date"),
    Input("date_range","end_date"),
)
def update(node, start_date, end_date):
    import pandas as pd
    dff = daily[daily[node_col].astype(str) == str(node)].copy()
    if start_date:
        dff = dff[dff["date"] >= pd.to_datetime(start_date)]
    if end_date:
        dff = dff[dff["date"] <= pd.to_datetime(end_date)]

    # Daily TS
    s = dff.sort_values("date")
    fig_ts = go.Figure([go.Scatter(x=s["date"], y=s["avg"], mode="lines", line=dict(color=ACCENTS[0], width=2))])
    apply_dark(fig_ts, f"Daily Avg LMP — {node}")

    # Monthly bar
    m = monthly[monthly[node_col].astype(str)==str(node)].sort_values("year_month")
    fig_m = go.Figure([go.Bar(x=m["year_month"], y=m["avg"], marker=dict(color=ACCENTS[1]))])
    apply_dark(fig_m, f"Monthly Average — {node}")

    # Heatmap
    mh = monthly[monthly[node_col].astype(str)==str(node)].copy()
    pivot = mh.pivot_table(index="year", columns="month", values="avg", aggfunc="mean").reindex(columns=range(1,13))
    fig_h = go.Figure(data=go.Heatmap(z=pivot.values, x=[pd.to_datetime(f"2000-{c:02d}-01").strftime("%b") for c in pivot.columns],
                                      y=pivot.index.astype(str), coloraxis="coloraxis"))
    fig_h.update_layout(coloraxis=dict(colorscale="Turbo", colorbar=dict(title="Avg LMP", tickcolor=FG, titlefont=dict(color=FG), tickfont=dict(color=FG))))
    apply_dark(fig_h, f"Monthly Heatmap — {node}")

    # Hourly profile
    hp = hourly[hourly[node_col].astype(str)==str(node)].sort_values("hour")
    fig_hp = go.Figure([go.Scatter(x=hp["hour"], y=hp["avg"], mode="lines+markers", line=dict(color=ACCENTS[2]))])
    apply_dark(fig_hp, f"Hour-of-Day Profile — {node}")

    # Box by month (from daily)
    dff["month"] = dff["date"].dt.month
    dff["month_abbr"] = dff["month"].apply(lambda m: pd.to_datetime(f"2000-{int(m):02d}-01").strftime("%b"))
    fig_box = go.Figure([go.Box(x=dff["month_abbr"], y=dff["avg"], boxmean=True, marker_color=ACCENTS[3])])
    apply_dark(fig_box, f"Monthly Boxplot — {node}")

    # Histogram
    fig_hist = go.Figure([go.Histogram(x=dff["avg"], nbinsx=60, marker=dict(color=ACCENTS[4]))])
    apply_dark(fig_hist, f"Distribution — {node}")

    return fig_ts, fig_m, fig_h, fig_hp, fig_box, fig_hist

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)
