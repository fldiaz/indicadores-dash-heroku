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

def diferenciamensual(df):
    dato=(df-df.shift(1))
    return dato

def diferenciaanual(df):
    dato=(df-df.shift(12))
    return dato

def datos(df):
    datos=pd.read_csv(get_api_call([df], format="csv", limit=5000), index_col='indice_tiempo')
    return datos



#Actividad
emae=pd.read_csv('datos/emae.csv', index_col='indice_tiempo')
emaeanual= compute_anual_variation(emae)*100
emaeanual.rename(columns={'emae_desestacionalizada': 'EMAE var. anual'}, inplace=True)
x = compute_mensual_variation(emae)*100
x.rename(columns={'emae_desestacionalizada': 'EMAE var. mensual'}, inplace=True)
emae=x.join(emaeanual)

pib= pd.read_csv('datos/pib.csv', index_col='indice_tiempo')
pibxcapita=pd.read_csv('datos/pibxcapita.csv', index_col='indice_tiempo')
pib.rename(columns={'pib_precios_2004':'PIB a precios de 2004'}, inplace=True)
componetespib= pd.read_csv('datos/componetespib.csv', index_col='indice_tiempo')
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

gfigurativos=pd.read_csv('datos/gfigurativos.csv', index_col='indice_tiempo')
ingresos=pd.read_csv('datos/ingresos.csv', index_col='indice_tiempo')
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
        width = 5, dash='dot'), name = 'Recursos Tributarios netos de copa')

gastoseingresos = [traces, traces2]
layout1 = go. Layout( title = '', xaxis = {'title': 'Período'}, yaxis = {'title': '% i.a'})

reca=pd.read_csv('datos/reca.csv', index_col='indice_tiempo')
#Inflacion anual
ipcanual=pd.read_csv('datos/ipcanual.csv', index_col='indice_tiempo')

recaipc=reca.join(ipcanual)
sup=pd.read_csv('datos/sup.csv', index_col='indice_tiempo')#Superavit primarioMetodología 2017
financiero=pd.read_csv('datos/financiero.csv', index_col='indice_tiempo')#el déficit financiero -que incluye el pago de los intereses de la deuda pública- fue de $ 49.838 millones teniendo en relación a marzo de 2018 un aumento equivalente a 31,5%, y una reducción en términos reales de 15% i.a.
rdo=sup.join(financiero)
rdo.rename(columns={'superavit_primario_2017': 'Rdo. Primario', 'resultado_fin_2017': 'Rdo. Financiero'}, inplace=True)
datos=[go.Bar(
    x= rdo.index,
    y= rdo[col], name=col) for col in rdo.columns]
layout = go.Layout(
    title = 'Resultado Primario y Financiero',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'Millones de Pesos'})
###########################################################################
# Create a Dash layout that contains a Graph component:
ipc=pd.read_csv('datos/ipc.csv', index_col='indice_tiempo')
ipc=ipc*100
ipc.rename(columns={'estacionales': 'Estacionales',
  'ipc_nucleo': 'Núcleo',
  'ipc_regulados': 'Regulados',
  'ipc_ng_nacional_tasa_variacion_mensual': 'Nivel General'}, inplace=True)

ipcxcomponente= pd.read_csv('datos/ipcxcomponente.csv', index_col='indice_tiempo')
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

infxzona=pd.read_csv('datos/ipcxzona.csv', index_col='indice_tiempo')
infxzona=infxzona*100
infxzona.rename (columns={'ipc_ng_nacional_tasa_variacion_mensual': 'Nacional',
       'ipc_ng_cuyo_tasa_variacion_mensual': 'Cuyo',
       'ipc_ng_nea_tasa_variacion_mensual': 'Noreste',
       'ipc_ng_noa_tasa_variacion_mensual': 'Noroeste',
       'ipc_ng_pampeana_tasa_variacion_mensual': 'Pampeana',
       'ipc_ng_patagonia_tasa_variacion_mensual': 'Patagónica'}, inplace=True)

