import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from Dataset import Dataset
import pandas as pd

def create_histogram(selected_category='genre'):
    histogram = draw_histogram(selected_category)
    return html.Div([
        dcc.Graph(figure=histogram,
                #   responsive=True,
                  config={
                      'displaylogo': False,
                      'displayModeBar': False
                  },
                  id=f'{selected_category}_histogram',
                  clear_on_unhover=True),
        dcc.Tooltip(id=f"{selected_category}_histogram-tooltip",
                    loading_text="LOADING"),
    ], className='border-widget stretchy-widget histogram-container')


def count_occurences(dataframe, selected_category):
    class_counts = dataframe[selected_category].value_counts()
    class_counts = class_counts.reindex(dataframe[selected_category].unique(), fill_value=0)
    class_counts = class_counts.to_frame()
    class_counts[selected_category] = class_counts.index
    return class_counts 

def draw_histogram(selected_category, sample_ids=[]):
    dataframe = Dataset.get()
    class_counts = count_occurences(dataframe, selected_category)
    if len(sample_ids):
        stacked_bar_counts = count_occurences(dataframe[dataframe['id'].isin(sample_ids)], selected_category)['count']
        class_counts['condition'] = stacked_bar_counts
        class_counts = class_counts.fillna(0.1)
        print(class_counts)
        # fig = px.histogram(class_counts, x=selected_category, y='count', color='condition')
        fig = go.Figure()
        fig.add_trace(go.Bar(x=class_counts[selected_category], y=class_counts['count'], name='Total'))
        fig.add_trace(go.Bar(x=class_counts[selected_category], y=class_counts['condition'], name='Selection'))
        fig.update_layout(barmode='overlay')
        fig.update_layout(legend=dict(
            yanchor="top",
            xanchor="right",
            x=0.99
        ))
    else:
        fig = px.histogram(class_counts, x=selected_category, y='count')

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
            title=dict(text="count", standoff=10),
            tickfont=dict(size=12)
        ),
        bargap=0.2, # gap between bars of adjacent location coordinates
        margin=dict(l=60, r=60, t=10, b=40)
    )
    
    return fig