from dash import Dash, html, dcc
from src import config
from src.Dataset import Dataset
from src.widgets import projection_radio_buttons, gallery, scatterplot, wordcloud, graph, heatmap, histogram, help_popup
from src.widgets.table import create_table
import dash_bootstrap_components as dbc