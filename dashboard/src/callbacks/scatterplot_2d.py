from dash import Dash, html, Output, Input, callback, State
from Dataset import Dataset
from widgets import scatterplot_2d
from widgets import gallery, categorical_histogram, numerical_histogram
import config
from utils.similar_tracks import get_similar_tracks
from PIL import Image

@callback(
    Output("grid", "rowData"),
    Output("genre_histogram", "figure", allow_duplicate=True),
    Output("tempo_histogram", "figure", allow_duplicate=True),
    Output("key_histogram", "figure", allow_duplicate=True),
    Output("loudness_histogram", "figure", allow_duplicate=True),
    Input("scatterplot-2D", "selectedData"),
    State('scatterplot-2D', 'figure'),
    State('genre_histogram', 'figure'),
    State('tempo_histogram', 'figure'),
    State('key_histogram', 'figure'),
    State('loudness_histogram', 'figure'),
    prevent_initial_call=True
)
def scatterplot_is_selected(data_selected, scatterplot_fig, genre_hist, tempo_hist, key_hist, loudness_hist):
    print('Scatterplot is selected')
    data_selected = scatterplot_2d.get_data_selected_on_scatterplot(data_selected)
    table_rows = data_selected[['title', 'artist', 'genre', 'tempo', 'key', 'loudness']].to_dict('records')
    
    genre_histogram = categorical_histogram.draw_histogram('genre', data_selected['id'])
    genre_histogram['data'][0].update({'marker': genre_hist['data'][0]["marker"]})
    
    key_histogram = categorical_histogram.draw_histogram('key', data_selected['id'])
    key_histogram['data'][0].update({'marker': key_hist['data'][0]["marker"]})
    
    print(tempo_hist)
    tempo_nbins = tempo_hist['data'][0]['nbinsx']
    tempo_histogram = numerical_histogram.draw_histogram('tempo', tempo_nbins, data_selected['id'])
    tempo_histogram['data'][0].update({'marker': tempo_hist['data'][0]["marker"]})
    
    loudness_nbins = loudness_hist['data'][0]['nbinsx']
    loudness_histogram = numerical_histogram.draw_histogram('loudness', loudness_nbins, data_selected['id'])
    loudness_histogram['data'][0].update({'marker': loudness_hist['data'][0]["marker"]})
    
    return table_rows, genre_histogram, tempo_histogram, key_histogram, loudness_histogram

@callback(
    [Output('album-cover', 'src', allow_duplicate=True),
     Output('track-title', 'children', allow_duplicate=True),
     Output('artist', 'children', allow_duplicate=True),
     Output('genre', 'children', allow_duplicate=True),
     Output('tempo', 'children', allow_duplicate=True),
     Output("gallery", "children", allow_duplicate=True),
     Output("gallery-card-header", "children", allow_duplicate=True),
     Output("grid", "rowData", allow_duplicate=True)],
    [Input('scatterplot-2D', 'clickData'),
     Input('projection-radio-buttons', 'value')],
    prevent_initial_call=True)
def update_selected_track(clickData, radio_button_value):
    print("Update selected track")
    if clickData is None:
        return 'assets/album_cover.png', '', '', '', '', '', 'No tracks selected yet!', []
    else:
        track_id = clickData['points'][0]['customdata'][0]
        d = Dataset.get()
        selected_track = d.loc[d['id'] == track_id].to_dict('records')[0]
        
        album_cover_path = f"{config.ROOT_DIR}/{selected_track['album_cover_path']}"
        try:
            album_cover = Image.open(album_cover_path)
        except:
            album_cover = Image.open('src/assets/album_cover.png')
        
        track_title = selected_track['title']
        artist = selected_track['artist']
        genre = selected_track['genre']
        tempo = f"{selected_track['tempo']:.2f}"

        similar_tracks_ids = get_similar_tracks(track_id, proj=radio_button_value)
        gallery_children = gallery.create_gallery_children(similar_tracks_ids)
        gallery_card_header = html.Span(['Tracks similar to: ', html.Strong(f'{track_title} - {artist}')])
    
        return album_cover, track_title, artist, genre, tempo, gallery_children, gallery_card_header, [selected_track]