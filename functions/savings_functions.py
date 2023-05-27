import pandas as pd
import plotly.graph_objects as go
from functions import general_functions


def kpi_month_savings(data_frame, month, year):
    df_prev = data_frame[(
        data_frame['Año'] == year) & (data_frame['Mes'] == month
    )].groupby(['Categoria']).sum().drop(['Inicial']).reset_index()
    expenses_act = df_prev['Cantidad ACT'].sum()
    expenses_tgt = df_prev['Cantidad TGT'].sum()

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = expenses_act,
        delta = {'reference': expenses_tgt, 'valueformat':'f', "suffix": "€", "font":{"size":20}},
        number = {'valueformat':'f', "suffix": "€", "font":{"size":60, "color":"#0460A9"}},
        title = f'ACT Savings {month} {year}'
    ))
    return fig

def kpi_accumulated_savings(data_frame, month, year):
    df_prev = data_frame[(
        data_frame['Año'] == year
    )].groupby(['Categoria', 'Mes']).sum().reset_index()
    df_prev = general_functions.sort_df_by_month(df_prev)
    df_prev = df_prev.pivot(index='Mes', columns='Categoria', values=['Cantidad ACT', 'Cantidad TGT', 'ACT - TGT'])
    df_prev = df_prev[df_prev['Cantidad ACT']['Ingresos']>0][['ACT - TGT']]
    savings = df_prev[:month]['ACT - TGT'].drop('Inicial', axis=1).sum().sum()

    fig = go.Figure(go.Indicator(
        mode="number",
        value=savings,
        number={'valueformat':'f', "suffix": "€", "font":{"size":60, "color":"#0460A9"}},
        title={"text": f'Accumulated savings by {month} {year}'}
    ))
    return fig

def savings_estimation(data_frame, month, year):
    df_prev = data_frame[
        (data_frame['Mes'] == month) & (data_frame['Año'] == year)
    ].groupby('Categoria').sum()[["Cantidad ACT", "Cantidad TGT", 'ACT - TGT']].drop(['Inicial'])
    df_prev.reset_index()
    vACT = df_prev.loc['Ingresos']['Cantidad ACT'] + (df_prev['Cantidad ACT'].sum() - df_prev.loc['Ingresos']['Cantidad ACT'])
    vTGT = df_prev.loc['Ingresos']['Cantidad TGT'] + (df_prev['Cantidad TGT'].sum() - df_prev.loc['Ingresos']['Cantidad TGT'])
    values = df_prev['ACT - TGT'].values.tolist()
    values.insert(0, vTGT)
    values.append(vACT)
    categorias = df_prev.index.values.tolist()
    categorias.insert(0, 'TGT')
    categorias.append('ACT')
    measure = ['relative'] * (len(df_prev.index)+1)
    measure.append('total')

    fig = go.Figure(go.Waterfall(
        measure = measure,
        x = categorias,
        y = values,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        increasing = {"marker":{"color":"#0460A9"}},
        decreasing = {"marker":{"color":"#9ABFDC"}},
        totals = {"marker":{"color":'#002F5C'}}
    ))
    fig.add_shape(
    type="rect", fillcolor='#002F5C', line=dict(color='#002F5C'), opacity=1,
    x0=-0.4, x1=0.4, xref="x", y0=0.0, y1=fig.data[0].y[0], yref="y"
)
    fig.update_layout(
        title = f"Savings estimation {month} {year}",
        showlegend = False
    )
    return fig

def phasing_savings(data_frame, year):
    df_prev = data_frame[(
        data_frame['Año'] == year
    )].groupby(['Categoria', 'Mes']).sum().drop(['Inicial']).reset_index()
    df_prev = df_prev.groupby(['Mes']).sum().reset_index()[['Mes', 'Cantidad ACT', 'Cantidad TGT', 'ACT - TGT']]
    df_prev = general_functions.sort_df_by_month(df_prev)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_prev['Mes'],
        y=df_prev['Cantidad ACT'],
        name="ACT",
        marker_color='#0460A9'
    ))
    fig.add_trace(go.Scatter(
        x=df_prev['Mes'],
        y=df_prev['Cantidad TGT'],
        name="TGT",
        marker_color='#9ABFDC'
    ))
    fig.update_layout(
        title = f"Monthly savings analysis {year} ",
        showlegend = True
    )
    return fig

def phasing_final_year_estimation_income(data_frame, year):
    df_prev = data_frame[(
        data_frame['Año'] == year
    )].groupby(['Categoria', 'Mes']).sum().reset_index()
    df_prev = general_functions.sort_df_by_month(df_prev)
    df_prev = df_prev.pivot(index='Mes', columns='Categoria', values=['Cantidad ACT', 'Cantidad TGT', 'ACT - TGT'])
    df_prev = df_prev[df_prev['Cantidad ACT']['Ingresos']>0][['ACT - TGT']]
    df_prev = df_prev[:]['ACT - TGT'].drop('Inicial', axis=1)
    savings_per_month = []
    for month in df_prev.index:
        savings_per_month.append(df_prev[:month].sum().sum())

    df_prev = data_frame[(
        (data_frame['Año'] == year) & (data_frame['Mes'] == 'Diciembre')
    )].groupby(['Categoria']).sum().reset_index()
    total_tgt_end_year = df_prev['Cantidad TGT'].sum()
    total = [(total_tgt_end_year + i).round(2) for i in savings_per_month]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=general_functions.phasing_dimension(),
        y=total,
        marker_color='#9ABFDC'
    ))
    fig.add_hline(y=total_tgt_end_year, line_color='#0460A9')
    fig.update_yaxes(tickformat = "digits", range=list([total_tgt_end_year*0.95, max(total)*1.05]))
    fig.update_layout(
        title = f"End-year balance estimation by Month {2023}",
        showlegend = False
    )
    return fig
