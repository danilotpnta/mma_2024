from Dataset import Dataset
from dash import dcc
import plotly.express as px
import config

def create_scatterplot_figure(projection, sample_ids=[]):

    if projection == "tsne":
        x_col, y_col, z_col = "x_tsne", "y_tsne", "z_tsne"

    elif projection == "umap":
        x_col, y_col, z_col = "x_umap", "y_umap", "z_umap"

    else:
        raise Exception("Projection not found")
    
    data = Dataset.get()
    data['marker_size'] = 10

    hover_temp = '''
    <b>%{customdata[0]}</b>
    <br>
    <b>Artist:</b>%{customdata[2]}
    <br>
    <b>Genre:</b>%{customdata[3]}
    <br>
    <b>ID:</b>%{customdata[1]}'''
    
    if len(sample_ids) > 0:
        data.loc[~data['id'].isin(sample_ids), 'marker_size'] = 1
    fig = px.scatter_3d(data_frame=data, x=x_col, y=y_col, z=z_col,
                        color='genre', custom_data=['title', 'id', 'artist', 'genre', 'album_cover_path'], 
                        size='marker_size', opacity=0.6, size_max=12)
    
    fig.update_traces(hovertemplate=hover_temp)

    fig.update_traces(marker=dict(opacity=1, line=dict(width=0)))

    return fig

def create_scatterplot(projection):
    return dcc.Graph(
        figure=create_scatterplot_figure(projection),
        id="scatterplot-3D",
        className="stretchy-widget border-widget border",
        config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['autoscale'],
            'displayModeBar': True,
        }
    )