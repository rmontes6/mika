import pandas as pd

def main_df():
    data = pd.read_excel('data/Detalle_Gastos_Ganancias.xlsx')
    df = data[['Año', 'Mes', 'SubCategoria', 'Categoria', 'Cantidad ACT', 'Cantidad TGT']].fillna(0)
    df['ACT - TGT'] = df['Cantidad ACT'] - df['Cantidad TGT']

    return df

def last_month_data(data_frame, year):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    df_prev = data_frame[(
        data_frame['Año'] == year
    )].groupby(['Categoria', 'Mes']).sum().drop(['Inicial']).reset_index()
    df_prev['Mes'] = pd.Categorical(df_prev['Mes'], categories=meses, ordered=True)
    df_prev = df_prev.sort_values('Mes')
    df_prev = df_prev.pivot(index='Mes', columns='Categoria', values=['Cantidad ACT', 'Cantidad TGT'])
    df_prev = df_prev[df_prev['Cantidad ACT']['Ingresos']>0]

    return df_prev.index[-1]

def phasing_dimension():
    month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return month

def sort_df_by_month(data_frame):
    month = phasing_dimension()
    data_frame['Mes'] = pd.Categorical(data_frame['Mes'], categories=month, ordered=True)
    data_frame = data_frame.sort_values('Mes')

    return data_frame
