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


def draw_histogram(selected_category, nbins, sample_ids=[]):
    if selected_category == 'tempo':
        xaxis_title_text='tempo (bpm)'
        bin_size = 10
    elif selected_category == 'loudness':
        xaxis_title_text='loudness (dB)'
        bin_size = 2

    df = Dataset.get()
    
    if len(sample_ids):
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df[selected_category], nbinsx=nbins, name='Total'))
        fig.add_trace(go.Histogram(x=df[df['id'].isin(sample_ids)][selected_category], nbinsx=nbins, name='Selection'))
        fig.update_layout(barmode='overlay')
        fig.update_layout(legend=dict(
            yanchor="top",
            xanchor="right",
            x=0.99
        ))
    else:
        fig = px.histogram(df, x=selected_category, nbins=nbins)
    
    fig.update_traces(hovertemplate='Count: %{y}<extra></extra>',
        xbins=dict( # bins used for histogram
        start=df[selected_category].min(),
        end=df[selected_category].max(),
        size=bin_size
    ))
    fig.update_traces()
    fig.update_layout(
        hovermode="x unified",
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