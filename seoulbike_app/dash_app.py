import dash
import dash_bootstrap_components as dbc

# Create the Dash app using Bootstrap
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}
    ],
)

# Create the app layout using Bootstrap fluid container
app.layout = dbc.Container([
    dbc.NavbarSimple([
        dbc.DropdownMenu([
            dbc.NavLink('Home', href=dash.page_registry['pages.home']['path']),
            dbc.NavLink('Comments', href=dash.page_registry['pages.comment']['path'])
        ],
            nav=True,
            in_navbar=True,
            label='Menu'
        ),
    ],
        brand='Seoul Bicycle',
        brand_href='#',
        color='secondary',
        className='nav-tab'
    ),
    dash.page_container
],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
