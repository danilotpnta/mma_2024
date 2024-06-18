from Dataset import Dataset
from dash import dcc
import plotly.express as px

def create_scatterplot_figure(projection):

    if projection == "t-SNE":
        x_col, y_col, z_col = "x_tsne", "y_tsne", "z_tsne"

    elif projection == "UMAP":
        x_col, y_col, z_col = "x_umap", "y_umap", "z_umap"

    else:
        raise Exception("Projection not found")
    
    fig = px.scatter_3d(data_frame=Dataset.get(), 
                        x=x_col, y=y_col, z=z_col,
                        color='genre',
                        custom_data=['id'])
    
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