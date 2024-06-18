from dash import Dash, html, Output, Input, callback
from Dataset import Dataset
from widgets import gallery
from utils.similar_tracks import get_similar_tracks

@callback(
    [Output('album-cover', 'src'),
     Output('track-title', 'children'),
     Output('artist', 'children'),
     Output('genre', 'children'),
     Output('tempo', 'children'),
     Output("gallery", "children"),
     Output("gallery-card-header", "children")],
    [Input('scatterplot-3D', 'clickData')])
def update_selected_track(clickData):
    if clickData is None:
        return 'assets/album_cover.png', '', '', '', '', '', 'No tracks selected yet!'
    else:
        track_id = clickData['points'][0]['customdata'][0]
        d = Dataset.get()
        selected_track = d.loc[d['id'] == track_id].to_dict('records')[0]
        
        album_cover = selected_track['album_cover']
        album_cover = 'assets/album_cover.png'
        
        track_title = selected_track['track_title']
        artist = selected_track['artist']
        genre = selected_track['genre']
        tempo = selected_track['tempo']

        similar_tracks_ids = get_similar_tracks(track_id)
        gallery_children = gallery.create_gallery_children(similar_tracks_ids)

        return album_cover, track_title, artist, genre, tempo, gallery_children, f'Tracks similar to {track_title} by {artist}'