inflacion = html.Div([
    dcc.Graph( id='ipc', figure={'data': [go.Scatter(
                    x = ipc.index,
                    y = ipc[col],
                    mode = 'lines', name=col ) for col in ipc.columns],
                'layout': go.Layout(
                title = 'Índice de precios al consumidor. Variaciones mensuales, según categorías. Total nacional',
                xaxis = {'title': 'Período'},
                yaxis = {'title': 'Var.mensual %'},
                hovermode='closest')}),
    dcc.Graph(id='ipcxcomponente', figure={'data': [go.Scatter(
    x = ipcxcomponente.index,
    y = compute_anual_variation(ipcxcomponente[col])*100,  mode = 'markers+lines', name=col) for col in ipcxcomponente.columns],
                'layout': go.Layout(
                title = 'Var. Índice de precios al consumidor. Según divisiones. Total nacional',
                xaxis = {'title': 'Período'},
                yaxis = {'title': 'Var. últimos 12 meses'},
                hovermode='closest', legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='ipcxzonas', figure={'data': [go.Scatter(
    x=infxzona.index, y = infxzona[col], name=col, mode='markers') for col in infxzona.columns],
                'layout': go.Layout(
                title = 'Índice de precios al consumidor. Var. mensual. Total nacional y regiones',
                xaxis = {'title': 'Período'},
                yaxis = {'title': 'Var.mensual %'},
                hovermode='closest')
    }),

    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Actividad', href='/page-4'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5'),
    html.Br(),
    dcc.Link('Indice', href='/index_page')
    ])

#Indicadores de desempleo 42.3_EPH_PUNTUATAL_0_M_30 trimestral
desocupacion= pd.read_csv('datos/desocupacion.csv', index_col='indice_tiempo')
asalariados=pd.read_csv('datos/asalariados.csv', index_col='indice_tiempo')
asalariados.rename(columns={'asalariados_pub_sin_estac':'Asalariados del sector público', 'asalariados_priv_sin_estac':'Asalariados del sector privado',
       'asalariados_casas_particulares_sin_estac': 'Asalariados de casas particulares',
       'independientes_autonomos_sin_estac': 'Independientes autónomos',
       'independientes_monotributo_sin_estac': 'Independientes con monotributo',
       'independientes_monotributo_social_sin_estac': 'Independientes con monotributo social'}, inplace=True)
salarios=pd.read_csv('datos/salarios.csv', index_col='indice_tiempo')

salarios.rename(columns={'indice_salarios_registrado_sector_privado':'Sector Privado Registrado', 'indice_salarios_no_registrado_sector_privado':'Sector Privado no Registrado',
       'indice_salarios_registrado_sector_publico':'Sector Público', 'ipc_2016_nivel_general': 'Nivel General de Precios'}, inplace=True)
cantdeasalariados=pd.read_csv('datos/cantdeasalariados.csv', index_col='indice_tiempo')
privado = go.Scatter(
    x = salarios.index,
    y = compute_anual_variation(salarios['Sector Privado Registrado']), mode='lines',
        line = dict(width = 5, color = ('rgb(22, 96, 167)'), dash ='dashdot'),  name= 'Sector Privado Registrado', showlegend= True)

noregis=go.Scatter(
    x = salarios.index,
    y = compute_anual_variation(salarios['Sector Privado no Registrado']),
    mode = 'lines', line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,
        dash = 'dot'),  name= 'Sector Privado no Registrado', showlegend= True)

publico=go.Scatter(
    x = salarios.index,
    y = compute_anual_variation(salarios['Sector Público']),
    mode = 'lines', line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,
        dash = 'dash'),  name= 'Sector Público', showlegend= True)

ipc=go.Scatter(
    x = salarios.index,
    y = compute_anual_variation(salarios['Nivel General de Precios']),
    mode = 'lines', line = dict(
        color = ('#ff0000'),
        width = 5),  name= 'Nivel General de Precios', showlegend= True)
salario= [privado, noregis, publico, ipc]

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
        barmode= 'relative', barnorm='percent', legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='cantdeasalariados', figure={'data':[go.Bar(
    x = cantdeasalariados.index,
    y = diferenciaanual(cantdeasalariados[col])*1000, name=col) for col in cantdeasalariados.columns],
    'layout': go.Layout(
    title = 'Asalariados registrados sector privado CABA-PBA. Variación Anual',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'Personas'},
    legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='salarios', figure={'data': salario,
    'layout':go.Layout(
    title = 'Indice de Salario y Precios',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '% i.a'}, legend=dict(orientation="h", traceorder='normal'))}),

    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Inflación', href='/page-1'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Actividad', href='/page-4'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5'),
    html.Br(),
    dcc.Link('Indice', href='/index_page')
])
#Dinero y Bancos
tc=pd.read_csv('datos/tc.csv', index_col='indice_tiempo')
# create traces
tc1= [go.Scatter(
    x = tc.index,
    y = tc['tipo_cambio_valuacion'], mode = 'lines', name='USD', line = dict(width = 5, color = '#1c79c0' ))]
layout = go.Layout(
    title = 'Tipo de Cambio BCRA',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'pesos'},
    legend=dict(orientation="h", traceorder='normal'))
tcrm=pd.read_csv('datos/tcrm.csv', index_col='indice_tiempo')
tcrusa=pd.read_csv('datos/tcrusa.csv', index_col='indice_tiempo')
tcrbra=pd.read_csv('datos/tcrbra.csv', index_col='indice_tiempo')
tcreuro=pd.read_csv('datos/tcreuro.csv', index_col='indice_tiempo')
tcrm1= go.Scatter(
    x = tcrm.index,
    y = tcrm['tipo_cambio_real_multilateral_actual'], mode = 'lines', name='Tipo de Cambio Real Multilateral',
    line = dict(width = 5, color = '#c01c94'))
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

