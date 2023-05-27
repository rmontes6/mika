from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from functions import savings_functions, general_functions
from app import main_app

df = general_functions.main_df()
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("Income Sheet")
        ], width=4),
        dbc.Col([
            dbc.RadioItems(
                id="month",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline",
                labelCheckedClassName="active",
                inline=True,
                options=[
                    {"label": "Jan", "value": "Enero"},
                    {"label": "Feb", "value": "Febrero"},
                    {"label": "Mar", "value": "Marzo"},
                    {"label": "Apr", "value": "Abril"},
                    {"label": "May", "value": "Mayo"},
                    {"label": "Jun", "value": "Junio"},
                    {"label": "Jul", "value": "Julio"},
                    {"label": "Aug", "value": "Agosto"},
                    {"label": "Sep", "value": "Septiembre"},
                    {"label": "Oct", "value": 'Octubre'},
                    {"label": "Nov", "value": "Noviembre"},
                    {"label": "Dec", "value": "Diciembre"},
                ],
                value=general_functions.last_month_data(df, 2023),
            ),
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='kpi-month-savings',
                figure={}
            )], width=3),
        dbc.Col([
            dcc.Graph(
                id='kpi-accumulated-savings',
                figure={}
            )], width=3),
        dbc.Col([
            dcc.Graph(
                id='savings-estimation',
                figure={}
            )], width=6),
    ]), 
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='phasing-savings',
                figure=savings_functions.phasing_savings(df, 2023)
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='phasing-final-year-estimation-income',
                figure=savings_functions.phasing_final_year_estimation_income(df, 2023)
            )
        ], width=6)
    ])
], fluid=True)

@main_app.app.callback([Output("kpi-month-savings", 'figure'),
               Output("savings-estimation", 'figure'), Output("kpi-accumulated-savings", 'figure')], 
               Input("month", "value"))
def expenses_KPI(value):
    return savings_functions.kpi_month_savings(df, value, 2023), \
           savings_functions.savings_estimation(df, value, 2023), \
           savings_functions.kpi_accumulated_savings(df, value, 2023)