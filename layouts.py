
import requests
import urllib.parse
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

def get_api_call(ids, **kwargs):
    API_BASE_URL = "https://apis.datos.gob.ar/series/api/"
    kwargs["ids"] = ",".join(ids)
    return "{}{}?{}".format(API_BASE_URL, "series", urllib.parse.urlencode(kwargs))

#Definicion de variacion interanual
def compute_anual_variation(df):
    """Compute and return the anual variations values."""
    anual_returns= (df/df.shift(12))-1
    return anual_returns

#Definicion de variacion mensual
def compute_mensual_variation(df):
    mensual=(df/df.shift(1))-1
    return mensual

def vartrimestral(df):
    trimestral=(df/df.shift(4))-1
    return trimestral
def datos(df):
    datos=pd.read_csv(get_api_call([df], format="csv", limit=5000), index_col='indice_tiempo')
    return datos


ipc=pd.read_csv(get_api_call([ '173.1_ECIONALLES_DIC-_0_12',
    '173.1_INUCLEOLEO_DIC-_0_10',
    '173.1_RLADOSDOS_DIC-_0_9',
    '145.3_INGNACUAL_DICI_M_38'], format="csv", limit=5000), index_col='indice_tiempo')
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
'146.3_IPRENDANAL_DICI_M_35', '146.3_IRECREANAL_DICI_M_31', '146.3_ISALUDNAL_DICI_M_18', '146.3_ITRANSPNAL_DICI_M_23', '146.3_IVIVIENNAL_DICI_M_52'], format="csv", limit=5000), index_col='indice_tiempo')

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
'145.3_INGPATUAL_DICI_M_39'], format="csv", limit=5000), index_col='indice_tiempo')
infxzona=infxzona*100
infxzona.rename (columns={'ipc_ng_nacional_tasa_variacion_mensual': 'Nacional',
       'ipc_ng_cuyo_tasa_variacion_mensual': 'Cuyo',
       'ipc_ng_nea_tasa_variacion_mensual': 'Noreste',
       'ipc_ng_noa_tasa_variacion_mensual': 'Noroeste',
       'ipc_ng_pampeana_tasa_variacion_mensual': 'Pampeana',
       'ipc_ng_patagonia_tasa_variacion_mensual': 'Patagónica'}, inplace=True)

#Indicadores de desempleo 42.3_EPH_PUNTUATAL_0_M_30 trimestral
desocupacion= pd.read_csv(get_api_call(['42.3_EPH_PUNTUATAL_0_M_30'], format="csv"), index_col='indice_tiempo')
asalariados=pd.read_csv(get_api_call(['151.1_AARIADOTAC_2012_M_25', '151.1_AARIADOTAC_2012_M_26', '151.1_AARIADOTAC_2012_M_40', '151.1_IPENDIETAC_2012_M_34', '151.1_IPENDIETAC_2012_M_36', '151.1_IPENDIETAC_2012_M_43'], format="csv"), index_col='indice_tiempo')
asalariados.rename(columns={'asalariados_pub_sin_estac':'Asalariados del sector público', 'asalariados_priv_sin_estac':'Asalariados del sector privado',
       'asalariados_casas_particulares_sin_estac': 'Asalariados de casas particulares',
       'independientes_autonomos_sin_estac': 'Independientes autónomos',
       'independientes_monotributo_sin_estac': 'Independientes con monotributo',
       'independientes_monotributo_social_sin_estac': 'Independientes con monotributo social'}, inplace=True)

tc=pd.read_csv(get_api_call(['175.1_DR_ESTANSE_0_0_20'], format="csv", limit=5000, start_date='2010'), index_col='indice_tiempo')

# create traces
tc1= [go.Scatter(
    x = tc.index,
    y = tc['dolar_estadounidense'], mode = 'lines', name='USD', line = dict(width = 5, color = '#1c79c0' ))]

layout = go.Layout(
    title = 'Tipo de Cambio BCRA',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'pesos'},
    legend=dict(orientation="h", traceorder='normal'))

tcrm=pd.read_csv(get_api_call(['116.3_TCRMA_0_M_36'], format="csv", limit=5000), index_col='indice_tiempo')
tcrusa=pd.read_csv(get_api_call(['116.3_TCREU_0_M_31'], format="csv", limit=5000), index_col='indice_tiempo')
tcrbra=pd.read_csv(get_api_call(['116.3_TCRB_0_M_23'], format='csv', limit=5000), index_col= 'indice_tiempo')
tcreuro=pd.read_csv(get_api_call(['116.3_TCRZE_0_M_26'], format='csv', limit=5000), index_col= 'indice_tiempo')

