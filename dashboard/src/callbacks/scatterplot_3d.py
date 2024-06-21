from dash import Dash, html, Output, Input, callback
from Dataset import Dataset
from widgets import gallery
import config
from utils.similar_tracks import get_similar_tracks
from PIL import Image

@callback(
    [Output('album-cover', 'src'),
     Output('track-title', 'children'),
     Output('artist', 'children'),
     Output('genre', 'children'),
     Output('tempo', 'children'),
     Output("gallery", "children"),
     Output("gallery-card-header", "children")],
    [Input('scatterplot-3D', 'clickData'),
     Input('projection-radio-buttons', 'value')])
def update_selected_track(clickData, radio_button_value):
    print("Update selected track")
    if clickData is None:
        return 'assets/album_cover.png', '', '', '', '', '', 'No tracks selected yet!'
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

        return album_cover, track_title, artist, genre, tempo, gallery_children, gallery_card_header