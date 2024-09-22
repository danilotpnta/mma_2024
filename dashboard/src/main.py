import os
import config
import argparse
import callbacks.navbar
import callbacks.histograms
import callbacks.track_table
import callbacks.scatterplots
import callbacks.trackinfo_bars
import callbacks.projection_radio_buttons
import dash_bootstrap_components as dbc

from Dataset import Dataset
from Collection import Collection
from utils.similar_tracks import get_similar_tracks
from dash import Dash, dcc, html, Output, Input, callback
from widgets import (
    projection_radio_buttons,
    scatterplot_3d,
    scatterplot_2d,
    track_info,
    track_table,
    categorical_histogram,
    numerical_histogram,
    gallery,
    filter_view,
    navbar,
)


def run_dashboard():

    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    projection_radio_buttons_widget = (
        projection_radio_buttons.create_projection_radio_buttons()
    )

    scatterplot_3d_widget = scatterplot_3d.create_scatterplot(config.DEFAULT_PROJECTION)
    scatterplot_2d_widget = scatterplot_2d.create_scatterplot(config.DEFAULT_PROJECTION)

    genre_dist = categorical_histogram.create_histogram("genre")
    tempo_dist = numerical_histogram.create_histogram("tempo", nbins=30)
    key_dist = categorical_histogram.create_histogram("key")
    loudness_dist = numerical_histogram.create_histogram("loudness", nbins=20)

    track_info_widget = track_info.create_track_info()
    track_table_widget = track_table.create_table()
    filter_view_widget = filter_view.create_filter_view()

    # deselect_button = button.create_deselect_button()
    # test_widget = html.H1("Test", id='image-click-output')
    navbar_widget = navbar.create_navbar(
        projection_radio_buttons_widget,
    )
    gallery_widget = gallery.create_gallery()

    audio_widget = html.Audio(
        id="audio-player", src="your-audio-file.mp3", controls=True
    )

    view_3d = dbc.Stack([scatterplot_3d_widget, html.Hr(), track_info_widget], gap=3)

    view_2d = dbc.Stack([scatterplot_2d_widget, html.Hr(), track_table_widget], gap=3)

    left_tab = dcc.Tabs(
        [
            dcc.Tab(label="3-D plot view", children=view_3d),
            dcc.Tab(label="2-D plot view", children=view_2d),
        ]
    )

    right_tab = dcc.Tabs(
        [
            dcc.Tab(label="genre distribution", children=genre_dist),
            dcc.Tab(label="tempo distribution", children=tempo_dist),
            dcc.Tab(label="key distribution", children=key_dist),
            dcc.Tab(label="loudness distribution", children=loudness_dist),
        ]
    )

    gallery_comp = dbc.Card(
        [
            dbc.CardHeader("No tracks selected yet!", id="gallery-card-header"),
            dbc.CardBody([gallery_widget]),
        ]
    )

    right_component_wrapper = dbc.Stack(
        [
            # deselect_button,
            right_tab,
            filter_view_widget,
            html.Hr(),
            gallery_comp,
            dcc.Store(id="invisible-store"),
            dcc.Store(id="song-data"),
            dcc.Store(id="prev-scatter-click", data=[[None], [None]]),
        ]
    )

    app.layout = dbc.Container(
        [
            navbar_widget,
            dbc.Row(
                [
                    dbc.Col(left_tab, className="shadow-sm p-3 mb-5 bg-white rounded"),
                    dbc.Col(
                        right_component_wrapper,
                        className="shadow-sm p-3 mb-5 bg-white rounded",
                    ),
                ],
                className="top-row",
            ),
        ],
        fluid=True,
        id="container",
    )

    app.run(debug=False, use_reloader=True, port=7864)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        default="gtzan",
        help="The folder containing the .wav files (in '/dashboard/data/[your_dataset_name]').",
    )

    parsed_args = parser.parse_args()

    # Getting the dataset directories
    data_folder = os.path.join(config.DATA_DIR, parsed_args.dataset)
    metadata_csv = os.path.join(data_folder, "metadata.csv")

    # Download the dataset if needed
    Dataset.download(parsed_args.dataset)

    # Check if the metadata file exist
    if not Dataset.metadata_exist(parsed_args.dataset):

        raise AssertionError(
            f"File {metadata_csv} is not found. Please generate this first!"
        )

    Dataset.load(metadata_csv)
    Collection.load()

    print("Starting Dash")
    run_dashboard()


# Execution
if __name__ == "__main__":

    main()
