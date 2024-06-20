import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from Dataset import Dataset


def create_histogram(selected_category, nbins):
    histogram = draw_histogram(selected_category, nbins)
    return html.Div([
        dcc.Graph(figure=histogram,
                  config={
                      'displaylogo': False,
                      'displayModeBar': False
                  },
                  id=f'{selected_category}_histogram',
                  clear_on_unhover=True),
        dcc.Tooltip(id=f"{selected_category}_histogram-tooltip",
                    loading_text="LOADING"),
    ], className='border-widget stretchy-widget histogram-container')


def draw_histogram(selected_category, nbins):
    if selected_category == 'tempo':
        xaxis_title_text='tempo (bpm)'
    elif selected_category == 'loudness':
        xaxis_title_text='loudness (dB)'

    df = Dataset.get()
    
    # Plotting with Plotly Express
    fig = px.histogram(df, x=selected_category, nbins=nbins)

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
        xaxis_title_text=xaxis_title_text, # xaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        margin=dict(l=60, r=60, t=10, b=40)
    )
    
    return fig