tasasdeint=pd.read_csv('datos/tasasdeint.csv', index_col='indice_tiempo')
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
depoyprest=pd.read_csv('datos/depoyprest.csv', index_col='indice_tiempo')
depoyprest.rename(columns={'depositos_totales_pesos_privado': 'Depósitos del Sector Privado', 'prestamos_al_sector_privado_pesos': 'Préstamos al Sector Privado'}, inplace=True)
depoyprest=depoyprest/1000
reservas=pd.read_csv('datos/reservas.csv', index_col='indice_tiempo')
reservas.rename(columns={'reservas_internacionales_bcra_saldos':'Reservas BCRA'},inplace=True)

depo_presta_pib=pd.read_csv('datos/depo_presta_pib.csv', index_col='indice_tiempo')

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

    dcc.Graph(id='reservas', figure={'data':[go.Bar(
    x = reservas.index,
    y = reservas['reservas_internacionales_dolares'])],
        'layout': go.Layout(
        title = 'Reservas BCRA, promedio de saldos diarios',
        xaxis = {'title': 'Período'},
        yaxis = {'title': 'en millones de US$'}, legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='tasaint', figure={'data':tasasint,
   'layout':layouttasas}),

    dcc.Graph(id='prestamosydepo', figure= {'data': [go.Bar(
    x = depoyprest.index,
    y = depoyprest[col], name = col) for col in depoyprest.columns],
    'layout':go.Layout(
    title = 'Depósitos y Préstamos del Sector Privado en pesos',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'millones de pesos'},
    legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='prestdepo', figure={'data':[go. Scatter(
    x = depoyprest.index,
    y = compute_anual_variation(depoyprest[col])*100, name = col) for col in depoyprest.columns],
    'layout': go.Layout(
    title = 'Variación i.a. de los depósitos y préstamos ',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'},
    legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='prestdepo/pib', figure={'data':[go. Bar(
    x = depo_presta_pib.index,
    y = depo_presta_pib[col], name = col) for col in depo_presta_pib.columns],
    'layout': go.Layout(
    title = 'Depósitos y Prestamos al SP respecto del PIB',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'},
    legend=dict(orientation="h", traceorder='normal'))}),


    html.Div(id='page-3-content'),
    dcc.Link('Inflación', href='/page-1'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Actividad', href='/page-4'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5'),
    html.Br(),
    dcc.Link('Indice', href='/index_page')
])

Actividad=html.Div([dcc.Graph(id='emae', figure={'data':[go.Bar(
    x = emae.index,
    y = emae[col], name = col) for col in emae.columns],
    'layout': go.Layout(
    title = 'EMAE. Variación anual y mensual',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'}, legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='pib', figure={'data':[go.Scatter(
    x = pib.index,
    y = vartrimestral(pib[col])*100, name = col) for col in pib.columns],
    'layout': go.Layout(
    title = 'PIB. Valores trimestrales. Var % respecto a igual período del año anterior.',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'})}),

    dcc.Graph(id='pbicomp', figure={'data':[go.Bar(
    x = componetespib.index,
    y = componetespib[col], name = col) for col in componetespib.columns],
    'layout': go.Layout(
    title = 'Participación de la Oferta y Demanda globales. Valores Trimestrales',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'},
    barmode='stack', barnorm='percent', legend=dict(orientation="h", traceorder='normal'))}),

    dcc.Graph(id='pbicomp2', figure={'data':[go.Bar(
    x = componetespib.index,
    y = vartrimestral(componetespib[col])*100, name = col) for col in componetespib.columns],
    'layout': go.Layout(
    title = 'Oferta y demanda globales. Var. % respecto a igual período del año anterior.',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'}, barmode='stack', legend=dict(orientation="h", traceorder='normal'))}),

    html.Div(id='page-4-content'),
    dcc.Link('Inflación', href='/page-1'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5'),
    html.Br(),
    dcc.Link('Indice', href='/index_page')
])

SectorPúblico=html.Div([
    dcc.Graph(id='reca', figure={'data': [go.Scatter(
    x = recaipc.index,
    y = compute_anual_variation(recaipc[col]), name = col) for col in recaipc.columns],
    'layout': go.Layout( title = 'Variación i.a. de los Recursos Tributarios',
    xaxis = {'title': 'Período'},
    yaxis = {'title': '%'})}),

    dcc.Graph(id='supe', figure= {'data':gastoseingresos, 'layout':layout1}),

    dcc.Graph(id='id', figure={'data': [go.Bar(
    x= rdo.index,
    y= rdo[col], name=col) for col in rdo.columns],
    'layout' : go.Layout( title = 'Resultado Primario y Financiero',
    xaxis = {'title': 'Período'},
    yaxis = {'title': 'Millones de Pesos'})}),

    html.Div(id='page-5-content'),
    html.Br(),
    dcc.Link('Inflación', href='/page-1'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Actividad', href='/page-4'),
    html.Br(),
    dcc.Link('Indice', href='/index_page')
])
