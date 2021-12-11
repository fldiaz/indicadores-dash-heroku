import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
#para ver en localhost tengo que sacarle la linea del server, acá y en app.
from app import server
from layouts import inflacion, Dinero, Empleo, Actividad, SectorPúblico
import pandas as pd

colors = {
'background': '#FFFFFF',
'text': '#FFFFFF'
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')],
    style={'backgroundColor': colors['background']})

# App layout

index_page = html.Div(
    id='root',
    children=[
        html.Div(id='header',
        children=[
            #html.Img(src= app.get_asset_url('Logo.Cross.Validated.PNG')),
            html.H4(children='Indicadores Económicos de Argentina', style={'color': '#FFFFFF'}),
            html.P(
                 """
                 Elaboración propia en base a última información publicada, \
                 a través de la API de Series de Tiempo,
                 por organismos de la Administración Pública Nacional.
                   """, style={'color': '#FFFFFF'})]),
        html.Div(id='index',
        children=[
            dcc.Link('Precios', href='/page-1'),
            html.Br(),
            dcc.Link('Empleo e Ingresos', href='/page-2'),
            html.Br(),
            dcc.Link('Dinero y Bancos', href='/page-3'),
            html.Br(),
            dcc.Link('Actividad', href='/page-4'),
            html.Br(),
            dcc.Link('Sector Público', href='/page-5'),
            html.Br()]),

        html.Div(id='foot',
        children=[
            #html.P('Última actualización: ', style={'color': '#FFFFFF'}), pd.to_datetime('today'),
            html.P('Consultas: fldiaz@crossvalidated.com.ar', style={'color': '#FFFFFF'}),
            ]),
        html.P(),
            ])




@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

##hacer el indice como corresponde
def display_page(pathname):
    if pathname == '/page-1':
        return inflacion
    elif pathname == '/page-2':
        return Empleo
    elif pathname == '/page-3':
        return Dinero
    elif pathname=='/page-4':
        return Actividad
    elif pathname=='/page-5':
        return SectorPúblico
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)
