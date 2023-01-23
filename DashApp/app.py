from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from prophet.serialize import model_from_json

# from src.layout import create_layout
from data.loader import load_gas_data
from src import ids

DATA_PATH = "../datasets/cleaned/gas_data.xlsx"
# model importing
with open('../models/gas_prophet.json', 'r') as fin:
    gas_model = model_from_json(fin.read())

with open('../models/backuppower_prophet.json', 'r') as fin:
    backuppower_model = model_from_json(fin.read())

with open('../models/water_prophet.json', 'r') as fin:
    water_model = model_from_json(fin.read())

with open('../models/electricity_prophet.json', 'r') as fin:
    electricity_model = model_from_json(fin.read())

all_data = load_gas_data("../datasets/cleaned/all_data.xlsx")


external_stylesheets = [
    dbc.themes.BOOTSTRAP
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets
    )


data = load_gas_data(DATA_PATH)
app.title = "Bityanr Utilities Dashboard"
app.layout = html.Div([

    html.Div(
        className = "visualisation-card",
        children=[
            html.H4('Water Readings Forecast',className="visualisation-title"),
            html.Div(
                id="'water-forecast",
                children=[
                    html.Div(
                        className="selector-column",
                        children=[
                            html.Div(
                                children=[
                                    html.P("Select Utility:"),
                                    dcc.Dropdown(
                                        id="utility-forecast",
                                        options=["backuppower", "water", "gas", "electricity"],
                                        value="water",
                                    )
                                ]
                            )
                    
                        ]
                    ),
                    dcc.Graph("forecast", className="forecast-visualisation"),
                ]

            )
            
            
        ]
    ),
    

    html.Div(
        className = "visualisation-card",
        children=[
            html.H4('Utility Quantities over Time',className="visualisation-title"),
            html.Div(
                className="graph-selector",
                children=[
                    html.Div(
                        className="selector-column",
                        children=[
                            html.Div(
                                children=[
                                    html.P("Select Utility:"),
                                    dcc.Dropdown(
                                        id="utility_quantity",
                                        options=[
                                            {"label": "electricity", "value":37}, 
                                            {"label":"backuppower", "value":11}, 
                                            {"label":"water", "value":36}, 
                                            {"label": "gas", "value":7}, 
                                            {"label":"electricity(cpf)", "value":42}, 
                                            {"label":"water", "value":41}, 
                                            {"label":"backuppower", "value":40}],
                                        value="electricity",
                                    ),
                                ]
                            )
                    
                        ]
                    ),
                    dcc.Graph("utility-bar-chart", className="quantities-graph"),
                ]

            )
            
            
        ]
    ),

    html.Div(
        className = "visualisation-card",
        children=[
            html.H4('Quantity Consumption Per Utility',className="visualisation-title"),
            html.Div(
                className="graph-selector",
                children=[
                    html.Div(
                        className="selector-column",
                        children=[
                            html.Div(
                                children=[
                                    html.P("Select Utility:"),
                                    dcc.Dropdown(
                                        id="id_quantity_year",
                                        className="drop-down-menu",
                                        options=[
                                            {"label": "electricity", "value":37}, 
                                            {"label":"backuppower", "value":11}, 
                                            {"label":"water", "value":36}, 
                                            {"label": "gas", "value":7}, 
                                            {"label":"electricity(cpf)", "value":42}, 
                                            {"label":"water", "value":41}, 
                                            {"label":"backuppower", "value":40}],
                                        value="electricity",
                                    ),
                                ]
                            )
                    
                        ]
                    ),
                    dcc.Graph("readings-yearly", className="quantity-consumption"),
                ]

            )
            
            
        ]
    ),

     html.Div(
        className = "visualisation-card",
        children=[
            html.H4('Yearly Distributions of Quantities',className="visualisation-title"),
            html.Div(
                className="graph-selector",
                children=[
                    html.Div(
                        children = [
                            html.Div(
                                    children=[
                                        html.P("Select Year:"),
                                        dcc.Dropdown(
                                            id="quantity-yearly-dist",
                                            options=[2019,2021,2022,2023],
                                            value=2019,
                                        ),
                                    ]
                                ),
                            
                    ]),
                    dcc.Graph("quantity-yearly-fig", className="violin-graph"),
                    
                ]

            )
            
            
        ]
    ),

     html.Div(
        className = "visualisation-card",
        children=[
            html.H4('Yearly Distributions of Readings',className="visualisation-title"),
            html.Div(
                className="graph-selector",
                children=[
                    html.Div(
                        children = [
                            html.Div(
                                    children=[
                                        html.P("Select Year:"),
                                        dcc.Dropdown(
                                            id="reading-yearly-dist",
                                            options=[2019,2021,2022,2023],
                                            value=2019,
                                        ),
                                    ]
                                ),
                            
                    ]),
                    dcc.Graph("reading-yearly-fig", className="violin-graph"),
                    
                ]

            )
            
            
        ]
    ),

    

    # html.Div(
    #     children=[
    #         html.H4('Yearly Distribution of Quantity Consumed'),
    #         html.Div(
    #             children=[
    #                 html.P("Select Year:"),
    #                 dcc.Dropdown(
    #                     id="quantity-yearly-dist",
    #                     options=[2019,2021,2022,2023],
    #                     value=2019,
    #                 ),
    #             ]
                
    #         ),
    #         dcc.Graph("quantity-yearly-fig"),
    #     ]
    # )    
])

