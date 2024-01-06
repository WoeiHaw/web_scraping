import pandas as pd
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import json
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
            dbc.Row([
                dbc.Col([
                    dbc.Card([
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
                    ])
                ]),

            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H4(["Rental's Mean"]),
                        html.P(id="mean-rental")
                    ], style={"height": "100%", "text-align": "center"})
                ]),
                dbc.Col([
                    dbc.Card([
                        html.H4(["Rental's Median"]),
                        html.P(id="median-rental")
                    ], style={"height": "100%", "text-align": "center"})
                ]),

                dbc.Col([
                    dbc.Card([
                        html.H4(["No of Ads"]),
                        html.P(id="ads-rental")
                    ], style={"height": "100%", "text-align": "center"})
                ]),

                dbc.Col([
                    dbc.Card([
                        html.H4(["Max Rental"]),
                        html.P(id="max-rental")
                    ], style={"height": "100%", "text-align": "center"})
                ]),
                dbc.Col([
                    dbc.Card([
                        html.H4(["Min Rental"]),
                        html.P(id="min-rental")
                    ], style={"height": "100%", "text-align": "center"})
                ]),
            ]),
            dbc.Card([dcc.Graph(id="map-chart", className="dbc")]),
            dbc.Row([
                dbc.Col([dbc.Card([dcc.Graph(id="hist-chart")])], width=4),
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
            Output("mean-rental", "children"),
            Output("median-rental", "children"),
            Output("ads-rental", "children"),
            Output("max-rental", "children"),
            Output("min-rental", "children"),
            Output("map-chart", "figure"),
            Output("hist-chart", "figure"),
            Output("burst-chart", "figure"),
            Output("bar-chart", "figure"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
            Input("metrics", "value")
        )
        def get_dashboard_components(start_date, end_date, metrics):
            df = rental_df.query(" @start_date <= Date <= @end_date and `Rental(SGD)`<10000")
            mean_rental = f"${round(df['Rental(SGD)'].mean(), 2)}"
            median_rental = f"${round(df['Rental(SGD)'].median(), 2)}"
            ads_rental = f"{df['Rental(SGD)'].count()}"
            max_rental = f"${df['Rental(SGD)'].max()}"
            min_rental = f"${df['Rental(SGD)'].min()}"
            with open("area_region.json") as f:
                area_sg = json.load(f)

            sg_rental_area = df.groupby("Area", as_index=False).agg(
                {"Rental(SGD)": "median", "Date": "count"})
            sg_rental_area["Area"] = sg_rental_area["Area"].apply(lambda x: x.upper())
            sg_rental_area.rename(columns={"Rental(SGD)": "Rental(median)", "Date": "Num of Ads"}, inplace=True)

            no_adv_area = []
            for area in area_sg:
                if area.upper() not in sg_rental_area["Area"].tolist():
                    no_adv_area.append(area.upper())
            no_adv_area_df = pd.DataFrame(
                {
                    "Area": no_adv_area,
                    "Rental(median)": [0] * len(no_adv_area),
                    "Num of Ads": [0] * len(no_adv_area)
                }
            )
            sg_rental_area = pd.concat([sg_rental_area, no_adv_area_df])
            print(sg_rental_area)
            with open("2-planning-area.json") as f:
                map_data = json.loads(f.read())

            map_chart = px.choropleth(
                sg_rental_area,
                geojson=map_data,
                locations="Area",
                color="Rental(median)",
                featureidkey="properties.name",
                color_continuous_scale=px.colors.sequential.Plasma,
                title="Singapore Room Rental Map",
                hover_data=["Num of Ads"]

            )

            map_chart.update_geos(fitbounds="locations", visible=False)
            map_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                    title={
                                        "x": 0.0,
                                        "y": .95,
                                        "font": {
                                            "size": 30
                                        }
                                    },
                                    )

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
            # mean_price = round(df["Rental(SGD)"].mean(), 2)
            # median_price = round(df["Rental(SGD)"].median(), 2)
            # min_price = round(df["Rental(SGD)"].min(), 2)
            # max_price = round(df["Rental(SGD)"].max(), 2)
            #
            # table_df = pd.DataFrame({"Metrics": ["Mean", "Median", "Minimum", "Maximum"],
            #                          "Value": [mean_price, median_price, min_price, max_price]})
            # stat_table = dash_table.DataTable(
            #     columns=[{"name": i, "id": i} for i in table_df.columns],
            #     data=table_df.to_dict("records"),
            #     sort_action="native",
            #     style_header={
            #         "backgroundColor": "rgb(30,30,30)",
            #         "color": "lightgrey",
            #         "font-familly": "Arial"
            #     },
            #     style_data={
            #         "backgroundColor": "rgb(50,50,50)",
            #         "color": "lightgrey",
            #         "font-familly": "Arial"
            #
            #     }
            # )
            region_df = df.groupby(["Region", "Area"], as_index=False).count()
            region_df.rename(columns={"Date": "Count"}, inplace=True)
            sum_count = region_df["Count"].sum()
            region_df["Percent"] = round((region_df["Count"] / sum_count) * 100, 2)

            burst = px.sunburst(region_df,
                                path=['Region', 'Area'],
                                values='Percent',
                                title='Room Locations Distribution',
                                hover_data=['Count']
                                )

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
            return mean_rental, median_rental, ads_rental, max_rental, min_rental, map_chart, hist, burst, bar

        thread = threading.Thread(target=app.run_server,
                                  kwargs={"port": 4002, "debug": False, "use_reloader": False})
        thread.start()
        webbrowser.open('http://127.0.0.1:4002/')
