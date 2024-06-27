from dash import Dash, html, Output, Input, callback
from Dataset import Dataset
from widgets import gallery
import config
from utils.similar_tracks import get_similar_tracks
from PIL import Image
import plotly.graph_objs as go

@callback(
    [Output('album-cover', 'src'),
     Output('track-title', 'children'),
     Output('artist', 'children'),
     Output('tempo', 'children'),
     Output("gallery", "children"),
     Output("gallery-card-header", "children"),
     Output('scatterplot-3D', 'figure')],
    [Input('scatterplot-3D', 'clickData'),
     Input('projection-radio-buttons', 'value'),
     Input('scatterplot-3D', 'figure')])
def update_selected_track(clickData, radio_button_value, current_figure):
    print("Update selected track 3D")
    if clickData is None:
        return 'assets/album_cover.png', '', '', '', '', 'No tracks selected yet!', current_figure
    else:
        track_id = clickData['points'][0]['customdata'][0]
        return update_track(track_id, radio_button_value, current_figure)


def update_track(track_id, radio_button_value, current_figure):

        d = Dataset.get()
        selected_track = d.loc[d['id'] == track_id].to_dict('records')[0]
        
        album_cover_path = f"{config.ROOT_DIR}/{selected_track['album_cover_path']}"
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

        new_figure = go.Figure(data=current_figure['data'], layout=current_figure['layout'])
        
        for genre in new_figure.data:
            if [track_id] in genre.customdata:
                genre.marker.symbol = ['x' if i[0] == track_id else 'circle' for i in genre.customdata]
            else:
                genre.marker.symbol = 'circle'

        return album_cover, track_title, artist, tempo, gallery_children, gallery_card_header, new_figure