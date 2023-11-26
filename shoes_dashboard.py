import os
import pandas as pd
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import warnings
import webbrowser
import threading

warnings.simplefilter(action='ignore', category=FutureWarning)


class Shoes_dashboard():
    def __init__(self, filepath):
        self.filepath = filepath

        dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
        load_figure_template("SLATE")
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

        my_skeachers = pd.read_csv(f"{filepath}skechers_shoes_MY.csv")
        sg_skeachers = pd.read_csv(f"{filepath}skechers_shoes_SG.csv")
        unique_description = set(
            my_skeachers["Description"].unique().tolist() + sg_skeachers["Description"].unique().tolist())
        unique_description = list(unique_description)
        unique_description.sort()
        my_skeachers["Date"] = pd.to_datetime(my_skeachers["Date"], dayfirst=True)
        sg_skeachers["Date"] = pd.to_datetime(sg_skeachers["Date"], dayfirst=True)
        max_date_my = my_skeachers["Date"].max()
        max_date_sg = my_skeachers["Date"].max()
        sg_skeachers["Price (SGD $)"] = sg_skeachers["Price (SGD $)"].apply(lambda x: x.replace("$", "")).astype(
            "float")

        my_skeachers_latest = my_skeachers.loc[my_skeachers["Date"] == max_date_my].copy()
        sg_skeachers_latest = sg_skeachers.loc[sg_skeachers["Date"] == max_date_sg].copy()

        # all_skechers_latest = my_skeachers_latest.merge(sg_skeachers_latest, how="outer", suffixes=("_my", "_sg"))
        #
        # my_skeachers_latest.drop(["Date", "Link"], axis=1, inplace=True)
        # sg_skeachers_latest.drop(["Date", "Link"], axis=1, inplace=True)
        #
        # compare_df = sg_skeachers_latest.merge(my_skeachers_latest, how="inner", on="Description")
        # compare_df["Difference(RM)"] = compare_df["Price (RM)"] - compare_df["Price (SGD $)"] * 3.45

        # item_num = {"Country": ["Malaysia", "Singapore"],
        #             "Number of items": [len(my_skeachers_latest), len(sg_skeachers_latest)]}
        # item_count_df = pd.DataFrame(item_num)
        self.app.layout = html.Div([
            dcc.Tabs([
                dcc.Tab(
                    label="Comparison Between Malaysia and Singapore",
                    children=[
                        html.H1("Comparison Between Malaysia and Singapore's Skechers", style={"text-align": "center"}),
                        html.P("Please Select Date Range"),
                        dcc.DatePickerRange(
                            id="date_picker",
                            start_date=my_skeachers["Date"].min(),
                            end_date=my_skeachers["Date"].max(),
                            min_date_allowed=my_skeachers["Date"].min(),
                            max_date_allowed=my_skeachers["Date"].max(),
                            display_format="YYYY-MMM-DD",
                            className="dbc"
                        ),
                        dcc.Graph(id="my_line_comp"),
                        dcc.Graph(id="sg_line_comp"),
                        html.H3("Please Select a Shoes"),
                        dcc.Dropdown(
                            id="metric_dropdown",
                            options=["Top 10 items(Malaysia cheaper)", "Top 10 items(Singapore cheaper)"],
                            value="Top 10 items(Malaysia cheaper)",
                            className="dbc"
                        ),

                        dash_table.DataTable(
                            id="data_table",
                            selected_rows=[],
                            row_selectable='single',
                            style_header={
                                "backgroundColor": "rgb(30,30,30)",
                                "color": "lightgrey",
                                "font-familly": "Arial"
                            },
                            style_data={
                                "backgroundColor": "rgb(50,50,50)",
                                "color": "lightgrey",
                                "font-familly": "Arial"
                            }),

                        dcc.Graph(id="bar_graph")

                    ]
                ),
                dcc.Tab(
                    label="Shoes Price",
                    children=[
                        html.H1(id="title", style={"text-align": "center"}),
                        dcc.Dropdown(
                            id="shoes_filter",
                            options=unique_description,
                            value=unique_description[0],
                            className="dbc"
                        ),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([html.Img(id="img_path", style={"width": f"{100*5/12}%", "height": f"{100*5/12}%"})]),
                                dbc.Card([dash_table.DataTable(
                                    id="compare_table",
                                    style_header={
                                        "backgroundColor": "rgb(30,30,30)",
                                        "color": "lightgrey",
                                        "font-familly": "Arial"
                                    },
                                    style_data={
                                        "backgroundColor": "rgb(50,50,50)",
                                        "color": "lightgrey",
                                        "font-familly": "Arial"
                                    },
                                )]),
                                dbc.Card([html.Div([
                                    html.H3("Link (Singapore)"),
                                    html.P(id="sg_link"),
                                    html.H3("Link (Malaysia)"),
                                    html.P(id="my_link")
                                ])])
                            ], width=5),

                            dbc.Col([
                            dcc.Graph(id="sg_line"),
                            dcc.Graph(id="my_line")
                            ], width=7)
                        ])

                    ]
                )
            ], className="dbc")

        ])

        @self.app.callback(
            Output("data_table", "columns"),
            Output("data_table", "data"),
            Output("data_table", "selected_rows"),
            Output("bar_graph", "figure"),
            Input("metric_dropdown", "value"),
            Input("date_picker", "end_date"),
            Input("date_picker", "start_date"),
        )
        def get_data_table(metric, end_date, start_date):
            global df

            my_skeachers_end_date = my_skeachers.loc[my_skeachers["Date"] == end_date].copy()
            sg_skeachers_end_date = sg_skeachers.loc[sg_skeachers["Date"] == end_date].copy()

            my_skeachers_end_date.drop(["Date", "Link"], axis=1, inplace=True)
            sg_skeachers_end_date.drop(["Date", "Link"], axis=1, inplace=True)

            compare_df = sg_skeachers_end_date.merge(my_skeachers_end_date, how="inner", on="Description")
            compare_df["Difference(RM)"] = compare_df["Price (RM)"] - compare_df["Price (SGD $)"] * 3.47

            item_num = {"Country": ["Malaysia", "Singapore"],
                        "Number of items": [
                            my_skeachers.query("@start_date<=Date <= @end_date")["Description"].nunique(),
                            sg_skeachers.query("@start_date<=Date <= @end_date")["Description"].nunique()
                        ]
                        # [len(my_skeachers_end_date), len(sg_skeachers_end_date)]
                        }
            item_count_df = pd.DataFrame(item_num)

            if metric == "Top 10 items(Malaysia cheaper)":
                df = compare_df.sort_values(by="Difference(RM)")[:10].copy()

                df = df.loc[df["Difference(RM)"] < 0]

                # to temove negative sign
                df["Difference(RM)"] = df["Difference(RM)"].apply(lambda x: round(x * -1, 2))

            else:
                df = compare_df.sort_values(by="Difference(RM)", ascending=False)[:10].copy()
                df = df.loc[df["Difference(RM)"] > 0]
                df = df.round(2)

            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("records")

            bar_graph = px.bar(
                item_count_df,
                x="Country",
                y="Number of items",

            )
            return columns, data, [0], bar_graph

        @self.app.callback(
            Output("my_line_comp", "figure"),
            Output("sg_line_comp", "figure"),
            Input("data_table", "selected_rows"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date"),
        )
        def compare_line_graph(selected_row, start_date, end_date):
            description = df.iloc[selected_row[0]]["Description"]
            my_line = px.line(
                my_skeachers.query("Description == @description and  @start_date <= Date<= @end_date"),
                x="Date",
                y="Price (RM)",
                title=f"{description} Price (RM)"
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font_size": 30

                }
            )

            sg_line = px.line(
                sg_skeachers.query("Description == @description and  @start_date<= Date <= @end_date"),
                x="Date",
                y="Price (SGD $)",
                title=f"{description} Price (SGD $)",
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font_size": 30
                })

            return my_line, sg_line

        @self.app.callback(
            Output("compare_table", "columns"),
            Output("compare_table", "data"),
            Output("img_path", "src"),
            Output("sg_link", "children"),
            Output("my_link", "children"),
            Output("sg_line", "figure"),
            Output("my_line", "figure"),
            Output("title", "children"),
            Input("shoes_filter", "value")
        )
        def shoes_compare(shoes):
            shoes_data_my = my_skeachers_latest.loc[my_skeachers_latest["Description"] == shoes]
            shoes_data_sg = sg_skeachers_latest.loc[sg_skeachers_latest["Description"] == shoes]

            price_my = "-" if len(shoes_data_my) == 0 else shoes_data_my["Price (RM)"].values[0]
            price_sg = "-" if len(shoes_data_sg) == 0 else shoes_data_sg["Price (SGD $)"].values[0]
            max_price_sg = "-" if len(sg_skeachers.loc[sg_skeachers["Description"] == shoes]) == 0 else \
                sg_skeachers[sg_skeachers["Description"] == shoes]["Price (SGD $)"].max()
            min_price_sg = "-" if len(sg_skeachers.loc[sg_skeachers["Description"] == shoes]) == 0 else \
                sg_skeachers[sg_skeachers["Description"] == shoes]["Price (SGD $)"].min()
            max_price_my = "-" if len(my_skeachers.loc[my_skeachers["Description"] == shoes]) == 0 else \
                my_skeachers[my_skeachers["Description"] == shoes]["Price (RM)"].max()
            min_price_my = "-" if len(my_skeachers.loc[my_skeachers["Description"] == shoes]) == 0 else \
                my_skeachers[my_skeachers["Description"] == shoes]["Price (RM)"].min()
            max_price_date_my = "-" if len(my_skeachers.loc[my_skeachers["Description"] == shoes]) == 0 else \
                my_skeachers.query("Description == @shoes and `Price (RM)` == @max_price_my")["Date"].iloc[-1].strftime(
                    '%d-%b-%Y')
            min_price_date_my = "-" if len(my_skeachers.loc[my_skeachers["Description"] == shoes]) == 0 else \
                my_skeachers.query("Description == @shoes and `Price (RM)` == @min_price_my")["Date"].iloc[-1].strftime(
                    '%d-%b-%Y')
            max_price_date_sg = "-" if len(sg_skeachers.loc[sg_skeachers["Description"] == shoes]) == 0 else \
                sg_skeachers.query("Description == @shoes and `Price (SGD $)` == @max_price_sg")["Date"].iloc[
                    -1].strftime(
                    '%d-%b-%Y')
            min_price_date_sg = "-" if len(sg_skeachers.loc[sg_skeachers["Description"] == shoes]) == 0 else \
                sg_skeachers.query("Description == @shoes and `Price (SGD $)` == @min_price_sg")["Date"].iloc[
                    -1].strftime(
                    '%d-%b-%Y')
            table_df = pd.DataFrame(
                {"Metric": ["Current Price", "Maximum Price", "Minimum Price", "Max Price Date", "Min Price Date"],
                 "Malaysia": [price_my, max_price_my, min_price_my, max_price_date_my, min_price_date_my],
                 "Singapore": [price_sg, max_price_sg, min_price_sg, max_price_date_sg, min_price_date_sg]})

            columns = [{"name": i, "id": i} for i in table_df.columns]
            data = table_df.to_dict("records")

            img_file = f"{shoes}.jpg"
            img_path = os.path.join("./assets/shoes images sg", img_file)
            if os.path.exists(img_path):
                src = self.app.get_asset_url(f"shoes images sg/{img_file}")
            else:
                src = self.app.get_asset_url(f"shoes images my/{img_file}")
            sg_link = "-" if len(sg_skeachers.loc[sg_skeachers["Description"] == shoes]) == 0 else \
                sg_skeachers.loc[sg_skeachers["Description"] == shoes, "Link"].iloc[-1]
            my_link = "-" if len(my_skeachers.loc[my_skeachers["Description"] == shoes]) == 0 else \
                my_skeachers.loc[my_skeachers["Description"] == shoes, "Link"].iloc[-1]

            sg_line = px.line(
                sg_skeachers.query("Description == @shoes"),
                x="Date",
                y="Price (SGD $)",
                title="Singapore Skeacher Price"
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font_size": 30

                }
            )

            my_line = px.line(
                my_skeachers.query("Description == @shoes"),
                x="Date",
                y="Price (RM)",
                title="Malaysia Skeacher Price"
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font_size": 30

                }
            )

            title = f"{shoes} Dashboard"

            return columns, data, src, sg_link, my_link, sg_line, my_line, title

        webbrowser.open('http://127.0.0.1:4000/')

    def run(self):
        # Run the Dash app in a separate thread
        thread = threading.Thread(target=self.app.run_server,
                                  kwargs={"port": 4000, "debug": False, "use_reloader": False})
        thread.start()
        # app.run_server(debug=True, port=4000)
