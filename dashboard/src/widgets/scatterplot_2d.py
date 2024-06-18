from dash import dcc
from Dataset import Dataset
import plotly.express 
import config

def highlight_class_on_scatterplot(scatterplot, class_ids):
    if class_ids:
        colors = Dataset.get()['class_id'].map(lambda x: config.SCATTERPLOT_SELECTED_COLOR if x in class_ids else config.SCATTERPLOT_COLOR)
    else:
        colors = config.SCATTERPLOT_COLOR
    scatterplot['data'][0]['marker'] = {'color': colors}

def create_scatterplot_figure(projection):
    if projection == 't-SNE':
        x_col, y_col = 'x_tsne', 'y_tsne'
    elif projection == 'UMAP':
        x_col, y_col = 'x_umap', 'y_umap'
    else:
        raise Exception('Projection not found')
    
    fig = plotly.express.scatter(data_frame=Dataset.get(), x=x_col, y=y_col, color='genre')
    fig.update_traces(
        customdata=Dataset.get().index, 
        marker={'color': config.SCATTERPLOT_COLOR},
        unselected_marker_opacity=0.60)

    fig.update_layout(dragmode='select')

    return fig

def create_scatterplot(projection):
    return dcc.Graph(
            figure=create_scatterplot_figure(projection),
            id='scatterplot-2D',
            className='stretchy-widget border-widget border',
            responsive=True,
            config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['autoscale'],
                'displayModeBar': True,
            }
        )

def get_data_selected_on_scatterplot(scatterplot_fig):
    scatterplot_fig_data = scatterplot_fig['data'][0]
    if 'selectedpoints' in scatterplot_fig_data:
        selected_image_ids = list(map(scatterplot_fig_data['customdata'].__getitem__, scatterplot_fig_data['selectedpoints']))
        data_selected = Dataset.get().loc[selected_image_ids]
    else:
        data_selected = Dataset.get()

    return data_selected