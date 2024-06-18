from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from Dataset import Dataset
import config
from utils.similar_tracks import get_similar_tracks

from widgets import (
    projection_radio_buttons,
    scatterplot_3d,
    scatterplot_2d,
    track_info,
    track_table,
    genre_histogram,
    tempo_histogram,
    gallery
)

import callbacks.scatterplot_3d
import callbacks.projection_radio_buttons


def run_dashboard():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    projection_radio_buttons_widget = (projection_radio_buttons.create_projection_radio_buttons())

    scatterplot_3d_widget = scatterplot_3d.create_scatterplot(config.DEFAULT_PROJECTION)
    scatterplot_2d_widget = scatterplot_2d.create_scatterplot(config.DEFAULT_PROJECTION)

    genre_dist = genre_histogram.create_histogram()
    tempo_dist = tempo_histogram.create_histogram()

    track_info_widget = track_info.create_track_info()
    track_table_widget = track_table.create_table()


    gallery_widget = gallery.create_gallery()

    view_3d = dbc.Col([
        scatterplot_3d_widget,
        track_info_widget
    ], align='center', class_name="main-col")

    view_2d = dbc.Col([
        scatterplot_2d_widget,
        track_table_widget
    ], align='center', class_name="main-col")

    app.layout = dbc.Container(
        [
            projection_radio_buttons_widget,
            dbc.Row([
                dbc.Col(
                    dcc.Tabs(
                        [
                            dcc.Tab(label='3-D plot view', children=view_3d),
                            dcc.Tab(label='2-D plot view', children=view_2d)
                        ]
                    ),
                    width=6, className="main-col"
                ),
                dbc.Col(
                    [
                        dcc.Tabs(
                            [
                                dcc.Tab(label='genre distribution', children=genre_dist),
                                dcc.Tab(label='tempo distribution', children=tempo_dist)
                            ]
                        ),
                        gallery_widget]
                    , width=6, className="main-col"
                )
            ], className='top-row', justify='between')
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