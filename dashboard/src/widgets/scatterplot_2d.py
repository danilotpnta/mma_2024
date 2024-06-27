from dash import dcc
from Dataset import Dataset
import plotly.express 
import config
import pandas as pd
import plotly.graph_objects as go


def create_scatterplot_figure(projection, sample_ids=[]):
    if projection == 'tsne':
        x_col, y_col = 'x_tsne', 'y_tsne'
    elif projection == 'umap':
        x_col, y_col = 'x_umap', 'y_umap'
    else:
        raise Exception('Projection not found')
    
    data = Dataset.get()

    data['marker_size'] = 10

    if len(sample_ids) > 0:
        data.loc[~data['id'].isin(sample_ids), 'marker_size'] = 1

    hover_temp = """
    <b>%{customdata[0]}</b>
    <br>
    <b>Artist:</b>%{customdata[2]}
    <br>
    <b>Genre:</b>%{customdata[3]}
    <br>
    <b>ID:</b>%{customdata[1]}"""

    fig = plotly.express.scatter(data_frame=data, x=x_col, y=y_col,
                                 color='genre', custom_data=['title', 'id', 'artist', 'genre', 'album_cover_path'],
                                 size='marker_size', size_max=8, color_discrete_map=config.GENRE_COLORS)
    
    fig.update_traces(hovertemplate=hover_temp)
    
    fig.update_layout(dragmode='select')
    fig.update_layout(legend=dict(itemsizing='constant'))
    fig.update_traces(marker=dict(opacity=1, line=dict(width=0)))

    return fig

def create_scatterplot(projection):
    return dcc.Graph(
            figure=create_scatterplot_figure(projection),
            id='scatterplot-2D',
            className='stretchy-widget border-widget border',
            config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['autoscale'],
                'displayModeBar': True,
            }
        )

def get_data_selected_on_scatterplot(selected_data):
    all_data = Dataset.get()
    if selected_data:
        selected_point_ids = [i['customdata'][0] for i in selected_data['points']]
        data_selected = all_data.loc[all_data['id'].isin(selected_point_ids)]
    else:
        data_selected = pd.DataFrame(columns=all_data.columns)

    return data_selected