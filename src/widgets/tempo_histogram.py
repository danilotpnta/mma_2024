import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from src.Dataset import Dataset


def create_histogram(nbins=20):
    histogram = draw_histogram(nbins)
    return html.Div([
        dcc.Graph(figure=histogram,
                  responsive=True,
                  config={
                      'displaylogo': False,
                      'displayModeBar': False
                  },
                  id='tempo_histogram',
                  clear_on_unhover=True),
        dcc.Tooltip(id="tempo_histogram-tooltip",
                    loading_text="LOADING"),
    ], className='border-widget stretchy-widget histogram-container')


def draw_histogram(nbins):
    df = Dataset.get()

    # Plotting with Plotly Express
    fig = px.histogram(df, x='tempo', nbins=nbins)

    fig.update_layout(
        xaxis=dict(
            tickangle=340, 
            automargin=False, 
            fixedrange=True
        ),
        yaxis=dict(
            visible=True, 
            automargin=False, 
            fixedrange=True,
            title=dict(text="frequency", standoff=10),
            tickfont=dict(size=12)
        ),
        xaxis_title_text='tempo (bpm)', # xaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        margin=dict(l=60, r=60, t=10, b=40)
    )
    
    return fig