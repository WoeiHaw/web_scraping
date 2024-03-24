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

        my_skeachers["Date"] = pd.to_datetime(my_skeachers["Date"], dayfirst=True, format="mixed")
        sg_skeachers["Date"] = pd.to_datetime(sg_skeachers["Date"], dayfirst=True, format="mixed")

        unique_description = set(list(my_skeachers.columns[1:]) + list(sg_skeachers.columns[1:]))
        unique_description = list(unique_description)
        unique_description.sort()

        sg_link_df = pd.read_csv(f"{filepath}SG Skechers Link.csv")
        my_link_df = pd.read_csv(f"{filepath}MY Skechers Link.csv")

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
                                dbc.Card([html.Img(id="img_path",
                                                   style={"width": f"{100 * 5 / 12}%", "height": f"{100 * 5 / 12}%"})]),
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

            my_skeachers_latest = my_skeachers.loc[my_skeachers["Date"] == end_date].dropna(axis="columns")
            sg_skeachers_latest = sg_skeachers.loc[sg_skeachers["Date"] == end_date].dropna(axis="columns")

            # to get the common items between two conuries (intesection)
            description_compare = list(set(sg_skeachers_latest.columns[1:]) & set(my_skeachers_latest.columns[1:]))

            # to build compare_df
            price_sgd = [sg_skeachers_latest[item].values[0] for item in description_compare]
            price_myr = [my_skeachers_latest[item].values[0] for item in description_compare]
            difference_myr = [round(price_myr[i] - price_sgd[i] * 3.55, 2) for i in range(len(price_sgd))]
            compare_df_dict = {"Description": description_compare, "Prcie (SGD $)": price_sgd, "Price (RM)": price_myr,
                               "Difference(RM)": difference_myr}
            compare_df = pd.DataFrame(compare_df_dict)

            item_num = {"Country": ["Malaysia", "Singapore"],
                        "Number of items": [
                            len(my_skeachers.query("@start_date<=Date <= @end_date").dropna(axis="columns",
                                                                                            how="all").columns) - 1,
                            len(sg_skeachers.query("@start_date<=Date <= @end_date").dropna(axis="columns",
                                                                                            how="all").columns) - 1
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
            plot_my_skeachers = my_skeachers.loc[:, ["Date", description]].dropna()
            my_line = px.line(
                plot_my_skeachers.query("@start_date<= Date <= @end_date"),
                x="Date",
                y=description,
                title=f"{description} Price (RM)",
                labels={
                    description: "Prcie (RM)"
                }
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font_size": 30

                }
            )

            plot_sg_skeachers = sg_skeachers.loc[:, ["Date", description]].dropna()
            sg_line = px.line(
                plot_sg_skeachers.query("@start_date<= Date <= @end_date"),
                x="Date",
                y=description,
                title=f"{description} Price (SGD $)",
                labels={
                    description: "Price (SGD)"
                }
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
            # Output("img_path", "src"),
            Output("sg_link", "children"),
            Output("my_link", "children"),
            Output("sg_line", "figure"),
            Output("my_line", "figure"),
            Output("title", "children"),
            Input("shoes_filter", "value")
        )
        def shoes_compare(shoes):
            my_skeachers_latest = my_skeachers.loc[my_skeachers["Date"] == my_skeachers["Date"].max()].dropna(
                axis="columns")
            sg_skeachers_latest = sg_skeachers.loc[sg_skeachers["Date"] == sg_skeachers["Date"].max()].dropna(
                axis="columns")
            current_price_my = "-" if shoes not in my_skeachers_latest else my_skeachers_latest[shoes].values[0]
            current_price_sg = "-" if shoes not in sg_skeachers_latest else sg_skeachers_latest[shoes].values[0]

            max_price_sg = "-" if shoes not in sg_skeachers else sg_skeachers[shoes].max()
            min_price_sg = "-" if shoes not in sg_skeachers else sg_skeachers[shoes].min()

            max_price_my = "-" if shoes not in my_skeachers else my_skeachers[shoes].max()
            min_price_my = "-" if shoes not in my_skeachers else my_skeachers[shoes].min()

            max_price_date_my = "-" if shoes not in my_skeachers else my_skeachers \
                .loc[my_skeachers[shoes] == my_skeachers[shoes].max(), "Date"].iloc[-1].strftime('%d-%b-%Y')

            min_price_date_my = "-" if shoes not in my_skeachers else my_skeachers \
                .loc[my_skeachers[shoes] == my_skeachers[shoes].min(), "Date"].iloc[-1].strftime('%d-%b-%Y')

            max_price_date_sg = "-" if shoes not in sg_skeachers else sg_skeachers \
                .loc[sg_skeachers[shoes] == sg_skeachers[shoes].max(), "Date"].iloc[-1].strftime('%d-%b-%Y')

            min_price_date_sg = "-" if shoes not in sg_skeachers else sg_skeachers \
                .loc[sg_skeachers[shoes] == sg_skeachers[shoes].min(), "Date"].iloc[-1].strftime('%d-%b-%Y')

            table_df = pd.DataFrame(
                {"Metric": ["Current Price", "Maximum Price", "Minimum Price", "Max Price Date", "Min Price Date"],
                 "Malaysia": [current_price_my, max_price_my, min_price_my, max_price_date_my, min_price_date_my],
                 "Singapore": [current_price_sg, max_price_sg, min_price_sg, max_price_date_sg, min_price_date_sg]})

            columns = [{"name": i, "id": i} for i in table_df.columns]
            data = table_df.to_dict("records")

            sg_link = "-" if shoes not in sg_skeachers else \
                sg_link_df.loc[sg_link_df["Description"] == shoes, "link"].values[0]

            my_link = "-" if shoes not in my_skeachers else \
                my_link_df.loc[my_link_df["Description"] == shoes, "link"].values[0]

            plot_sg_shoes = sg_skeachers[["Date", shoes]].dropna() if shoes in sg_skeachers else pd.DataFrame(
                {"Date": [], shoes: []})
            plot_my_shoes = my_skeachers[["Date", shoes]].dropna() if shoes in my_skeachers else pd.DataFrame(
                {"Date": [], shoes: []})
            sg_line = px.line(
                plot_sg_shoes,
                x="Date",
                y=shoes,
                title="Singapore Skeacher Price",
                labels={
                    shoes: "Price (SGD)"
                }
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font_size": 30

                }
            )

            my_line = px.line(
                plot_my_shoes,
                x="Date",
                y=shoes,
                title="Malaysia Skeacher Price",
                labels={
                    shoes: "Price (MYR)"
                }
            ).update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font_size": 30

                }
            )

            title = f"{shoes} Dashboard"
            return columns, data, sg_link, my_link, sg_line, my_line, title

        @self.app.callback(
            Output("img_path", "src"),
            Input("shoes_filter", "value")
        )
        def get_image(shoes):
            img_file = f"{shoes}.jpg"
            img_path_sg = os.path.join("./assets/shoes images sg", img_file)
            img_path_my = os.path.join("./assets/shoes images my", img_file)
            if os.path.exists(img_path_sg):
                src = self.app.get_asset_url(f"shoes images sg/{img_file}")
                return src
            elif os.path.exists(img_path_my):
                src = self.app.get_asset_url(f"shoes images my/{img_file}")
                return src
            else:
                raise PreventUpdate

        webbrowser.open('http://127.0.0.1:4000/')


    def run(self):
        # Run the Dash app in a separate thread
        thread = threading.Thread(target=self.app.run_server,
                                  kwargs={"port": 4000, "debug": False, "use_reloader": False})
        thread.start()
        # app.run_server(debug=True, port=4000)
