import requests
import urllib.parse
import pandas as pd
import numpy as np


import plotly.offline as pyo
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

def get_api_call(ids, **kwargs):
    API_BASE_URL = "https://apis.datos.gob.ar/series/api/"
    kwargs["ids"] = ",".join(ids)
    return "{}{}?{}".format(API_BASE_URL, "series", urllib.parse.urlencode(kwargs))

    #variacionmensual
ipc=pd.read_csv(get_api_call([ '173.1_ECIONALLES_DIC-_0_12',
    '173.1_INUCLEOLEO_DIC-_0_10',
    '173.1_RLADOSDOS_DIC-_0_9', '145.3_INGNACUAL_DICI_M_38'], format="csv"), index_col='indice_tiempo')
ipc=ipc*100
ipc.rename(columns={
 'estacionales': 'Estacionales',
  'ipc_nucleo': 'Núcleo',
  'ipc_regulados': 'Regulados',
  'ipc_ng_nacional_tasa_variacion_mensual': 'Nivel General',
 }, inplace=True)

ipcxcomponente= pd.read_csv(get_api_call(['146.3_IALIMENNAL_DICI_M_45',
'146.3_IBEBIDANAL_DICI_M_39',
'146.3_IBIENESNAL_DICI_M_36',
'146.3_ICOMUNINAL_DICI_M_27',
'146.3_IEDUCACNAL_DICI_M_22',
'146.3_IPRENDANAL_DICI_M_35', '146.3_IRECREANAL_DICI_M_31', '146.3_ISALUDNAL_DICI_M_18', '146.3_ITRANSPNAL_DICI_M_23', '146.3_IVIVIENNAL_DICI_M_52'], format="csv"), index_col='indice_tiempo')

ipcxcomponente.rename(columns={'ipc_nivel_general_nacional': 'Nivel General',
       'ipc_alimentos_bebidas_no_alcoholicas_nacional': 'Alimentos y bebidas no alcohólicas',
       'ipc_bebidas_alcoholicas_tabaco_nacional': 'Bebidas alcohólicas y tabaco',
       'ipc_bienes_servicios_varios_nacional': 'Otros bienes y servicios', 'ipc_comunicaciones_nacional': 'Comunicación',
       'ipc_educacion_nacional': 'Educación',
       'ipc_equipamiento_mantenimientos_hogar_nacional': 'Equipamiento y mantenimiento del hogar',
       'ipc_prendas_vestir_calzado_nacional': 'Prendas de vestir y calzado',
       'ipc_recreacion_cultura_nacional': 'Recreación y cultura', 'ipc_restaurantes_hoteles_nacional': 'Restaurantes y hoteles',
       'ipc_salud_nacional': 'Salud', 'ipc_transporte_nacional': 'Transporte',
       'ipc_vivienda_agua_electricidad_combustibles_nacional' : 'Vivienda, agua,electricidad, gas y otros combustibles'}, inplace=True)

infxzona=pd.read_csv(get_api_call(['145.3_INGNACUAL_DICI_M_38',
'145.3_INGCUYUAL_DICI_M_34',
'145.3_INGNEAUAL_DICI_M_33',
'145.3_INGNOAUAL_DICI_M_33',
'145.3_INGPAMUAL_DICI_M_38',
'145.3_INGPATUAL_DICI_M_39'], format="csv"), index_col='indice_tiempo')
infxzona=infxzona*100
infxzona.rename (columns={'ipc_ng_nacional_tasa_variacion_mensual': 'Nacional',
       'ipc_ng_cuyo_tasa_variacion_mensual': 'Cuyo',
       'ipc_ng_nea_tasa_variacion_mensual': 'Noreste',
       'ipc_ng_noa_tasa_variacion_mensual': 'Noroeste',
       'ipc_ng_pampeana_tasa_variacion_mensual': 'Pampeana',
       'ipc_ng_patagonia_tasa_variacion_mensual': 'Patagónica'}, inplace=True)

# Launch the application:

app = dash.Dash()
server = app.server

# Create a Dash layout that contains a Graph component:
app.layout = html.Div([
    dcc.Graph( id='ipc', figure={
            'data': [
                go.Scatter(
                    x = ipc.index,
                    y = ipc[col],
                    mode = 'lines', name=col ) for col in ipc.columns
            ],
            'layout': go.Layout(
                title = 'Índice de precios al consumidor. Variaciones mensuales, según categorías. Total nacional',
                xaxis = {'title': 'Período'},
                yaxis = {'title': 'Var.mensual %'},
                hovermode='closest')
        }
    ),
    dcc.Graph(id='ipcxcomponente', figure={
            'data': [
                go.Scatter(x = ipcxcomponente.index, y = ipcxcomponente[col],  mode = 'markers+lines', name=col) for col in ipcxcomponente.columns
        ],
        'layout': go.Layout(
                title = 'Índice de precios al consumidor. Según divisiones.Total nacional',
                xaxis = {'title': 'Período'},
                yaxis = {'title': 'Indice Base 100=2016'},
                hovermode='closest')
        }
    ),
    dcc.Graph(id='ipcxzonas', figure={
        'data': [
        go.Scatter(x=infxzona.index, y = infxzona[col], name=col, mode='markers') for col in infxzona.columns
    ],
        'layout': go.Layout(
         title = 'Índice de precios al consumidor. Variaciones mensuales. Total nacional y regiones',
                xaxis = {'title': 'Período'},
                yaxis = {'title': 'Var.mensual %'},
                hovermode='closest')
    })
    ])

# Add the server clause:
if __name__ == '__main__':
    app.run_server()
