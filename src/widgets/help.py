from dash import html, Output, Input, State, callback
import dash_bootstrap_components as dbc

def create_help_widget():
    return html.Div(
        [
            dbc.Button("Help", id="open-offcanvas", n_clicks=0),
            dbc.Offcanvas(
                html.Div([
    html.P("Welcome to the Genre Classification Dashboard! Here's a brief guide to help you navigate and make the most of the features available:"),
    
    html.H3("Overview"),
    html.P("This dashboard allows you to explore and analyze a collection of songs, visualizing their distribution across various genres, tempo, key, and loudness. You can also select individual tracks to view detailed information."),
    
    html.H3("Features"),
    html.Ul([
        html.Li([
            html.B("3-D Plot View:"),
            html.Ul([
                html.Li([html.B("Location:"), " Top left."]),
                html.Li([html.B("Description:"), " This 3D plot visualizes songs based on three dimensions (X, Y, Z) that may represent features such as tempo, loudness, or other extracted features. Different colors indicate different genres."])
            ])
        ]),
        html.Li([
            html.B("2-D Plot View:"),
            html.Ul([
                html.Li([html.B("Location:"), " Top center."]),
                html.Li([html.B("Description:"), " Similar to the 3D plot, this 2D plot provides an alternative view for visualizing songs on a two-dimensional plane."])
            ])
        ]),
        html.Li([
            html.B("Genre Distribution:"),
            html.Ul([
                html.Li([html.B("Location:"), " Top right."]),
                html.Li([html.B("Description:"), " This bar chart shows the count of songs in each genre, giving you an overview of the genre distribution within your dataset."])
            ])
        ]),
        html.Li([
            html.B("Detailed Track Information:"),
            html.Ul([
                html.Li([html.B("Location:"), " Bottom center."]),
                html.Li([html.B("Description:"), " When you select a track from the visualizations above, detailed information about the track will be displayed here, including the title, artist, genre, tempo (bpm), key, and loudness (dB)."])
            ])
        ]),
    ]),
    
    html.H3("How to Use"),
    html.Ul([
        html.Li([
            html.B("Viewing the Plots:"),
            html.Ul([
                html.Li([html.B("3-D and 2-D Views:"), " Use these views to explore the distribution and clustering of songs based on their features. Hover over the points to see more details about individual songs."])
            ])
        ]),
        html.Li([
            html.B("Selecting a Track:"),
            html.Ul([
                html.Li(["Click on any point in the 3-D or 2-D plot to select a song. The detailed information about the selected track will appear in the 'Detailed Track Information' section."])
            ])
        ]),
        html.Li([
            html.B("Genre Distribution Analysis:"),
            html.Ul([
                html.Li("Check the bar chart on the top right to understand the overall genre distribution in your dataset. This can help identify genre trends and the diversity of your song collection.")
            ])
        ]),
        html.Li([
            html.B("Switching Views:"),
            html.Ul([
                html.Li([html.B("UMAP/t-SNE Toggle:"), " Use the radio buttons on the top right to switch between different dimensionality reduction techniques (UMAP or t-SNE) for the 2D and 3D plots."])
            ])
        ]),
    ]),
    
    html.H3("Tips"),
    html.Ul([
        html.Li([html.B("Interactivity:"), " The plots are interactive, allowing you to zoom, pan, and rotate (for 3D plots) to get a better view of the data."]),
        html.Li([html.B("Exploration:"), " Experiment with different views and filters to gain deeper insights into the genre classification and other features of the songs."])
    ])
                    ]
                ),
                id="offcanvas",
                title="Quick Guide to Using the Prosono Dashboard",
                is_open=False,
            ),
        ]
    )


@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open