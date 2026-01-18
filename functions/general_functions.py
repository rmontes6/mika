import pandas as pd

def current_year_data():
    data_excel = pd.ExcelFile('data/Detalle_Gastos_Ganancias.xlsx')
    data = [pd.read_excel('data/Detalle_Gastos_Ganancias.xlsx', sheet_name=sheet) for sheet in data_excel.sheet_names]
    for i in range(len(data)):
        if data[i][(data[i]['Categoria'] == 'Ingresos') & (data[i]['Mes'] == 'Enero')]['Cantidad ACT'].iloc[0] > 0:
            current_year = int(data_excel.sheet_names[i])
    return current_year

def previous_year_data():
    act_year = current_year_data()
    data_excel = pd.ExcelFile('data/Detalle_Gastos_Ganancias.xlsx')
    if act_year == int(data_excel.sheet_names[0]):
        previous_year_data = None
    else:
        previous_year_data = act_year- 1
    return previous_year_data

def main_df():
    # years = [previous_year_data(), current_year_data()]
    years = []
    data = pd.read_excel('data/Detalle_Gastos_Ganancias.xlsx', sheet_name='Summary')
    # for i in range(len(data)):
    data = data[['Año', 'Mes', 'Categoria', 'Cantidad ACT', 'Cantidad TGT']].fillna(0)
    # data[i] = data[i][['Año', 'Mes', 'SubCategoria', 'Categoria', 'Cantidad ACT', 'Cantidad TGT', 'Cantidad PY']].fillna(0)
    data['ACT vs TGT'] = data['Cantidad ACT'] - data['Cantidad TGT']
    # data[i]['ACT vs PY'] = data[i]['Cantidad ACT'] - data[i]['Cantidad PY'] 
    # df = pd.concat(data, ignore_index=True)
    return data

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
