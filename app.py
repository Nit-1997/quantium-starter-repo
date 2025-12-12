import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("formatted_sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

app = dash.Dash(__name__)

app.layout = html.Div(
    id="main-container",
    style={
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "backgroundColor": "#f8f9fa",
        "minHeight": "100vh",
        "padding": "20px",
    },
    children=[
        html.Div(
            id="header-container",
            style={
                "backgroundColor": "#e91e63",
                "borderRadius": "12px",
                "padding": "30px",
                "marginBottom": "25px",
                "boxShadow": "0 4px 15px rgba(233, 30, 99, 0.3)",
            },
            children=[
                html.H1(
                    id="header-title",
                    children="Pink Morsel Sales Visualizer",
                    style={
                        "textAlign": "center",
                        "color": "white",
                        "margin": "0",
                        "fontSize": "2.5rem",
                        "fontWeight": "600",
                        "letterSpacing": "1px",
                    },
                ),
                html.P(
                    id="header-subtitle",
                    children="Analyzing sales impact of the January 15, 2021 price increase",
                    style={
                        "textAlign": "center",
                        "color": "rgba(255, 255, 255, 0.85)",
                        "margin": "10px 0 0 0",
                        "fontSize": "1.1rem",
                    },
                ),
            ],
        ),
        html.Div(
            id="controls-container",
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "20px 30px",
                "marginBottom": "25px",
                "boxShadow": "0 2px 10px rgba(0, 0, 0, 0.08)",
            },
            children=[
                html.Label(
                    id="region-filter-label",
                    children="Filter by Region:",
                    style={
                        "fontWeight": "600",
                        "fontSize": "1.1rem",
                        "color": "#333",
                        "marginRight": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All Regions", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"},
                        {"label": "East", "value": "east"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"display": "inline-block"},
                    inputStyle={"marginRight": "6px", "cursor": "pointer"},
                    labelStyle={
                        "marginRight": "25px",
                        "cursor": "pointer",
                        "padding": "8px 16px",
                        "borderRadius": "20px",
                        "backgroundColor": "#f0f0f0",
                        "transition": "all 0.2s ease",
                    },
                ),
            ],
        ),
        html.Div(
            id="chart-container",
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "25px",
                "boxShadow": "0 2px 10px rgba(0, 0, 0, 0.08)",
            },
            children=[
                dcc.Graph(id="sales-line-chart"),
            ],
        ),
        html.Div(
            id="footer-container",
            style={
                "textAlign": "center",
                "marginTop": "25px",
                "color": "#888",
                "fontSize": "0.9rem",
            },
            children=[
                html.P(
                    id="footer-text",
                    children="Soul Foods - Pink Morsel Sales Analysis Dashboard",
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.groupby("date")["sales"].sum().reset_index()
        title_suffix = "All Regions"
    else:
        region_df = df[df["region"] == selected_region]
        filtered_df = region_df.groupby("date")["sales"].sum().reset_index()
        title_suffix = selected_region.capitalize()

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Sales ($)"},
    )

    fig.update_traces(
        line=dict(color="#e91e63", width=2),
        hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Sales:</b> $%{y:,.2f}<extra></extra>",
    )

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="#ff5722",
        line_width=2,
    )

    fig.add_annotation(
        x="2021-01-15",
        y=1.05,
        yref="paper",
        text="Price Increase (Jan 15, 2021)",
        showarrow=False,
        font=dict(color="#ff5722", size=12),
    )

    fig.update_layout(
        title=dict(
            text=f"Pink Morsel Sales Over Time - {title_suffix}",
            font=dict(size=20, color="#333"),
            x=0.5,
            xanchor="center",
        ),
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=True,
            gridcolor="#eee",
            linecolor="#ddd",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#eee",
            linecolor="#ddd",
        ),
        margin=dict(t=60, b=40, l=60, r=40),
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
