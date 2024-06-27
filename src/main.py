# To handle importing from `src`
import os
import sys

dirpath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dirpath)

# The rest of the code
from dash import Dash, dcc, callback, Input, Output
from src import config
from src.Dataset import Dataset

import dash_bootstrap_components as dbc


from src.widgets import (
    genre_histogram,
    scatterplot_3d,
    projection_radio_buttons,
    tempo_histogram,
    gallery,
    track_player,
)

import src.callbacks.projection_radio_buttons
import src.callbacks.track_player
import src.callbacks.scatterplot_3d


def run_dashboard():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(
        __name__, external_stylesheets=external_stylesheets, assets_folder="assets"
    )

    projection_radio_buttons_widget = (
        projection_radio_buttons.create_projection_radio_buttons()
    )

    scatterplot_widget = scatterplot_3d.create_scatterplot(config.DEFAULT_PROJECTION)

    genre_dist = genre_histogram.create_histogram()
    tempo_dist = tempo_histogram.create_histogram()

    track_player_widget = track_player.create_track_player()

    # gallery_widget = gallery.create_gallery()

    right_tab = dcc.Tabs(
        [
            dcc.Tab(label="genre distribution", children=genre_dist),
            dcc.Tab(label="tempo distribution", children=tempo_dist),
        ]
    )

    app.layout = dbc.Container(
        [
            projection_radio_buttons_widget,
            dbc.Row(
                [
                    dbc.Col(scatterplot_widget, width=6, className="main-col"),
                    dbc.Col(right_tab, width=6, className="main-col"),
                ],
                className="top-row",
                justify="between",
            ),
            dbc.Row(dbc.Col([track_player_widget])),
        ],
        fluid=True,
        id="container",
    )

    app.run(debug=True, use_reloader=True)


def main():
    if not Dataset.files_exist():
        print("File", config.SAMPLE_DATASET_PATH, "missing")
        print("Creating dataset.")
        Dataset.download()

    Dataset.load()

    print("Starting Dash")
    run_dashboard()


if __name__ == "__main__":
    main()
