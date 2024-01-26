from dash import html, dcc, Input, Output, callback_context
import dash_bootstrap_components as dbc
from functions import summary_functions, savings_functions, expenses_functions, general_functions
from app import main_app

df = general_functions.main_df()

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("Summary Sheet")
        ], width=2),
        dbc.Col([
            dbc.DropdownMenu(
                id="category",
                label="Categoria", 
                children=[dbc.DropdownMenuItem(i, id=f"{i[0].lower() + i[1:]}") for i in df.groupby('Categoria').sum().reset_index()['Categoria']], 
                direction="down",
                color = 'white',
            )], width=2),
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
                value=general_functions.last_month_data(df, general_functions.current_year_data()),
            ),
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='kpi-balance',
                figure={}
            )], width=3),
        dbc.Col([
            dcc.Graph(
                id='kpi-balance-estimation-endyear',
                figure=summary_functions.kpi_balance_estimation_endyear(df, general_functions.current_year_data())
            )], width=3),
        dbc.Col([
            dcc.Graph(
                id='summary-kpi-month-savings',
                figure={}
            )], width=3),
        dbc.Col([
            dcc.Graph(
                id='summary-kpi-month-expenses',
                figure={}
            )], width=3)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='phasing-analysis',
                figure={}
            )], width=6),
        dbc.Col([
            dcc.Graph(
                id='month-table',
                figure={}
            )], width=6)
    ])   
],fluid=True)

@main_app.app.callback([Output("kpi-balance", 'figure'),
               Output("summary-kpi-month-savings", 'figure'),
               Output("summary-kpi-month-expenses", 'figure'),
               Output("month-table", 'figure')], Input("month", "value"))
def expenses(value):
    return summary_functions.kpi_balance(df, value, general_functions.current_year_data()), \
           savings_functions.kpi_month_savings(df, value, general_functions.current_year_data()), \
           expenses_functions.kpi_month_expenses(df, value, general_functions.current_year_data()), \
           summary_functions.month_table(df, value, general_functions.current_year_data())


@main_app.app.callback(Output("phasing-analysis", 'figure'),
                       [Input(f"{i[0].lower() + i[1:]}", "n_clicks") for i in df.groupby('Categoria').sum().reset_index()['Categoria']],
                       prevent_initial_update=True)
def phasing(*args):
    id_lookup = {}
    categories = [i[0].lower() + i[1:] for i in df.groupby('Categoria').sum().reset_index()['Categoria']]
    values = [i[0].capitalize() + i[1:] for i in categories]
    j = 0
    for i in categories:
        id_lookup[i] = values[j]
        j += 1
    ctx = callback_context

    if not ctx.triggered:
        button_id = 'inicial'
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    return summary_functions.phasing_analysis(df, id_lookup[button_id], general_functions.current_year_data())
