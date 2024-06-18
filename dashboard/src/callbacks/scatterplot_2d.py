from dash import Output, Input, State, callback
from Dataset import Dataset
from widgets import scatterplot_2d

@callback(
    Output("grid", "rowData"),
    State('scatterplot-2D', 'figure'),
    Input("scatterplot-2D", "selectedData"),
    prevent_initial_call=True
)
def scatterplot_is_selected(scatterplot_fig, data_selected):
    print('Scatterplot is selected')

    data_selected = scatterplot_2d.get_data_selected_on_scatterplot(scatterplot_fig)
    table_rows = data_selected[['track_title', 'artist', 'genre']].to_dict('records')
    print(table_rows)
    scatterplot_2d.highlight_class_on_scatterplot(scatterplot_fig, None)

    return table_rows