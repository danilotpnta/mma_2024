from dash import dcc
from Dataset import Dataset
import plotly.express 
import config

def highlight_markers_on_scatterplot(scatterplot, sample_ids):
    # if sample_ids:
    #     colors = Dataset.get()['class_id'].map(lambda x: config.SCATTERPLOT_SELECTED_COLOR if x in class_ids else config.SCATTERPLOT_COLOR)
    # else:
    #     colors = config.SCATTERPLOT_COLOR
    pass
    # scatterplot['data'][0]['marker'] = {'color': colors}

def create_scatterplot_figure(projection):
    if projection == 't-SNE':
        x_col, y_col = 'x_tsne', 'y_tsne'
    elif projection == 'UMAP':
        x_col, y_col = 'x_umap', 'y_umap'
    else:
        raise Exception('Projection not found')
    
    data = Dataset.get()
    fig = plotly.express.scatter(data_frame=data, x=x_col, y=y_col, color='genre', custom_data='id')
    fig.update_traces(
        unselected_marker_opacity=0.60)

    fig.update_layout(dragmode='select')

    return fig

def create_scatterplot(projection):
    return dcc.Graph(
            figure=create_scatterplot_figure(projection),
            id='scatterplot-2D',
            className='stretchy-widget border-widget border',
            # responsive=True,
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
        data_selected = Dataset.get()

    return data_selected