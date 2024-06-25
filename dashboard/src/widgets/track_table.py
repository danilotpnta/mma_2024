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
            {"field": "title", 'headerName': "Track Title"},
            {"field": "artist", 'headerName': "Artist"},
            {"field": "genre", 'headerName': "Genre"},
            {"field": "tempo", 'headerName': "Tempo (bpm)", 'valueFormatter': {"function":"d3.format(',.2f')(params.value)"}},
            {"field": "key", 'headerName': "Key"},
            {"field": "loudness", 'headerName': "Loudness (dB)"},
            {"field": "id", 'headerName': "sample_id", "suppressToolPanel": "True", "hide": "True"}
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