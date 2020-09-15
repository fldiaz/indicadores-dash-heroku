import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
#para ver en localhost tengo que sacarle la linea del server, acá y en app.
from app import server
from layouts import inflacion, Dinero, Empleo, Actividad, SectorPúblico
import pandas as pd

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

##hacer el in
def header_colors():
    return {
        'bg_color': '#0C4142',
        'font_color': 'white',
    }

def layout():
    return html.Div(id='alignment-body', className='app-body', children=[
        html.Div([
            html.Div(id='alignment-control-tabs', className='control-tabs', children=[
                dcc.Tabs(
                    id='alignment-tabs', value='what-is',
                    children=[
                        dcc.Tab(
                            label='About',
                            value='what-is',
                            children=html.Div(className='control-tab', children=[
                                html.H4(
                                    className='what-is',
                                    children='What is Alignment Viewer?'
                                ),
                                html.P(
                                    """
                                    The Alignment Viewer (MSA) component is used to align
                                    multiple genomic or proteomic sequences from a FASTA or
                                    Clustal file. Among its extensive set of features,
                                    the multiple sequence alignment viewer can display
                                    multiple subplots showing gap and conservation info,
                                    alongside industry standard colorscale support and
                                    consensus sequence. No matter what size your alignment
                                    is, Alignment Viewer is able to display your genes or
                                    proteins snappily thanks to the underlying WebGL
                                    architecture powering the component. You can quickly
                                    scroll through your long sequence with a slider or a
                                    heatmap overview.
                                    """
                                ),
                                html.P(
                                    """
                                    Note that the AlignmentChart only returns a chart of
                                    the sequence, while AlignmentViewer has integrated
                                    controls for colorscale, heatmaps, and subplots allowing
                                    you to interactively control your sequences.
                                    """
                                ),
                                html.P(
                                    """
                                    Read more about the component here:
                                    https://github.com/plotly/react-alignment-viewer
                                    """
                                ),
                            ])
                        )}

index_page = html.Div([
    html.H1('Indicadores Económicos de Argentina', style={'color': '#0099e5'}),
    html.Div([
        html.P('Elaboración propia en base a última información publicada, a través de la API de Series de Tiempo, por organismos de la Administración Pública Nacional.')
    ]),
    html.Br(),
    dcc.Link('Precios', href='/page-1'),
    html.Br(),
    dcc.Link('Empleo e Ingresos', href='/page-2'),
    html.Br(),
    dcc.Link('Dinero y Bancos', href='/page-3'),
    html.Br(),
    dcc.Link('Actividad', href='/page-4'),
    html.Br(),
    dcc.Link('Sector Público', href='/page-5'),
    html.Br(),
    html.P('Última actualización: '), pd.to_datetime('today'),
    html.P('Consultas: fldiaz@crossvalidated.com.ar', style={'color': '#0099e5'})])


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
