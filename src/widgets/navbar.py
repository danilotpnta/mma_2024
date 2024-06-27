import dash_bootstrap_components as dbc
from dash import html
import config
from widgets import help

def create_navbar(projection_radio_buttons_widget):
    offcanvas = help.create_help_widget()
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=config.PROSONO_LOGO, height="30px")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    style={"textDecoration": "none"},
                ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Row([projection_radio_buttons_widget,
                         offcanvas],
                        className='g-0 ms-auto flex-nowrap mt-3 mt-md-0',
                        align='center'),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
            ]
        ),
        color="white",
        dark=False,
        className='border-bottom'
    )

    return navbar