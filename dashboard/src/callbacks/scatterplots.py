from dash import Dash, html, Output, Input, callback, State, ALL, callback_context, no_update, Patch
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
    Output('scatterplot-3D', 'figure', allow_duplicate=True),
    Input("scatterplot-2D", "selectedData"),
    State('scatterplot-3D', 'figure'),
    State({"type": 'histogram', 'feature': ALL}, "figure"),
    prevent_initial_call=True
)
def scatterplot_2d_is_selected(data_selected, scatter_3d, _):#genre_hist, key_hist, tempo_hist, loudness_hist):
    print('Scatterplot is selected')

    data_selected = scatterplot_2d.get_data_selected_on_scatterplot(data_selected)
    table_rows = data_selected[['title', 'artist', 'genre', 'tempo', 'key', 'loudness', 'id']].to_dict('records')
    
    hist_dict = {feature_key_from_state_string(k): v for k, v in callback_context.states.items() if 'scatter' not in k}

    genre_histogram = categorical_histogram.draw_histogram('genre', data_selected['id'])
    genre_histogram['data'][0]['marker'].update({'pattern': hist_dict['genre']['data'][0]["marker"]['pattern']})
    
    key_histogram = categorical_histogram.draw_histogram('key', data_selected['id'])
    key_histogram['data'][0].update({'marker': hist_dict['key']['data'][0]["marker"]})
    
    tempo_nbins = hist_dict['tempo']['data'][0]['nbinsx']
    tempo_histogram = numerical_histogram.draw_histogram('tempo', tempo_nbins, data_selected['id'])
    tempo_histogram['data'][0].update({'marker': hist_dict['tempo']['data'][0]["marker"]})
    
    loudness_nbins = hist_dict['loudness']['data'][0]['nbinsx']
    loudness_histogram = numerical_histogram.draw_histogram('loudness', loudness_nbins, data_selected['id'])
    loudness_histogram['data'][0].update({'marker': hist_dict['loudness']['data'][0]["marker"]})
    
    fig_3d = Patch()
    for i, trace in enumerate(scatter_3d['data']):
        scatter_3d['data'][i]['marker']['opacity'] = [0.1 if i[0] in data_selected['id'] else 1 for i in trace['customdata']]
        scatter_3d['data'][i]['marker']['symbol'] = ['square' if i[0] in data_selected['id'] else 'circle' for i in trace['customdata']]
    
    fig_3d['data'] = scatter_3d['data']
    
    return table_rows, [genre_histogram, tempo_histogram, key_histogram, loudness_histogram], fig_3d


@callback(
    [Output('album-cover', 'src', allow_duplicate=True),
    Output('audio-player', 'src', allow_duplicate=True),
    Output('track-title', 'children', allow_duplicate=True),
    Output('artist', 'children', allow_duplicate=True),
    Output('tempo', 'children', allow_duplicate=True),
    Output('loudness', 'children', allow_duplicate=True),
    Output("gallery", "children", allow_duplicate=True),
    Output("gallery-card-header", "children", allow_duplicate=True),
    Output("grid", "rowData", allow_duplicate=True),
    Output(f'scatterplot-2D', 'figure', allow_duplicate=True),
    Output(f'scatterplot-3D', 'figure', allow_duplicate=True),
    Output("prev-scatter-click", 'data', allow_duplicate=True)],
    [Input(f'scatterplot-2D', 'clickData'),
    Input({'type': 'gallery-card', 'index': ALL}, 'n_clicks'),
    State('projection-radio-buttons', 'value'),
    State(f'scatterplot-2D', 'figure'),
    State(f'scatterplot-3D', 'figure'),
    State("prev-scatter-click", 'data')],
    prevent_initial_call=True)
