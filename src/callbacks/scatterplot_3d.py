from dash import callback, Output, Input, State, dash

@callback(
    Output('placeholder', 'ee'),
    Input('scatterplot-3D', 'clickData')
)
def trackSelected(clickData):
    print('A track was selected')
    print(clickData)