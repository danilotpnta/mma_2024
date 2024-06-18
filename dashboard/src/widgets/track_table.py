import dash_ag_grid
from dash import dcc, html

from Dataset import Dataset

def create_table():
    return html.Div([
        create_table_grid()
    ],
        className='stretchy-widget',
        id='table'
    )

def create_table_grid():
    return dash_ag_grid.AgGrid(
        columnDefs=[
            {"field": "track_title", 'headerName': "Track Title"},
            {"field": "artist", 'headerName': "Artist"},
            {"field": "genre", 'headerName': "Genre"}
        ],
        rowData=[],
        columnSize="responsiveSizeToFit",
        dashGridOptions={
            "pagination": False,
            "paginationAutoPageSize": True,
            "suppressCellFocus": True,
            "rowSelection": "multiple",
        },
        defaultColDef={"filter": "agTextColumnFilter"},
        className='stretchy-widget ag-theme-alpine',
        # style={'width': '', 'height': ''},
        id='grid'
    )