def update_selected_track_2D(clickData, n_clicks, radio_button_value, current_figure_2d, current_figure_3d, prev_click):
    print(f"2D clicked")
    if clickData is None:
        curr_click = prev_click[0]
    else:
        curr_click = clickData['points'][0]['customdata'][0]

    # If [None, ..., n] and the previously registered click is the same as the current click (also if current click is None)
    n_clicks = [0 if x is None else x for x in n_clicks]
    if( (sum(n_clicks) < 1) and (len(n_clicks) > 0) and (curr_click == prev_click[0])): #or (('2D' != prev_click[1]) and (prev_click[1] != None)):
    # if (clickData == None and sum(n_clicks) < 1):
        print("2D Clicked cancelled 2")
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # clickData can be None if gallery-card is updated, but n_clicks might be [], [None, ..., n] or [1, None, ..., n]
    if clickData is None:
        
        # If n_clicks is []
        if len(n_clicks) == 0:
            return 'assets/album_cover.png', '', '', '', '', '', '', 'No tracks selected yet!', [], current_figure_2d, current_figure_3d
        
        # Get track id from gallery-card
        track_id = callback_context.triggered_id['index']
    
    # clickData is set, but n_clicks is [] or [None, ..., n]
    elif sum(n_clicks) == 0:
        track_id = clickData['points'][0]['customdata'][0]
    elif sum(n_clicks) > 0:
        track_id = callback_context.triggered_id['index']
    
    else:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    return *update_track(track_id, radio_button_value, current_figure_2d, current_figure_3d), [curr_click, prev_click[1]]

@callback(
    [Output('album-cover', 'src', allow_duplicate=True),
    Output('audio-player', 'src', allow_duplicate=True),
    Output('track-title', 'children', allow_duplicate=True),
    Output('artist', 'children', allow_duplicate=True),
    Output('tempo', 'children', allow_duplicate=True),
    Output('loudness', 'children', allow_duplicate=True),
    Output("gallery", "children", allow_duplicate=True),
    Output("gallery-card-header", "children", allow_duplicate=True),
    Output("grid", "rowData", allow_duplicate=True),
    Output(f'scatterplot-2D', 'figure', allow_duplicate=True),
    Output(f'scatterplot-3D', 'figure', allow_duplicate=True),
    Output("prev-scatter-click", 'data', allow_duplicate=True),
    Output("song-data", 'data', allow_duplicate=True)],
    [Input(f'scatterplot-3D', 'clickData'),
    Input({'type': 'gallery-card', 'index': ALL}, 'n_clicks'),
    State('projection-radio-buttons', 'value'),
    State(f'scatterplot-2D', 'figure'),
    State(f'scatterplot-3D', 'figure'),
    State("prev-scatter-click", 'data')],
    prevent_initial_call=True)
def update_selected_track_3D(clickData, n_clicks, radio_button_value, current_figure_2d, current_figure_3d, prev_click):
    print(f"3D clicked")
    if clickData is None:
        curr_click = prev_click[1]
    else:
        curr_click = clickData['points'][0]['customdata'][0]

    # If [None, ..., n] and the previously registered click is the same as the current click (also if current click is None)
    n_clicks = [0 if x is None else x for x in n_clicks]
    # if (clickData == None and sum(n_clicks) < 1):
    if( (sum(n_clicks) < 1) and (len(n_clicks) > 0) and (curr_click == prev_click[1])): #or (('3D' != prev_click[1]) and (prev_click[1] != None)):
        print("3D cancelled")
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # clickData can be None if gallery-card is updated, but n_clicks might be [], [None, ..., n] or [1, None, ..., n]
    if clickData is None:
        
        # If n_clicks is []
        if len(n_clicks) == 0:
            return 'assets/album_cover.png', '', '', '', '', '', '', 'No tracks selected yet!', [], no_update, no_update, no_update

        # Get track id from gallery-card
        track_id = callback_context.triggered_id['index']
    
    # clickData is set, but n_clicks is [] or [None, ..., n]
    elif sum(n_clicks) == 0:
        track_id = clickData['points'][0]['customdata'][0]
    elif sum(n_clicks) > 0:
        track_id = callback_context.triggered_id['index']
    else:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    return *update_track(track_id, radio_button_value, current_figure_2d, current_figure_3d), [prev_click[0], curr_click], track_id


def update_track(track_id, radio_button_value, current_figure_2d, current_figure_3d):
    print("Updating track")
    d = Dataset.get()
    selected_track = d.loc[d['id'] == track_id].to_dict('records')[0]
    
    album_cover_path = f"{config.ROOT_DIR}/{selected_track['album_cover_path']}"
    try:
        album_cover = Image.open(album_cover_path)
    except:
        album_cover = Image.open('src/assets/album_cover.png')
    
    audio_file_path = f"{config.BASE_URL}/{selected_track['filepath']}"

    track_title = selected_track['title']
    artist = selected_track['artist']
    tempo = f"{selected_track['tempo']:.2f}"
    loudness = f"{selected_track['loudness']:.2f}"

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

    return album_cover, audio_file_path, track_title, artist, tempo, loudness, gallery_children, gallery_card_header, [selected_track], *new_figures
