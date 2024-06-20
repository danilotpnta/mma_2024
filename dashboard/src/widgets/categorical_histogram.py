import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from Dataset import Dataset


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


def draw_histogram(selected_category):
    category_column = Dataset.get()[selected_category]

    # Grouping and counting occurrences
    class_counts = category_column.value_counts().reset_index()
    class_counts.columns = [selected_category, 'count']

    # Plotting with Plotly Express
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