tcrm1= go.Scatter(
    x = tcrm.index,
    y = tcrm['tipo_cambio_real_multilateral_actual'], mode = 'lines', name='Tipo de Cambio Real Multilateral',
    line = dict(width = 5, color = '#1c79c0'))

tcrusa1= go.Scatter(
    x = tcrusa.index,
    y = tcrusa['tipo_cambio_real_estados_unidos'], mode = 'lines', name='TCRM USA',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,
        dash = 'dot'))

tcrbra1= go.Scatter(
    x = tcrbra.index,
    y = tcrbra['tipo_cambio_real_brasil'], mode = 'lines', name='TCRM BRASIL', line=dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,
        dash = 'dash'))

tcreuro1= go.Scatter(
    x = tcreuro.index,
    y = tcreuro['tipo_cambio_real_zona_euro'], mode = 'lines', name='TCRM EURO',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,
        dash = 'dashdot'))

tcrm2=[tcrm1, tcrusa1, tcrbra1,tcreuro1]

layout = go.Layout(
    title = 'Tipo de Cambio Real Multilateral',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'indice base100= Dic2015'},
    legend=dict(orientation="h", traceorder='normal'))

tipodecambio = go.Figure(data=tcrm2,layout=layout)
tasasdeint=pd.read_csv(get_api_call(['89.1_TIAC_0_0_26', '89.1_TIB_0_0_20', '89.1_TIC_0_0_18', '89.1_TIPF35D_0_0_35'], format="csv", start_date=2015, limit=5000), index_col='indice_tiempo')

tasasdeint.rename(columns={'tasas_interes_adelantos_cc': 'Adel.Cta.Cte',
       'tasas_interes_badlar': 'Badlar',
       'tasas_interes_call': 'Call', 'tasas_interes_plazo_fijo_30_59_dias': 'PF+60d'}, inplace=True)

# create traces
adelanto = go.Scatter(
    x = tasasdeint.index,
    y = tasasdeint['Adel.Cta.Cte'], mode='lines',
        line = dict(width = 5, color = ('rgb(22, 96, 167)')),  name= 'Adel.Cta.Cte', showlegend= False)

badlar=go.Scatter(
    x = tasasdeint.index,
    y = tasasdeint['Badlar'],
    mode = 'lines', line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 5,
        dash = 'dot'),  name= 'Badlar', showlegend= False)

call=go.Scatter(
    x = tasasdeint.index,
    y = tasasdeint['Call'],
    mode = 'lines', line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 5,
        dash = 'dash'),  name= 'Call', showlegend= False)

pf=go.Scatter(
    x = tasasdeint.index,
    y = tasasdeint['PF+60d'],
    mode = 'lines', line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 5,
        dash = 'dashdot'),  name= 'PF+60d', showlegend= False)

tasas= [adelanto, call, badlar,pf]

layouttasas = go.Layout(
    title = 'Tasas de Interés Activas',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'},
    legend=dict(orientation="h", traceorder='normal'))
tasasint = go.Figure(data=tasas,layout=layouttasas)

reservas=pd.read_csv(get_api_call(['174.1_RRVAS_IIOS_0_0_60'], format="csv", limit=5000), index_col='indice_tiempo', decimal=',')

reservas.rename(columns={'reservas_internacionales_bcra_prom_mensual_de_saldos_diarios':'Reservas BCRA'},inplace=True)

# create traces
reservas1 = [go.Bar(
    x = reservas.index,
    y = reservas['Reservas BCRA'])]

layout = go.Layout(
    title = 'Reservas BCRA, promedio mensual de saldos diarios',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'en millones de US$'},
    legend=dict(orientation="h", traceorder='normal'))

depoyprest= pd.read_csv(get_api_call([
'174.1_DSITOS_S_0_0_19',
'174.1_PTAMOS_S_0_0_19'], format="csv", start_date=2005, limit=5000), index_col='indice_tiempo')

depoyprest.rename(columns={'depositos_totales_pesos': 'Depósitos', 'prestamos_totales_pesos': 'Préstamos'}, inplace=True)
depoyprest=depoyprest/1000
data = [go. Scatter(
    x = depoyprest.index,
    y = compute_anual_variation(depoyprest[col]), name = col) for col in depoyprest.columns]


