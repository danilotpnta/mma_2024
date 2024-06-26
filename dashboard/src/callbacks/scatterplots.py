from dash import Dash, html, Output, Input, callback, State, ALL, callback_context
from Dataset import Dataset
from widgets import scatterplot_2d
from widgets import gallery, categorical_histogram, numerical_histogram
import config
from utils.similar_tracks import get_similar_tracks
from PIL import Image
from utils.utils import feature_key_from_state_string
import plotly.graph_objs as go

@callback(
    Output("grid", "rowData"),
    Output({"type": 'histogram', 'feature': ALL}, "figure"),
    Input("scatterplot-2D", "selectedData"),
    State('scatterplot-2D', 'figure'),
    State({"type": 'histogram', 'feature': ALL}, "figure"),
    prevent_initial_call=True
)
def scatterplot_2d_is_selected(data_selected, scatterplot_fig, histograms):#genre_hist, key_hist, tempo_hist, loudness_hist):
    print('Scatterplot is selected')

    data_selected = scatterplot_2d.get_data_selected_on_scatterplot(data_selected)
    table_rows = data_selected[['title', 'artist', 'genre', 'tempo', 'key', 'loudness', 'id']].to_dict('records')
    
    hist_dict = {feature_key_from_state_string(k): v for k, v in callback_context.states.items() if 'scatter' not in k}

    genre_histogram = categorical_histogram.draw_histogram('genre', data_selected['id'])
    genre_histogram['data'][0].update({'marker': hist_dict['genre']['data'][0]["marker"]})
    
    key_histogram = categorical_histogram.draw_histogram('key', data_selected['id'])
    key_histogram['data'][0].update({'marker': hist_dict['key']['data'][0]["marker"]})
    
    tempo_nbins = hist_dict['tempo']['data'][0]['nbinsx']
    tempo_histogram = numerical_histogram.draw_histogram('tempo', tempo_nbins, data_selected['id'])
    tempo_histogram['data'][0].update({'marker': hist_dict['tempo']['data'][0]["marker"]})
    
    loudness_nbins = hist_dict['loudness']['data'][0]['nbinsx']
    loudness_histogram = numerical_histogram.draw_histogram('loudness', loudness_nbins, data_selected['id'])
    loudness_histogram['data'][0].update({'marker': hist_dict['loudness']['data'][0]["marker"]})
    
    return table_rows, [genre_histogram, tempo_histogram, key_histogram, loudness_histogram]


for dim in ['2D', '3D']:
    @callback(
        [Output('album-cover', 'src', allow_duplicate=True),
        Output('track-title', 'children', allow_duplicate=True),
        Output('artist', 'children', allow_duplicate=True),
        Output('tempo', 'children', allow_duplicate=True),
        Output("gallery", "children", allow_duplicate=True),
        Output("gallery-card-header", "children", allow_duplicate=True),
        Output("grid", "rowData", allow_duplicate=True),
        Output(f'scatterplot-2D', 'figure', allow_duplicate=True),
        Output(f'scatterplot-3D', 'figure', allow_duplicate=True),],
        [Input(f'scatterplot-{dim}', 'clickData'),
        State('projection-radio-buttons', 'value'),
        State(f'scatterplot-2D', 'figure'),
        State(f'scatterplot-3D', 'figure')],
        prevent_initial_call=True)
    def update_selected_track(clickData, radio_button_value, current_figure_2d, current_figure_3d):
        print(f"Update selected track {dim}")
        if clickData is None:
            return 'assets/album_cover.png', '', '', '', '', 'No tracks selected yet!', [], current_figure_2d, current_figure_3d
        else:
            track_id = clickData['points'][0]['customdata'][0]
            d = Dataset.get()
            selected_track = d.loc[d['id'] == track_id].to_dict('records')[0]
            
            album_cover_path = f"{config.ROOT_DIR}/{selected_track['filename'].replace('wav', 'png')}"
            try:
                album_cover = Image.open(album_cover_path)
            except:
                album_cover = Image.open('src/assets/album_cover.png')
            
            track_title = selected_track['title']
            artist = selected_track['artist']
            tempo = f"{selected_track['tempo']:.2f}"

            similar_tracks_ids = get_similar_tracks(track_id, proj=radio_button_value)
            gallery_children = gallery.create_gallery_children(similar_tracks_ids)
            gallery_card_header = html.Span(['Tracks similar to: ', html.Strong(f'{track_title} - {artist}')])

            new_figures = []
            for current_figure in [current_figure_2d, current_figure_3d]:
                new_figure = go.Figure(data=current_figure['data'], layout=current_figure['layout'])

                for genre in new_figure.data:
                    if [track_id] in genre.customdata:
                        genre.marker.symbol = ['x' if i[0] == track_id else 'circle' for i in genre.customdata]
                    else:
                        genre.marker.symbol = 'circle'
                        
                new_figure['layout']['uirevision'] = True
                new_figures.append(new_figure)
        
            return album_cover, track_title, artist, tempo, gallery_children, gallery_card_header, [selected_track], *new_figures