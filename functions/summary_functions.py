import pandas as pd
import plotly.graph_objects as go
from functions import general_functions


def kpi_balance(data_frame, month, year):
    df_prev = data_frame[(
            (data_frame['Año'] == year) & (data_frame['Mes'] == month)
        )][['Mes', 'Categoria', 'Cantidad ACT', 'Cantidad TGT']]
    act_balance = df_prev['Cantidad ACT'].sum()
    tgt_balance = df_prev['Cantidad TGT'].sum()

    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=act_balance,
        delta={'reference': tgt_balance, 'valueformat':'f', "suffix": "€", "font":{"size":20}},
        number={'valueformat':'f', "suffix": "€", "font":{"size":60, "color":"#0460A9"}},
        title={"text": f'ACT Balance {month} {year}'}
    ))
    return fig

def kpi_balance_estimation_endyear(data_frame, year):
    df_prev = data_frame[(
        data_frame['Año'] == year
    )].groupby(['Categoria', 'Mes']).sum().reset_index()
    df_prev = general_functions.sort_df_by_month(df_prev)
    df_prev = df_prev.pivot(index='Mes', columns='Categoria', values=['Cantidad ACT', 'Cantidad TGT', 'ACT vs TGT'])
    df_prev = df_prev[df_prev['Cantidad ACT']['Ingresos']>0]
    savings = df_prev.tail(1)['Cantidad ACT'].sum().sum() - df_prev.tail(1)['Cantidad TGT'].sum().sum()

    df_prev = data_frame[(
        (data_frame['Año'] == year) & (data_frame['Mes'] == 'Diciembre')
    )].groupby(['Categoria']).sum().reset_index()
    tgt = df_prev['Cantidad TGT'].sum()

    fig = go.Figure(go.Indicator(
        mode="number",
        value=savings + tgt,
        number={'valueformat':'f', "suffix": "€", "font":{"size":60, "color":"#0460A9"}},
        title={"text": f'End-year balance estimation {year}'}
    ))
    return fig

def phasing_analysis(data_frame, category, year):
    df_prev = data_frame[
        (data_frame['Año'] == year)
    ][['Mes', 'Categoria', 'Cantidad ACT', 'Cantidad TGT']].groupby(['Categoria', 'Mes']).sum().reset_index()
    df_prev = df_prev[(df_prev['Categoria'] == category)]
    df_prev = general_functions.sort_df_by_month(df_prev)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_prev['Mes'],
        y=df_prev['Cantidad ACT'].round(3),
        name="ACT",
        marker_color='#0460A9'
    ))
    fig.add_trace(go.Scatter(
        x=df_prev['Mes'],
        y=df_prev['Cantidad TGT'].round(3),
        name="TGT",
        marker_color='#9ABFDC'
    ))
    fig.update_layout(
        title = f"Phasing Analysis {category} {year} ",
        showlegend = True
    )
    fig.update_yaxes(tickformat = "digits")
    return fig

def month_table(data_frame, month, year):
    df_table = data_frame[
        (data_frame['Mes'] == month) & 
        (data_frame['Año'] == year)
    ].drop(['Mes', 'Año', 'Categoria'], axis=1)
    cols_to_show = ['SubCategoria', 'Cantidad ACT', 'Cantidad TGT', 'Cantidad PY', 'ACT vs TGT', 'ACT vs PY']
    text_color, background_color = [], []
    n = len(df_table)
    for col in cols_to_show:
        if not col in ('ACT vs TGT', 'ACT vs PY'):
            background_color.append(["white"] * n)
            text_color.append(["black"] * n)
        else:
            df_table['color'] = ["#ffa590" if i < 0 else "#c7ddb5" for i in df_table[col]]
            background_color.append(df_table['color'].to_list())
            text_color.append(["white"] * n)
    df_table = df_table.drop(['color'], axis=1)
    
    fig = go.Figure(
        data = [go.Table(
            header=dict(
                values=list(df_table.columns),
                fill_color='#0460A9',
                align='center',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values = df_table[['SubCategoria', 'Cantidad ACT', 'Cantidad TGT', 'Cantidad PY', 'ACT vs TGT', 'ACT vs PY']].round(3).values.T,
                fill_color=background_color,
                align='right',
                font=dict(color=text_color, size=12),
                height=20
            )
        )
    ])
    fig.update_layout(
        title = f"Categorical Analysis {month} {year}",
        showlegend = False
    )
    return fig
