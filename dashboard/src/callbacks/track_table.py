from dash import callback, Output, Input, html, State
from utils.similar_tracks import get_similar_tracks
from Dataset import Dataset
from Collection import Collection
from Dataset import Dataset
import config
from widgets import gallery
from PIL import Image

@callback(
    Output("grid", "rowData", allow_duplicate=True),
    Input("filter-view", "children"),
    prevent_initial_call=True
)
def update_table_selection(filters):
    filtered_ids = Collection.get_filter_selection_ids()
    data_selected = Dataset.get().iloc[filtered_ids]
    table_rows = data_selected[['title', 'artist', 'genre', 'tempo', 'key', 'loudness']].to_dict('records')
    return table_rows

@callback(
    [Output('album-cover', 'src', allow_duplicate=True),
     Output('track-title', 'children', allow_duplicate=True),
     Output('artist', 'children', allow_duplicate=True),
     Output('tempo', 'children', allow_duplicate=True),
     Output("gallery", "children", allow_duplicate=True),
     Output("gallery-card-header", "children", allow_duplicate=True)],
    Input("grid", "selectedRows"),
    State('projection-radio-buttons', 'value'),
    prevent_initial_call=True
)
def clicktosim(clickData, radio_button_value):
    if not len(clickData):
        return 'assets/album_cover.png', '', '', '', '', 'No tracks selected yet!'
    track_id = clickData[0]['id']
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

    return album_cover, track_title, artist, tempo, gallery_children, gallery_card_header