import pandas as pd
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
from datetime import timedelta
import threading
import webbrowser


class HousePriceDashBoard:
    def __init__(self, path):
        self.path = path
        jb_house = pd.read_csv(self.path + "House Price JB(Processed).csv")
        kl_house = pd.read_csv(self.path + "House Price kl(Processed).csv")
        kl_house["Date"] = pd.to_datetime(kl_house["Date"],dayfirst=True,format="mixed")
        jb_house["Date"] = pd.to_datetime(jb_house["Date"],dayfirst=True,format="mixed")

        dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
        load_figure_template("SLATE")
        app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

        app.layout = html.Div([
            html.H1(id="main-title", style={"text-align": "center"}),
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.P("Please Select Date Range"),
                        dcc.DatePickerRange(
                            id="date-picker",
                            display_format="YYYY-MM-DD",
                            className="dbc"
                        )
                    ]),
                    dbc.Col([
                        html.P("Please Seelct City"),
                        dcc.RadioItems(
                            id="city_selector",
                            options=["Johor Bahru", "Kuala Lumpur"],
                            value="Johor Bahru",
                            inline=True
                        )

                    ]),

                    dbc.Col([
                        html.P("Please Select the Price Range"),
                        dcc.RangeSlider(
                            id="price_slider",
                            max=2000000,
                            step=400000,
                            value=[0, 2000000],
                            className="dbc",
                            marks={
                                i: f'{int(i / 1000)}K' if i < 1000000 else f"{i / 1000000}M" if i < 2000000 else "2M++"
                                for
                                i in range(0, 2000001, 200000)

                            }
                        )
                    ], width=6)

                ])
            ]),
            dbc.Card([
                dbc.Row([

                    dbc.Col([

                        dcc.Graph(id="burst-distribution")

                    ], width=4),

                    dbc.Col([
                        dcc.RadioItems(
                            id="radio_selector_bar",
                            value="Area",
                            inline=True
                        ),
                        dcc.RadioItems(
                            id="metrics_selector_bar",
                            options=["Highest", "Lowest"],
                            value="Highest",
                            inline=True
                        ),
                        dcc.Graph(id="bar-price")

                    ], width=4),
                    dbc.Col([
                        dcc.Graph(id="pie-type")
                    ], width=4)

                ])

            ]),
            dbc.Card([
                dbc.Row([
                    dbc.Col([dcc.Graph(id="scatter-price")], width=6),
                    dbc.Col([dcc.Graph(id="hist-price")], width=6)
                ])
            ])

        ])

        @app.callback(
            Output("main-title", "children"),
            Output("date-picker", "min_date_allowed"),
            Output("date-picker", "max_date_allowed"),
            Output("date-picker", "start_date"),
            Output("date-picker", "end_date"),
            Output("price_slider", "min"),
            Output("radio_selector_bar", "options"),
            Input("city_selector", "value")
        )
        def select_country(city):

            if city == "Johor Bahru":
                df = jb_house
                selector_bar = "Parliament Seat", "State Seat", "Area"



            elif city == "Kuala Lumpur":
                df = kl_house
                selector_bar = "Parliament Seat", "Area"

            title = f"{city} House Price Dashboard"
            min_date = df["Date"].min()
            max_date = df["Date"].max()
            start_date = df["Date"].max() - timedelta(days=30)
            end_date = df["Date"].max()
            min_price = df["Price"].min()

            return title, min_date, max_date, start_date, end_date, min_price, selector_bar

        @app.callback(
            Output("bar-price", "figure"),
            Output("scatter-price", "figure"),
            Output("burst-distribution", "figure"),
            Output("pie-type", "figure"),
            Output("hist-price", "figure"),
            Input("city_selector", "value"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
            Input("price_slider", "value"),
            Input("radio_selector_bar", "value"),
            Input("metrics_selector_bar", "value")
        )
        def create_graph(city, start_date, end_date, price, bar_selector, metrics_bar):

            if city == "Johor Bahru":
                df = jb_house
                path = ["Parliament", "State", "Area"]

            elif city == "Kuala Lumpur":
                df = kl_house
                path = ["Parliament", "Area"]

            if price[1] == 2000000:
                df = df.query("@start_date <= Date <= @end_date and Price >= @price[0]")
            else:
                df = df.query("@start_date <= Date <= @end_date and @price[0] <= Price <= @price[1]")

            bar_selector = bar_selector.replace("Seat", "").strip()
            if (bar_selector == "State") & (city == "Kuala Lumpur"):
                bar_selector = "Area"
            df_area = df.groupby(bar_selector, as_index=False).agg({"Price/Sq.ft": "median", "Date": "count"})
            df_area.rename(columns={"Date": "count", "Price/Sq.ft": "Price/Sq.ft(median)"}, inplace=True)
            bar = px.bar(
                df_area.sort_values(by="Price/Sq.ft(median)", ascending=False if metrics_bar == "Highest" else True)[
                :10][
                ::-1],
                y=bar_selector,
                x="Price/Sq.ft(median)",
                title=f"Top 10 {metrics_bar} Price (median) by {bar_selector}",
                hover_data="count"
            ).update_layout(title={
                "x": 0.5,
                "y": .87,
                "font": {
                    "size": 20
                }
            }, )
            scatter = px.scatter(
                df,
                x="Size (sq.ft)",
                y="Price",
                color="Number of bedroom",
                size="Number of bathroom",
                title="Scatter Plot of House Price vs Size"

            ).update_layout(title={
                "x": 0.5,
                "y": .87,
                "font": {
                    "size": 20
                }
            }, )

            burst_df = df.groupby(path, as_index=False).agg(
                {
                    "Date": "count",
                    "Price/Sq.ft": "mean"
                }
            )[path + ["Price/Sq.ft", "Date"]]

            burst_df.rename(columns={"Date": "Count", "Price/Sq.ft": "Price/Sq.ft(mean)"}, inplace=True)
            burst_df["Price/Sq.ft(mean)"] = burst_df["Price/Sq.ft(mean)"].round(decimals=2)

            burst = px.sunburst(burst_df,
                                path=path,
                                values='Count',
                                title='House Locations Distribution',
                                hover_data="Price/Sq.ft(mean)"
                                ).update_layout(title={
                "x": 0.5,
                "y": .87,
                "font": {
                    "size": 20
                }
            }, )
            pie = px.pie(
                df.groupby(["Type"], as_index=False).agg({"Price/Sq.ft": "mean", "Date": "count"}) \
                    .rename(columns={"Date": "count", "Price/Sq.ft": "Price/Sq.ft(mean)"}).sort_values(by="count",
                                                                                                       ascending=False)[
                :10],
                values='count',
                names='Type',
                title="House Type Percentage",
                hover_data="Price/Sq.ft(mean)",
                hole=0.5
            ).update_layout(title={
                "x": 0.5,
                "y": .87,
                "font": {
                    "size": 20
                }
            }, )
            pie.update_traces(textposition='inside', textinfo='percent+label')
            pie.update_layout(showlegend=False)

            hist = px.histogram(df,
                                x="Price",
                                title="Histrogram of House Price").update_layout(title={
                "x": 0.5,
                "y": .87,
                "font": {
                    "size": 20
                }
            }, )

            hist.add_vline(
                x=df["Price"].median(), line_width=3, line_dash="dash", annotation_text="Median",
                line_color="green", annotation_position="top left",annotation_font_color="green")
            hist.add_vline(
                x=df["Price"].mean(), line_width=3, line_dash="dash", annotation_text="Mean",
                line_color="red",annotation_position="top right",annotation_font_color="red")


            return bar, scatter, burst, pie, hist

        thread = threading.Thread(target=app.run_server,
                                  kwargs={"port": 4005, "debug": False, "use_reloader": False})
        thread.start()
        webbrowser.open('http://127.0.0.1:4005/')
