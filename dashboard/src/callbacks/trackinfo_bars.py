import ast
import config
from Dataset import Dataset
from dash import dcc, html, ClientsideFunction, clientside_callback, callback
from dash.dependencies import Input, Output, State


# Register the JavaScript function
clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize_track_info_bars"),
    Output("invisible-store", "data"),
    Input("song-data", "data"),
    State("invisible-store", "data"),
    prevent_initial_call=True,
)


@callback(
    Output("song-data", "data"),
    Input("scatterplot-3D", "clickData"),
    prevent_initial_call=True,
)
def store_click_data(clickData):

    print("Updating track info bars...")
    track_id = clickData["points"][0]["customdata"][0]
    d = Dataset.get()
    selected_track = d.loc[d["id"] == track_id]

    features_list = []
    for feature in [selected_track["sorted_pred_genres"], selected_track["keys"]]:
        feature_value = []
        feature_probabilities = []

        feature_dict = ast.literal_eval(feature.iloc[0])
        for k, v in feature_dict.items():
            feature_value.append(k)
            feature_probabilities.append(float(v))

        features_list.append([feature_value[:3], feature_probabilities[:3]])

    features_list[0][1] = [round(i * 100, 2) for i in features_list[0][1]]
    features_list[0].append([config.GENRE_COLORS[i] for i in features_list[0][0]])

    return features_list