layout = go.Layout(
    title = 'Variación anual de los depósitos y préstamos ',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'})

emae=pd.read_csv(get_api_call(['143.3_NO_PR_2004_A_28','143.3_NO_PR_2004_A_31'], format="csv", start_date='2005',limit=5000), index_col='indice_tiempo')

pib= pd.read_csv(get_api_call(['9.2_PP2_2004_T_16'], format="csv", limit=5000), index_col='indice_tiempo')
pibxcapita=pd.read_csv(get_api_call(['9.1_IPC_2004_A_25'], format="csv", limit=5000), index_col='indice_tiempo')

#Valores trimestrales en millones de pesos a precios de 2004
pib.rename(columns={'pib_precios_2004':'PIB a precios de 2004'}, inplace=True)
componetespib= pd.read_csv(get_api_call([
'4.2_MGCP_2004_T_25',
'4.2_DGCP_2004_T_30',
'4.2_DGE_2004_T_26',
'4.2_DGIT_2004_T_25',
'4.2_OGI_2004_T_25'], format="csv", limit=5000), index_col='indice_tiempo')
componetespib.rename(columns={'manda_global_consumo_priv':'Consumo Privado', 'demanda_global_consumo_publico':'Consumo Público',
       'demanda_global_exportacion': 'Exportaciones FOB', 'demanda_global_ibif_total': 'Formación bruta de capital fijo',
       'oferta_global_importacion':'Importaciones FOB '}, inplace=True)
# create traces
data = [go.Bar(
    x = componetespib.index,
    y = componetespib[col], name = col) for col in componetespib.columns]

layout = go.Layout(
    title = 'Oferta y Demanda globales. Valores Trimestrales',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'},
    barmode='stack', barnorm='percent')
# create traces
data = [go.Bar(
    x = componetespib.index,
    y = vartrimestral(componetespib[col])*100, name = col) for col in componetespib.columns]

layout = go.Layout(
    title = 'Oferta y Demanda globales.Oferta y demanda globales. Variación porcentual respecto a igual período del año anterior.',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'}, barmode='stack')
gfigurativos=datos('379.9_GTOS_PRIMA017__37_33')
ingresos=datos('379.9_ING_ANTES_017__26_83')
traces = go.Scatter(
    x = gfigurativos.index,
    y = compute_anual_variation(gfigurativos['gtos_primario_antes_figurativos_2017']),
    mode = 'lines', line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 5), name = 'Gasto Primario')

traces2 = go.Scatter(
    x = ingresos.index,
    y = compute_anual_variation(ingresos['ing_antes_figurativos_2017']),
    mode = 'lines', line = dict(
        width = 5, dash='dot'), name = 'Ingresos')

gastoseingresos = [traces, traces2]
layout1 = go.Layout( title = '', xaxis = {'title': 'Período'}, yaxis = {'title': '% i.a'})

reca=datos('172.3_TL_RECAION_M_0_0_17')
#Inflacion anual
ipcanual=pd.read_csv(get_api_call(['103.1_I2N_2016_M_19',], format="csv", limit=5000), index_col='indice_tiempo')

recaipc=reca.join(ipcanual)
sup=datos('379.9_SUPERAVIT_017__23_94') #Superavit primarioMetodología 2017
financiero=datos('379.9_RESULTADO_017__18_38')#el déficit financiero -que incluye el pago de los intereses de la deuda pública- fue de $ 49.838 millones teniendo en relación a marzo de 2018 un aumento equivalente a 31,5%, y una reducción en términos reales de 15% i.a.
rdo=sup.join(financiero)
rdo.rename(columns={'superavit_primario_2017': 'Rdo. Primario', 'resultado_fin_2017': 'Rdo. Financiero'}, inplace=True)
datos=[go.Bar(
    x= rdo.index,
    y= rdo[col], name=col) for col in rdo.columns]
layout = go.Layout(
    title = 'Resultado Primario y Financiero',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'Millones de Pesos'})

# Create a Dash layout that contains a Graph component:
inflacion = html.Div([
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
    }),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='empleo/'),
    html.Br(),
    dcc.Link('Indice', href='/index_page')
    ])
