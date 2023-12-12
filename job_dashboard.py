import pandas as pd
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
from dash_holoniq_wordcloud import DashWordcloud
import plotly.express as px
import warnings
import threading
import webbrowser

warnings.filterwarnings("ignore", category=UserWarning)


class JobDashboard:
    def __init__(self, path):
        def process_data(dataframe):
            mask_type1 = dataframe["Job Type"] == "Full-Time"
            mask_type2 = dataframe["Job Type"] == "Temporary"
            mask_type3 = dataframe["Job Type"] == "Contract"
            mask_type4 = dataframe["Job Type"] == "Part-Time"
            mask_type5 = dataframe["Job Type"] == ' '

            dataframe.loc[mask_type1, "Job Type"] = "Full time"
            dataframe.loc[mask_type2, "Job Type"] = "Contract/Temp"
            dataframe.loc[mask_type3, "Job Type"] = "Contract/Temp"
            dataframe.loc[mask_type4, "Job Type"] = "Part time"
            dataframe.loc[mask_type5, "Job Type"] = "Undefined"

            mask = dataframe[
                       "Company Name"] == "PERSOLKELLY Singapore Pte Ltd (Formerly Kelly Services Singapore Pte Ltd)"
            mask2 = dataframe["Company Name"] == "ST Engineering Training & Simulation Systems Pte Ltd"
            mask3 = dataframe["Company Name"] == "QUESS CORP SINGAPORE PTE. LTD. / QUESS SINGAPORE"
            mask4 = dataframe["Company Name"] == "Government Technology Agency of Singapore (GovTech)"
            mask5 = dataframe["Company Name"] == "Oversea-Chinese Banking Corporation Ltd "
            mask6 = dataframe["Company Name"] == "Agency for Science, Technology and Research (A*STAR)"

            dataframe.loc[mask, "Company Name"] = "PERSOLKELLY Singapore Pte Ltd"
            dataframe.loc[mask2, "Company Name"] = "ST Engineering Training & Simulation Systems"
            dataframe.loc[mask3, "Company Name"] = "QUESS SINGAPORE"
            dataframe.loc[mask4, "Company Name"] = "GovTech"
            dataframe.loc[mask5, "Company Name"] = "OCBC Singapore"
            dataframe.loc[mask6, "Company Name"] = "A * STAR"
            return dataframe

        def count_frequency(tokens):
            word_count = {}
            for token in tokens:
                token = token.replace("[", "").replace("]", "").replace("'", "").replace("'", "").split(",")
                for i in range(len(token)):
                    word = token[i].strip()

                    if word in word_count.keys():
                        word_count[word] += 1
                    else:
                        word_count[word] = 1
            return word_count

        def process_job_title(title):
            if len(title) > 30:
                index = title.find("(")
                index2 = title.find("|")
                index3 = title.find("-")

                title = title[:index] if index != -1 else title
                title = title[:index2] if index2 != -1 else title
                title = title[:index3] if index3 != -1 else title
            #         if index != -1:
            #             title = title[:index]
            #         if index2 !=-1:
            #             print(title)
            #             title = title[:index2]
            #             print(title)
            return title

        # path = "C:/Users/User/Desktop/web scrap/data/"
        dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
        load_figure_template("SLATE")
        app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

        sg_df = pd.read_csv(f"{path}Singapore Job(Processed).csv")
        my_df = pd.read_csv(f"{path}Malaysia Job(Processed).csv")

        sg_df = process_data(sg_df)
        my_df = process_data(my_df)

        sg_df["Title"] = sg_df["Title"].apply(process_job_title)
        my_df["Title"] = my_df["Title"].apply(process_job_title)

        sg_df["Posted Date"] = sg_df["Posted Date"].apply(lambda x : x.replace("-","/"))
        my_df["Posted Date"] = my_df["Posted Date"].apply(lambda x: x.replace("-", "/"))

        sg_df["Posted Date"] = pd.to_datetime(sg_df["Posted Date"], format="mixed")
        my_df["Posted Date"] = pd.to_datetime(my_df["Posted Date"], format="mixed")

        app.layout = html.Div([
            html.Div(id="title"),
            dbc.Card([
                dbc.Row([
                    dbc.Col([

                        html.P("Please Selact Date Range"),
                        dcc.DatePickerRange(
                            id="date-picker",
                            display_format="YYYY-MMM-DD",
                            className="dbc"
                        )

                    ], ),

                    dbc.Col([

                        html.P("Please Select Country"),
                        dcc.RadioItems(
                            id='country_selector',
                            options=["Malaysia", "Singapore"],
                            value="Malaysia",
                            inline=True
                        )

                    ])

                ])

            ]),

            dbc.Row([
                dbc.Col([dbc.Card([dcc.Graph(id="bar-company")])], width=4),
                dbc.Col([dbc.Card([dcc.Graph(id="burst-location")])], width=4),
                dbc.Col([dbc.Card([dcc.Graph(id="bar-title")])], width=4)
            ]),

            dbc.Row([
                dbc.Col([dbc.Card([dcc.Graph(id="pie-chart")])], width=4),
                dbc.Col([
                    dbc.Card(id="wordcloud")

                ], width=4),
                dbc.Col([dbc.Card([dcc.Graph(id="scatter-chart")])], width=4)
            ])

        ])

        @app.callback(
            Output("title", "children"),
            Output("date-picker", "min_date_allowed"),
            Output("date-picker", "max_date_allowed"),
            Output("date-picker", "start_date"),
            Output("date-picker", "end_date"),
            Input("country_selector", "value")
        )
        def data_title(country):

            if country == "Malaysia":
                df = my_df
            elif country == "Singapore":
                df = sg_df
            #     df = pd.read_csv(f"{path}{country} Job(Processed).csv")
            # df["Posted Date"] = pd.to_datetime(df["Posted Date"])
            # df["Date"] = pd.to_datetime(df["Date"])
            title = html.H1([f"{country} Data Science Jobs Analysis"], style={"text-align": "center"})
            min_date = df["Posted Date"].min()
            max_date = df["Posted Date"].max()
            start_date = df["Posted Date"].sort_values().unique()[-30]
            end_date = df["Posted Date"].sort_values().unique()[-1]

            return title, min_date, max_date, start_date, end_date,

        @app.callback(
            Output("bar-company", "figure"),
            Output("burst-location", "figure"),
            Output("bar-title", "figure"),
            Output("pie-chart", "figure"),
            Output("wordcloud", "children"),
            Output("scatter-chart", "figure"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
            Input("country_selector", "value")
        )
        def create_graph(start_date, end_date, country):
            if country == "Malaysia":
                df = my_df
            elif country == "Singapore":
                df = sg_df

            # df["Posted Date"] = pd.to_datetime(df["Posted Date"])
            # df["Date"] = pd.to_datetime(df["Date"])
            df = df.query(" @start_date <=`Posted Date`<= @end_date")

            company_name_df = df["Company Name"].value_counts()[:10].sort_values()
            bar_company = px.bar(
                x=company_name_df.values,
                y=company_name_df.index,
                title="Top 10 Companies by Number of Advertisements"
            )
            bar_company.update_layout(
                xaxis_title='Number',
                yaxis_title='Company Name',
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 20
                    }
                }, )

            burst_df = df.groupby(["State/Region", "Country/Location"], as_index=False)["Posted Date"].count()
            burst = px.sunburst(burst_df,
                                path=['State/Region', 'Country/Location'],
                                values='Posted Date',
                                title='Job Locations Distribution',
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
            burst.update_layout(
                xaxis_title='Number of Advertisements',
                yaxis_title='Region',
                coloraxis_showscale=False,
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 20
                    }
                },
            )
            bar_title = px.bar(
                x=df['Title'].value_counts()[:10].index,
                y=df['Title'].value_counts()[:10].values,
                title="Top 10 Job Titles by  Number of Advertisements"
            )
            bar_title.update_layout(
                xaxis_title='Job Titles',
                yaxis_title='Number',
                title={
                    "x": 0.5,
                    "y": .87,
                    "font": {
                        "size": 20
                    }
                }, )
            pie = px.pie(
                df,
                values=df["Job Type"].value_counts().values,
                names=df["Job Type"].value_counts().index,
                hole=0.5,
                title="Percentage of Job Type"
            )
            count_word = count_frequency(df["Key Words"])

            count_word_df = pd.DataFrame(count_word.keys(), columns=["Words"])
            count_word_df["Count"] = count_word.values()
            #     count_word_df["Count"] = round(count_word_df["Count"]/count_word_df["Count"].iloc[:num_words_show].sum()*200)

            count_word_word_cloud = []
            for index, row in count_word_df.iterrows():
                count_word_word_cloud.append([row["Words"], row["Count"]])

            wordcloud = DashWordcloud(

                list=count_word_word_cloud,
                width=530, height=450,
                gridSize=16,
                color='#f0f0c0',
                backgroundColor='#001f00',
                shuffle=False,
                rotateRatio=0.0,
                shrinkToFit=True,
                drawOutOfBound=False,
                shape='circle',
                hover=True,
                #                                 weightFactor = 0.35,
                #                                 minSize = 100

            )

            date_count_df = df["Posted Date"].value_counts().reset_index().sort_values("Posted Date")
            scatter = px.scatter(
                date_count_df,
                x="Posted Date",
                y="count",
                title="Number of Job Advertisement"
            )
            scatter.add_hline(
                y=date_count_df["count"].mean(),
                annotation_text="Average Value"
            )
            scatter.update_layout(title={
                "x": 0.5,
                "y": .87,
                "font": {
                    "size": 20
                }
            }, )

            return bar_company, burst, bar_title, pie, wordcloud, scatter

        thread = threading.Thread(target=app.run_server,
                                  kwargs={"port": 4004, "debug": False, "use_reloader": False})
        thread.start()
        webbrowser.open('http://127.0.0.1:4004/')
        # app.run_server(debug=True, port=5001, jupyter_mode="external")
