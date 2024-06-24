import dash_bootstrap_components as dbc
from dash import html
from typing import List, Tuple


feature_colors = {
    'genre': 'primary',
    'tempo': 'success',
    'key': 'warning',
    'loudness': 'danger'
}


def create_filter_view(filters: List[Tuple[str, str]]=[]):
    buttons = [dbc.Button(
        
        f"{feature}:{value}", color=feature_colors[feature],
        className='filter-button') for feature, value in filters
        ]
    
    filter_view = html.Div(children=buttons, className='filter-view')
    return filter_view