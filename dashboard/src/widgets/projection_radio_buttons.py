import dash_bootstrap_components as dbc
import config


def create_projection_radio_buttons():

    return dbc.RadioItems(
        options=[{"label": label, "value": value} for (label, value) in [('UMAP', 'umap'), ('t-SNE', 'tsne')]],
        value=config.DEFAULT_PROJECTION,
        inline=True,
        id="projection-radio-buttons",
        class_name="radio-buttons",
    )