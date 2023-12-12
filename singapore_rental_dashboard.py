import pandas as pd
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import webbrowser
import threading
import numpy as np


class Sg_rental_dashboard():
    def __init__(self, path):
        dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
        load_figure_template("SLATE")
        app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

        rental_df = pd.read_csv(path + "sg rental(processed).csv")

        app.layout = html.Div([
            html.H1(["Singapore Rooms Rental Analysis "], style={"text-align": "center"}),
            dbc.Card([
                html.P(["Please Pick Data Range"]),
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=rental_df["Date"].min(),
                    max_date_allowed=rental_df["Date"].max(),
                    start_date=rental_df["Date"].unique()[-30],
                    end_date=rental_df["Date"].max(),
                    display_format="YYYY-MMM-DD",
                    className="dbc"

                )]),
            dbc.Card([dcc.Graph(id="hist-chart", className="dbc")]),
            dbc.Row([
                dbc.Col([dbc.Card(id="data-table")], width=4),
                dbc.Col(dbc.Card([dcc.Graph(id="burst-chart")]), width=4),
                dbc.Col([dbc.Card([
                    dcc.RadioItems(
                        id="metrics",
                        options=["Highest Price", "Lowest Price"],
                        value="Highest Price",
                        inline=True,
                    ),
                    dcc.Graph(id="bar-chart")
                ])], width=4),

            ])
        ])

        @app.callback(
            Output("hist-chart", "figure"),
            Output("data-table", "children"),
            Output("burst-chart", "figure"),
            Output("bar-chart", "figure"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
            Input("metrics", "value")
        )
        def get_dashboard_components(start_date, end_date, metrics):
            df = rental_df.query(" @start_date <= Date <= @end_date")
            hist = px.histogram(
                df,
                x="Rental(SGD)",
                title="Rental Price Distribution"
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 40
                    }
                }, )
            mean_price = round(df["Rental(SGD)"].mean(), 2)
            median_price = round(df["Rental(SGD)"].median(), 2)
            min_price = round(df["Rental(SGD)"].min(), 2)
            max_price = round(df["Rental(SGD)"].max(), 2)

            table_df = pd.DataFrame({"Metrics": ["Mean", "Median", "Minimum", "Maximum"],
                                     "Value": [mean_price, median_price, min_price, max_price]})
            stat_table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in table_df.columns],
                data=table_df.to_dict("records"),
                sort_action="native",
                style_header={
                    "backgroundColor": "rgb(30,30,30)",
                    "color": "lightgrey",
                    "font-familly": "Arial"
                },
                style_data={
                    "backgroundColor": "rgb(50,50,50)",
                    "color": "lightgrey",
                    "font-familly": "Arial"

                }
            )
            region_df = df.groupby(["Region", "Area"], as_index=False).count()
            # pie = px.pie(values=region_df.values, names=region_df.index, title='Number of Advertisements by Region')
            burst = px.sunburst(region_df,
                                path=['Region', 'Area'],
                                values='Date',
                                title='Room Locations Distribution'
                                )

            # burst.update_traces(textposition='inside', textinfo='percent+label')
            burst.update_layout(
                xaxis_title='Number of Jobs',
                yaxis_title='City',
                coloraxis_showscale=False,
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 20
                    }
                },
            )
            if metrics == "Highest Price":
                is_ascending = False
                title_components = "Highest"
            else:
                is_ascending = True
                title_components = "Lowest"
            # area_df = df.groupby("Area")["Rental(SGD)"].median().sort_values(ascending=is_ascending)[0:10]
            area_df = df.groupby("Area").agg({"Rental(SGD)": [np.median, "count"]})
            area_df.columns = area_df.columns.droplevel()
            area_df = area_df.sort_values(by="median", ascending=is_ascending)[0:10]

            bar = px.bar(
                area_df,
                x=area_df.index,
                y="median",
                hover_data=["count"],
                title=f"Top 10 {title_components}(median) Rental by Area"
            )
            bar.update_layout(
                xaxis_title="Area",
                yaxis_title="Price (SGD)",
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 20
                    }
                }, )
            return hist, stat_table, burst, bar

        thread = threading.Thread(target=app.run_server,
                                  kwargs={"port": 4002, "debug": False, "use_reloader": False})
        thread.start()
        webbrowser.open('http://127.0.0.1:4002/')
