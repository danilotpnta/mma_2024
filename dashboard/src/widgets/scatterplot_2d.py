from dash import dcc
from Dataset import Dataset
import plotly.express 



def create_scatterplot_figure(projection):
    if projection == 't-SNE':
        x_col, y_col = 'x_tsne', 'y_tsne'
    elif projection == 'UMAP':
        x_col, y_col = 'x_umap', 'y_umap'
    else:
        raise Exception('Projection not found')
    
    fig = plotly.express.scatter(data_frame=Dataset.get(), x=x_col, y=y_col)

    return fig

def create_scatterplot(projection):
    return dcc.Graph(
            figure=create_scatterplot_figure(projection),
            id='scatterplot',
            className='stretchy-widget border-widget',
            responsive=True,
            config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['autoscale'],
                'displayModeBar': True,
            }
        )