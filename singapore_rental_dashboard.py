import pandas as pd
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

import plotly.express as px

import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from difflib import SequenceMatcher
import webbrowser
import threading
class Sg_rental_dashboard():
    def __init__(self,path):
        dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
        load_figure_template("SLATE")
        app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])


        def similar(str1, str2):
            return SequenceMatcher(None, str1, str2).ratio()

        def drop_duplicate_row(duplicated_items, duplicated_column_name, check_item_column_name, rental):
            for i in range(len(duplicated_items)):
                isFirst = True
                isbreak = False
                while isFirst | isbreak:
                    isbreak = False
                    isFirst = False
                    item = duplicated_items[i]
                    data = rental[rental[duplicated_column_name] == item]
                    for j in range(len(data)):
                        data_series = data.iloc[j]
                        if isbreak:
                            break
                        for k in range(len(data)):
                            if j != k:

                                similar_score = similar(data.iloc[k][check_item_column_name],
                                                        data.iloc[j][check_item_column_name])

                                if (similar_score >= 0.75) & (
                                        data.iloc[j]["Rental(SGD)"] == data.iloc[k]["Rental(SGD)"]):
                                    rental.drop(index=data.iloc[k].name, inplace=True)
                                    isbreak = True
                                    break
                                else:
                                    isbreak = False

        rental_df = pd.read_csv(path + "sg rental.csv")

        # drop duplicates rows
        rental_df["Adress_check"] = rental_df["Address"].apply(
            lambda x: x.strip().lower().replace(",", "").replace(" ", ""))
        rental_df["Description_check"] = rental_df["Description"].apply(
            lambda x: x.strip().lower().replace(",", "").replace("\n", "").replace(" ", "") if type(x) == str else "-")
        rental_df.drop_duplicates(subset=["Description", "Adress_check"], inplace=True)
        duplicated_description = rental_df[rental_df["Description"].duplicated()]["Description"].unique().tolist()
        duplicated_address = rental_df[rental_df["Address"].duplicated()]["Address"].unique().tolist()
        drop_duplicate_row(duplicated_description, "Description", "Adress_check", rental_df)
        drop_duplicate_row(duplicated_address, "Address", "Description_check", rental_df)

        rental_df["Date"] = rental_df["Date"].apply(lambda x: x.replace("-", "/"))
        rental_df["Date"] = pd.to_datetime(rental_df["Date"], dayfirst=True)

        if os.path.exists('area_region.json'):
            f = open('area_region.json')
            area_list = json.load(f)
            f.close()
        else:
            service = Service()
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://en.wikipedia.org/wiki/Planning_Areas_of_Singapore")
            table = driver.find_elements(By.CSS_SELECTOR, "table.sortable")
            table_body = table[0].find_element(By.CSS_SELECTOR, 'tbody')
            areas = table_body.find_elements(By.CSS_SELECTOR, "tr")
            area_list = {}
            for i in range(len(areas)):
                item = areas[i].find_elements(By.CSS_SELECTOR, "td > a")
                area_list[item[0].text] = item[1].text
            driver.quit()

            with open("area_region.json", "w") as outfile:
                json.dump(area_list, outfile)

        rental_df["Area"] = rental_df["Location"].apply(lambda x: x[x.find("(") + 1:] if x.find("(") != -1 else x)
        rental_df["Area"] = rental_df["Area"].apply(lambda x: x[x.find("(") + 1:-1] if x.find("(") != -1 else x)
        rental_df["Area"] = rental_df["Area"].apply(lambda x: x.replace(")", ""))
        rental_df["Region"] = rental_df["Area"].apply(lambda x: area_list[x])

        app.layout = html.Div([
            html.H1(["Singapre Rooms Rental Analysis "], style={"text-align": "center"}),
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
                dbc.Col([dbc.Card(id="data-table")], width=3),
                dbc.Col(dbc.Card([dcc.Graph(id="pie-chart")]), width=3),
                dbc.Col([dbc.Card([
                    dcc.RadioItems(
                        id="metrics",
                        options=["Highest Price", "Lowest Price"],
                        value="Highest Price",
                        inline=True,
                    ),
                    dcc.Graph(id="bar-chart")
                ])], width=6),

            ])
        ])

        @app.callback(
            Output("hist-chart", "figure"),
            Output("data-table", "children"),
            Output("pie-chart", "figure"),
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
            region_df = df.groupby("Region").count()["Date"]
            pie = px.pie(values=region_df.values, names=region_df.index, title='Number of Advertisements by Region')
            pie.update_traces(textposition='inside', textinfo='percent+label')
            pie.update_layout(
                showlegend=False,
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 20
                    }
                }, )
            if metrics == "Highest Price":
                is_ascending = False
                title_components = "Highest"
            else:
                is_ascending = True
                title_components = "Lowest"
            area_df = df.groupby("Area")["Rental(SGD)"].mean().sort_values(ascending=is_ascending)[0:10]

            bar = px.bar(
                x=area_df.index,
                y=area_df.values,
                title=f"Top 10 {title_components} Rental by Area"
            )
            bar.update_layout(
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 20
                    }
                }, )
            return hist, stat_table, pie, bar

        thread = threading.Thread(target=app.run_server,
                                  kwargs={"port": 4002, "debug": False, "use_reloader": False})
        thread.start()
        webbrowser.open('http://127.0.0.1:4002/')

