import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


###EXPENSES FUNCTIONS###
###KPI that shows actual month expenses given a selected month###
def kpi_month_expenses(data_frame, month, year):
    df_prev = data_frame[(
        data_frame['Año'] == year) & (data_frame['Mes'] == month
    )].groupby(['Categoria']).sum().drop(['Inicial', 'Ingresos']).reset_index()
    expenses_act = df_prev['Cantidad ACT'].sum()
    expenses_tgt = df_prev['Cantidad TGT'].sum()

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = expenses_act,
        delta = {'reference': expenses_tgt, 'valueformat':'f', "suffix": "€", "font":{"size":20}},
        number = {'valueformat':'f', "suffix": "€", "font":{"size":60, "color":"#0460A9"}},
        title = f'Gastos ACT de {month} {year}'
    ))

    return fig

###KPI that shows total expense up to the current month###
def kpi_year_total_expenses(data_frame, year):
    df_prev = data_frame[(
        data_frame['Año'] == year
    )].groupby(['Categoria', 'Mes']).sum().drop(['Inicial']).reset_index()
    df_prev = df_prev.pivot(index='Mes', columns='Categoria', values=['Cantidad ACT', 'Cantidad TGT'])
    df_prev = df_prev[df_prev['Cantidad ACT']['Ingresos']>0]
    total_expenses_act = df_prev['Cantidad ACT'].drop('Ingresos', axis=1).sum(axis=1).sum()
    total_expenses_tgt = df_prev['Cantidad TGT'].drop('Ingresos', axis=1).sum(axis=1).sum()

    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=total_expenses_act,
        delta={'reference': total_expenses_tgt, 'valueformat':'f', "suffix": "€", "font":{"size":20}},
        number={'valueformat':'f', "suffix": "€", "font":{"size":60, "color":"#0460A9"}},
        title={"text": f'Gastos totales ACT {year}'}
    ))
    return fig

###Combo Chart that shows ACT and TGT phasing expenses and ACT income per month###
def phasing_expenses(data_frame, year):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    df_prev = data_frame[data_frame['Año'] == year].groupby(['Categoria', 'Mes']).sum().drop(['Inicial', 'Ingresos']).reset_index()
    df_prev = df_prev.groupby(['Mes']).sum().reset_index()[['Mes', 'Cantidad ACT', 'Cantidad TGT']]
    df_prev['Mes'] = pd.Categorical(df_prev['Mes'], categories=meses, ordered=True)
    df_prev = df_prev.sort_values('Mes')
    df_prev['Cantidad ACT'] = abs(df_prev['Cantidad ACT'])
    df_prev['Cantidad TGT'] = abs(df_prev['Cantidad TGT'])

    df_ingresos = data_frame[data_frame['Año'] == year].groupby(['Categoria', 'Mes']).sum().loc['Ingresos'].drop(['Año', 'ACT - TGT', 'Cantidad TGT'], axis=1).reset_index()
    df_ingresos['Mes'] = pd.Categorical(df_ingresos['Mes'], categories=meses, ordered=True)
    df_ingresos = df_ingresos.sort_values('Mes')
    df_ingresos = df_ingresos[df_ingresos['Cantidad ACT'] > 0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_ingresos['Mes'],
        y=df_ingresos['Cantidad ACT'],
        name="Ingresos ACT",
        marker_color='#002F5C',
        mode="markers"
    ))
    fig.add_trace(go.Bar(
        x=df_prev['Mes'],
        y=df_prev['Cantidad ACT'],
        name="Gastos ACT",
        marker_color='#0460A9'
    ))
    fig.add_trace(go.Scatter(
        x=df_prev['Mes'],
        y=df_prev['Cantidad TGT'],
        name="Gastos TGT",
        marker_color='#9ABFDC'
    ))
    fig.update_layout(
        title = f"Analisis Mensual de Gastos {year} ",
        showlegend = True
    )
    return fig

###Two Pie Charts showing ACT and TGT expenses per category###
def weight_expenses(data_frame, month, year):
    df_prev = data_frame[
        (data_frame['Mes'] == month) & (data_frame['Año'] == year)
    ].groupby('Categoria').sum().drop(['Inicial', 'Ingresos']).reset_index()
    df_prev['Cantidad ACT'] = abs(df_prev['Cantidad ACT'])
    df_prev['Cantidad TGT'] = abs(df_prev['Cantidad TGT'])

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])
    fig.add_trace(go.Pie(
        values=df_prev['Cantidad ACT'],
        labels=df_prev['Categoria'],
        domain=dict(x=[0, 0.5]),
        name="ACT",
        title='ACT'), 
        row=1, col=1
    )
    fig.add_trace(go.Pie(
        values=df_prev['Cantidad TGT'],
        labels=df_prev['Categoria'],
        domain=dict(x=[0.5, 1.0]),
        name="TGT",
        title='TGT'), 
        row=1, col=2
    )
    fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r))
    fig.update_layout(
        title = f"Peso de Gastos ACT Y TGT en {month} {year} ",
        showlegend = True
    )
    return fig

###Bar Chart showing ACT, TGT diff in order to see the expense margin per category###
def expenses_margin(data_frame, month, year):
    df_mg = data_frame[
                (data_frame['Mes'] == month) & 
                (data_frame['Año'] == year)
            ].drop(['SubCategoria'], axis=1).groupby('Categoria').sum().drop(['Inicial', 'Ingresos']).reset_index()
    colors = ["#ffa590" if i < 0 else "#c7ddb5" for i in df_mg['ACT - TGT'].values]
    
    fig = go.Figure(go.Bar(
        x=df_mg['Categoria'],
        y=df_mg['ACT - TGT'],
        name="ACT",
        marker_color=colors
    ))
    fig.update_layout(
        title = f"Margen de gastos {month} {year} ",
        showlegend = False
    )
    return fig
