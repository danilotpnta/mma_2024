from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from Dataset import Dataset
import config
from utils.similar_tracks import get_similar_tracks

from widgets import (
    projection_radio_buttons,
    scatterplot_3d,
    genre_histogram,
    tempo_histogram,
    track_table,
    gallery
)

import callbacks.scatterplot_3d
import callbacks.projection_radio_buttons


def run_dashboard():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    projection_radio_buttons_widget = (projection_radio_buttons.create_projection_radio_buttons())

    scatterplot_widget = scatterplot_3d.create_scatterplot(config.DEFAULT_PROJECTION)

    genre_dist = genre_histogram.create_histogram()
    tempo_dist = tempo_histogram.create_histogram()

    selected_track_label = html.Div(id='selected-track-title')
    track_table_widget = track_table.create_track_table()

    gallery_widget = gallery.create_gallery()

    right_tab = dcc.Tabs([
        dcc.Tab(label='genre distribution', children=genre_dist),
        dcc.Tab(label='tempo distribution', children=tempo_dist)
    ])

    app.layout = dbc.Container([
        projection_radio_buttons_widget,
        dbc.Row([
            dbc.Col(scatterplot_widget, width=6, className="main-col"),
            dbc.Col(right_tab, width=6, className="main-col")
        ]),
        dbc.Row([
            dbc.Col(track_table_widget),
            dbc.Col(gallery_widget)
        ])
        ], fluid=True, id="container")
    
    
    app.run(debug=True, use_reloader=True)


def main():
    if not Dataset.files_exist():
        print("File", config.DATASET_PATH, "missing")
        print("Creating dataset.")
        Dataset.download()

    Dataset.load()

    print("Starting Dash")
    run_dashboard()


if __name__ == "__main__":

    main()