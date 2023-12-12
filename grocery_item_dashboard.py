import pandas as pd
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import warnings
import threading
import webbrowser

warnings.filterwarnings("ignore", category=UserWarning)


class Grocery_dashboard():
    def __init__(self, path):
        dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
        load_figure_template("SLATE")
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

        # kluang_kopi = pd.read_csv(path + "kopi o price.csv")
        # kluang_kopi["Date"] = pd.to_datetime(kluang_kopi["Date"], dayfirst=True)

        self.app.layout = html.Div([
            html.H1(id="main_title", style={"font-size": "1.5rem", "text-align": "center"}),
            dbc.Card([dbc.Row([
                dbc.Col([
                    html.P("Please Select an Grocery item"),
                    dcc.Dropdown(
                        id="data-dropdown",
                        options=["Kopi O Kosong", "Dettol Shower Gel", "Darlie Toothpaste", "Head & Shoulder Shampoo",
                                 "Face Wash"],
                        value="Kopi O Kosong",
                        className="dbc"
                    )
                ]),
                dbc.Col([
                    html.P("Please Select Date Range"),
                    dcc.DatePickerRange(
                        id="date_picker",
                        display_format="YYYY-MMM-DD",
                        className="dbc"
                    )
                ])

            ])

            ]),
            dbc.Card([dcc.Graph(id="line_graph", className="dbc")]),
            dbc.Card([dbc.Col([dbc.Card(id="data-table")]), ]),
            dbc.Card([dbc.Col([dbc.Card([dcc.Graph(id="pie-chart")])])])
        ])

        @self.app.callback(
            Output("main_title", "children"),
            Output("date_picker", "min_date_allowed"),
            Output("date_picker", "max_date_allowed"),
            Output("date_picker", "start_date"),
            Output("date_picker", "end_date"),
            Input("data-dropdown", "value"),

        )
        def process_selectdate(data):
            global grocery_data, y_data, table_column

            if data == "Kopi O Kosong":
                grocery_data = pd.read_csv(path + "kopi o price.csv")
                y_data = ["Date", "Shopee Price", "Lazada Price", "PGMall Price"]
                table_column = ["Shopee", "Lazada", "PGMall"]
                grocery_name = "Kluang Coffee Cap Televisyen Kopi O Kosong Eco Pack (100 sachets x 1 Pack) Kopi-O Kluang Cap TV Dashboard"
            elif data == "Dettol Shower Gel":
                grocery_data = pd.read_csv(path + "Dettol Shower Gel.csv")
                y_data = ["Date", "Price/pcs (Watson)", "Price/pcs (Aeon)", "Price/pcs (Guardian)",
                          "Price/pcs (Caring)"]
                table_column = ["Watson", "Aeon", "Guardian", "Caring"]
                grocery_name = "DETTOL Shower Gel Lasting Fresh 950G"
            elif data == "Darlie Toothpaste":
                grocery_data = pd.read_csv(path + "Darlie Toothpaste.csv")
                y_data = ["Date", "Guardian Price", "BigPharmacy Price", "Watson Price"]
                table_column = ["Guardian", "BigPharmacy", "Watson"]
                grocery_name = "Darlie Double Action Toothpaste 2 x 225g"
            elif data == "Head & Shoulder Shampoo":
                grocery_data = pd.read_csv(path + "shampoo price.csv")
                grocery_data["Guardian Price"] = grocery_data["Guardian Price"].apply(
                    lambda x: None if x == " " else x).astype(
                    "float")
                grocery_data["Lotus Price"] = grocery_data["Lotus Price"].apply(lambda x: None if x == 0 else x)
                y_data = ["Date", "Watson Price", "Guardian Price", "Lotus Price"]
                table_column = ["Watson", "Guardian", "Lotus"]
                grocery_name = "Head & Shoulder Shampoo Menthol 480ml"
            elif data == "Face Wash":
                grocery_data = pd.read_csv(path + "Nivea Man.csv")
                grocery_data["Guardian Price"] = grocery_data["Guardian Price"].apply(lambda x: 2 * x if x < 20 else x)
                y_data = ["Date", "Guardian Price", "Aeon Price", "Watson Price"]
                table_column = ["Guardian", "Aeon", "Watson"]
                grocery_name = "NIVEA FOR MEN DEEP White Oil Clear Mud Foam Twin Pack 2x100g"

            dashboard_title = f"{grocery_name} Dashboard"
            grocery_data["Date"] = grocery_data["Date"].apply(lambda x: x.replace("-", "/"))
            grocery_data["Date"] = pd.to_datetime(grocery_data["Date"], dayfirst=True)
            min_date = grocery_data["Date"].min()
            max_date = grocery_data["Date"].max()
            start_date = grocery_data.iloc[-30]["Date"]
            end_date = grocery_data["Date"].max()

            return dashboard_title.title(), min_date, max_date, start_date, end_date

        @self.app.callback(
            Output("line_graph", "figure"),
            Output("data-table", "children"),
            Output("pie-chart", "figure"),
            Input("date_picker", "start_date"),
            Input("date_picker", "end_date"),
        )
        def price_dashbord(start_date, end_date):
            df = grocery_data.query("@start_date<= Date <= @end_date")[y_data]
            y_data_removed = []
            table_column_removed = []
            for column in df:
                if df[column].isnull().sum() == len(df):
                    df.drop(columns=column, inplace=True)
                    y_data.remove(column)
                    y_data_removed.append(column)
                    # to remove 'price'
                    index = column.find('Price')
                    platform_name = column[:index].strip()
                    table_column.remove(platform_name)
                    table_column_removed.append(platform_name)

            y_data.remove("Date")

            new_legend = {y_data[i]: table_column[i] for i in range(len(y_data))}
            line_chart = px.line(
                df,
                x="Date",
                y=y_data,
                labels={
                    "variable": "Platform/ Vendor"
                },
                title=f"Price from {df['Date'].min().strftime('%d-%b-%Y')} to {df['Date'].max().strftime('%d-%b-%Y')}"
            )
            line_chart.update_layout(
                title={
                    "x": 0.5,
                    "y": 0.85,
                    "font": {"size": 25}
                },
                hovermode="x"

            ).update_yaxes(
                title="Price (RM)"
            ).for_each_trace(lambda t: t.update(name=new_legend[t.name],
                                                legendgroup=new_legend[t.name],
                                                hovertemplate=t.hovertemplate.replace(t.name, new_legend[t.name])
                                                )
                             )
            df["for_groupby"] = "text"

            # data table
            mean = df.groupby("for_groupby", as_index=False).mean(numeric_only=True)
            median = df.groupby("for_groupby", as_index=False).median(numeric_only=True)

            mode = df.groupby("for_groupby", as_index=False).agg(lambda x: x.value_counts().index[0])
            mode = mode[y_data]

            min_price = df.groupby("for_groupby", as_index=False).min(numeric_only=True)
            max_price = df.groupby("for_groupby", as_index=False).max(numeric_only=True)
            min_price_date = pd.DataFrame(columns=y_data)
            max_price_date = pd.DataFrame(columns=y_data)

            for column in y_data:
                min_price_df = df[df[column] == df[column].min()]
                min_price_date[column] = [min_price_df["Date"].iloc[-1].strftime('%d-%b-%Y')]

                max_price_df = df[df[column] == df[column].max()]
                max_price_date[column] = [max_price_df["Date"].iloc[-1].strftime('%d-%b-%Y')]

            mean["for_groupby"] = "Mean"
            median["for_groupby"] = "Median"
            mode["for_groupby"] = "Mode"
            min_price["for_groupby"] = "Min Price"
            max_price["for_groupby"] = "Max Price"
            min_price_date["Metrics"] = "Min Price's Date"
            max_price_date["Metrics"] = "Max Price's Date"
            metric_data = [mean, median, mode, min_price, max_price]

            for data in metric_data:
                data.rename({"for_groupby": "Metrics"}, axis="columns", inplace=True)

            metric_combine = pd.concat(metric_data)
            metric_combine = metric_combine.round(2)
            metric_combine = pd.concat([metric_combine, min_price_date, max_price_date])
            for i in range(len(y_data)):
                metric_combine.rename(columns={y_data[i]: table_column[i]}, inplace=True)

            #     metric_combine.rename(columns = {"Shopee Price":"Shopee","Lazada Price":"Lazada","PGMall Price":"PGMall"}, inplace = True)

            data_table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in metric_combine.columns],
                data=metric_combine.to_dict("records"),
                #         filter_action = "native",
                sort_action="native",
                #         export_format = "csv",
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

            # pie chart
            platform_min_count = [0] * len(y_data)
            for index, row in df.iterrows():
                min_price = row[y_data[0]]
                for column in y_data:
                    if min_price >= row[column]:
                        min_price = row[column]

                for i in range(len(y_data)):
                    if row[y_data[i]] == min_price:
                        platform_min_count[i] = platform_min_count[i] + 1
            #             if row["Lazada Price"] == min_price:
            #                 lazada +=1
            #             if row["PGMall Price"] == min_price:
            #                 pgmall +=1
            min_price_df = pd.DataFrame({"Platform": table_column, "Min Price Time": platform_min_count})

            pie_chart = px.pie(
                min_price_df,
                values="Min Price Time",
                names="Platform",
                title=f"Frequency of Minimum Price from {df['Date'].min().strftime('%d-%b-%Y')} to {df['Date'].max().strftime('%d-%b-%Y')} "
            )

            pie_chart.update_traces(textinfo='percent+value')
            pie_chart.update_layout(
                title={
                    "x": 0.5,
                    "y": 0.90,
                    "font": {"size": 25}
                },
            )
            pie_chart.update_layout(
                margin=dict(l=0, r=0, t=140, b=0),  # Adjust the left, right, top, and bottom margins
                #             height=400,                           # Set the height of the chart
                #             width=600                             # Set the width of the chart
            )

            y_data.append("Date")
            for i in range(len(y_data_removed)):
                y_data.append(y_data_removed[i])
                table_column.append(table_column_removed[i])

            return line_chart, data_table, pie_chart

    def run(self):
        # Run the Dash app in a separate thread
        thread = threading.Thread(target=self.app.run_server,
                                  kwargs={"port": 4001, "debug": False, "use_reloader": False})
        thread.start()
        webbrowser.open('http://127.0.0.1:4001/')
        # self.app.run_server(debug=True, jupyter_mode="external")
