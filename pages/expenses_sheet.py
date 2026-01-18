from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from functions import expenses_functions, general_functions
from app import main_app

df = general_functions.main_df()

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("Expenses Sheet")
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
                # value=general_functions.last_month_data(df, general_functions.current_year_data()),
                value=general_functions.last_month_data(df, 2026)
            ),
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='kpi-month-expenses',
                figure={}
            )], width=3),
        dbc.Col([
            dcc.Graph(
                id='kpi-year-total-expenses',
                figure=expenses_functions.kpi_year_total_expenses(df, 2026)
            )], width=3),
        dbc.Col([
            dcc.Graph(
                id='expenses-margin',
                figure={}
            )], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='phasing-expenses',
                figure=expenses_functions.phasing_expenses(df, 2026)
            )], width=6),
        dbc.Col([
            dcc.Graph(
                id='weight-expenses',
                figure={}
            )], width=6)
    ])   
],fluid=True)

@main_app.app.callback([Output("kpi-month-expenses", 'figure'),
               Output("expenses-margin", 'figure'),
               Output("weight-expenses", 'figure')], Input("month", "value"))
def expenses(value):
    return expenses_functions.kpi_month_expenses(df, value, 2026), \
           expenses_functions.expenses_margin(df, value, 2026), \
           expenses_functions.weight_expenses(df, value, 2026)
