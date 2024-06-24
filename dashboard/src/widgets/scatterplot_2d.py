from dash import dcc
from Dataset import Dataset
import plotly.express 
import config
import pandas as pd

def highlight_markers_on_scatterplot(sample_ids, radio_button_value):
    if sample_ids:
        condition = list(Dataset.get()['id'].map(lambda x: 4 if x in sample_ids else 1))
    else:
        condition = []
    return create_scatterplot_figure(radio_button_value, condition)

def create_scatterplot_figure(projection, condition=[]):
    if projection == 'tsne':
        x_col, y_col = 'x_tsne', 'y_tsne'
    elif projection == 'umap':
        x_col, y_col = 'x_umap', 'y_umap'
    else:
        raise Exception('Projection not found')
    
    data = Dataset.get()
    
    if len(condition) > 0:
        data['condition'] = condition
        fig = plotly.express.scatter(data_frame=data, x=x_col, y=y_col, color='genre', custom_data=['id'], size='condition', labels={"genre": "Genre"})
    else:
        fig = plotly.express.scatter(data_frame=data, x=x_col, y=y_col, color='genre', custom_data=['id'])
        fig.update_traces(marker=dict(size=14))
    
    fig.update_layout(dragmode='select')
    fig.update_layout(legend=dict(itemsizing='constant'))
    fig.update_traces(
        unselected_marker_opacity=0.60)


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