Empleo=html.Div([
    dcc.Graph (id='desocupacion', figure={ 'data':[go.Scatter(
    x = desocupacion.index,
    y = desocupacion['eph_puntual_desocupacion_total']*100,
    mode = 'lines', line = dict(width = 5, color = '#1c79c0'), name= 'Tasa de desocupacion')],
    'layout': go.Layout(
    title = 'Tasa de Desocupación',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'}
    )}),
    dcc.Graph(id='asalariados', figure={'data':[go.Bar(
    x = asalariados.index,
    y = asalariados[col], name=col) for col in asalariados.columns],

    'layout': go.Layout(
    title = 'Trabajadores registrados según modalidad ocupacional principal. Total del país',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '% participación'},
    barmode= 'relative', barnorm='percent', legend=dict(orientation="h", traceorder='normal') )
    }),

    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Datos Inflación', href='/page-1'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5')
])

Dinero=html.Div([
    dcc.Graph(id="tcrm", figure= {'data': tipodecambio,
    'layout': go.Layout(
    title = 'Tipo de Cambio Real Multilateral',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'indice base100= Dic2015'},
    legend=dict(orientation="h", traceorder='normal'))
    }),

    dcc.Graph(id='tc', figure={'data': tc1,
                              'layout': go.Layout(
    title = 'Tipo de Cambio BCRA',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'pesos'},
    legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='reservas', figure={'data':reservas,
                                    'layout':go.Layout(
    title = 'Reservas BCRA, promedio mensual de saldos diarios',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'en millones de US$'},
    legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='tasaint', figure={'data':tasasint,
   'layout':layouttasas}),

    dcc.Graph(id='prestamosydepo', figure= {'data': [go.Bar(
    x = depoyprest.index,
    y = depoyprest[col], name = col) for col in depoyprest.columns],
    'layout':go.Layout(
    title = 'Depósitos y Préstamos en pesos',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'millones de pesos'},
    legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='prestdepo', figure={'data':[go. Scatter(
    x = depoyprest.index,
    y = compute_anual_variation(depoyprest[col]), name = col) for col in depoyprest.columns],
                                      'layout': go.Layout(
    title = 'Variación anual de los depósitos y préstamos ',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'},
    legend=dict(orientation="h", traceorder='normal'))}),


    html.Div(id='page-2-content'),
    dcc.Link('Datos Inflación', href='/page-1'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Actividad', href='/page-4'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5')
])

Actividad=html.Div([
    dcc.Graph(id='emae', figure={'data':[go.Scatter(
    x = emae.index,
    y = emae[col], name = col) for col in emae.columns],
    'layout': go.Layout(
    title = 'Estimador mensual de actividad económica',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'base 2004=100'}, legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='pib', figure={'data':[go.Scatter(
    x = pib.index,
    y = vartrimestral(pib[col]), name = col) for col in pib.columns],
                                'layout': go.Layout(
    title = 'PIB. Valores trimestrales. Var % respecto a igual período del año anterior.',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'})}),

    dcc.Graph(id='pbicomp', figure={'data':[go.Bar(
    x = componetespib.index,
    y = componetespib[col], name = col) for col in componetespib.columns],
                                'layout': go.Layout(
    title = 'Oferta y Demanda globales. Valores Trimestrales',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'},
    barmode='stack', barnorm='percent', legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='pbicomp', figure={'data':[go.Bar(
    x = componetespib.index,
    y = vartrimestral(componetespib[col])*100, name = col) for col in componetespib.columns],
                                    'layout': go.Layout(
    title = 'Oferta y demanda globales. Variación porcentual respecto a igual período del año anterior.',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'}, barmode='stack', legend=dict(orientation="h", traceorder='normal'))}),

    html.Div(id='page-2-content'),
    dcc.Link('Datos Inflación', href='/page-1'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5')
])

SectorPúblico=html.Div([
    dcc.Graph(id='reca', figure={'data': [go.Scatter(
    x = recaipc.index,
    y = compute_anual_variation(recaipc[col]), name = col) for col in recaipc.columns],
                                  'layout': go.Layout( title = 'Recursos Tributarios % i.a',
                                    xaxis = {'title': 'Período'}, yaxis = {'title': '% i.a'})}),

    dcc.Graph(id='supe', figure= {'data':gastoseingresos, 'layout':layout1}),

    dcc.Graph(id='id', figure={'data': [go.Bar(
    x= rdo.index,
    y= rdo[col], name=col) for col in rdo.columns],
                               'layout' : go.Layout( title = 'Resultado Primario y Financiero',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'Millones de Pesos'})}),

    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Actividad', href='/page-4')
])
