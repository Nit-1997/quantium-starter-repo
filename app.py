import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

df = pd.read_csv("formatted_sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

daily_sales = df.groupby("date")["sales"].sum().reset_index()

app = dash.Dash(__name__)

fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales ($)"},
)

fig.add_vline(
    x=pd.Timestamp("2021-01-15"),
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase (Jan 15, 2021)",
    annotation_position="top left",
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    hovermode="x unified",
)

app.layout = html.Div(
    id="main-container",
    children=[
        html.H1(
            id="header-title",
            children="Pink Morsel Sales Visualizer",
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        dcc.Graph(id="sales-line-chart", figure=fig),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