def forecast_graph(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_upper'],
        line=dict(color="firebrick", width=2, dash='dash'),
        name='Upper Limit',
    ))

    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_lower'],
        line=dict(color="royalblue", width=2, dash='dash'),
        name='Lower Limit',
    ))

    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        line_color='rgb(0,100,80)',
        name='Forecast',
    ))

    fig.update_traces(mode='lines')
    return fig

@app.callback(Output("forecast", "figure"),Input("utility-forecast", "value"))
def forecast_utility(utility):

    if utility=="electricity":
        future = electricity_model.make_future_dataframe(periods=200)
        forecast = electricity_model.predict(future)
        fig = forecast_graph(forecast)
        return fig
    elif utility == "backuppower":
        future = backuppower_model.make_future_dataframe(periods=200)
        forecast = backuppower_model.predict(future)
        fig = forecast_graph(forecast)
        return fig
    elif utility=="water":
        future = water_model.make_future_dataframe(periods=200)
        forecast = water_model.predict(future)
        fig = forecast_graph(forecast)
        return fig
    elif utility == "gas":
        future = gas_model.make_future_dataframe(periods=200)
        forecast = gas_model.predict(future)
        fig = forecast_graph(forecast)
        return fig
    

@app.callback(Output("quantity-yearly-fig", "figure"),
    Input("quantity-yearly-dist", "value")
)
def display_year(year):
    mapping = {
        37: "electricity", 
        11:"backuppower", 
        36:"water", 
        7: "gas", 
        42:"electricity(cpf)", 
        41:"water(cpf)",
        40:"backuppower(cpf)"}
    all_data['paymenttermid'] = all_data['paymenttermid'].map(mapping) 
    year_data = all_data[all_data['year'] == year]
    # year_pivot = year_data.pivot_table(values=['quantity'], index=['yearmonth'], aggfunc="mean", fill_value=0)
    fig = px.violin(year_data, y="quantity", points='all', color="paymenttermid")
    return fig


@app.callback(Output("utility-bar-chart", "figure"), Input("utility_quantity", "value"))
def display_time_series(utility):
    df = all_data.query("paymenttermid == @utility")
    gas_time = df.pivot_table(values=['quantity'], index=['yearmonth'], aggfunc="mean", fill_value=0)
    fig = px.bar(gas_time, x=gas_time.index, y='quantity')
    return fig

@app.callback(Output("readings-yearly", "figure"),
    Input("id_quantity_year", "value")
)
def display_year(utility):
    df = all_data.query("paymenttermid == @utility")
    df = df.pivot_table(values=['quantity'], index=['yearmonth'], aggfunc="mean", fill_value=0)
    fig = px.line(df, x=df.index, y="quantity")
    return fig

@app.callback(Output("reading-yearly-fig", "figure"), Input("reading-yearly-dist","value"))
def yearly_reading(year):
    mapping = {
        37: "electricity", 
        11:"backuppower", 
        36:"water", 
        7: "gas", 
        42:"electricity(cpf)", 
        41:"water(cpf)",
        40:"backuppower(cpf)"}
    all_data['paymenttermid'] = all_data['paymenttermid'].map(mapping)
    year_data = all_data[all_data['year'] == year]
    fig =px.violin(year_data, y="reading",  points='all', color="paymenttermid")
    return fig


# def forecast_graph(forecast):
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=forecast['ds'],
#         y=forecast['yhat_upper'],
#         line=dict(color="firebrick", width=2, dash='dash'),
#         name='Upper Limit',
#     ))

#     fig.add_trace(go.Scatter(
#         x=forecast['ds'],
#         y=forecast['yhat_lower'],
#         fill='toself',
#         line=dict(color="royalblue", width=2, dash='dash'),
#         name='Lower Limit',
#     ))

#     fig.add_trace(go.Scatter(
#         x=forecast['ds'],
#         y=forecast['yhat'],
#         line_color='rgb(0,100,80)',
#         name='Gas Forecast',
#     ))

#     fig.update_traces(mode='lines')
#     return fig

# @app.callback(Output("meter-quantity", "figure"), Input("year-quantities", "value"))
# def dislapy_graph(_):
#     data['status'] = data['meterid'].astype("category")
#     fig = px.scatter(data, x="count", y="meterid", color="status")
    # return fig

if __name__ == '__main__':
    app.run_server(debug=True)
