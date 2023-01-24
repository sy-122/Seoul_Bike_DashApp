from pathlib import Path
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

# Import Data
BIKE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'Bike_data_adjusted.csv')
df_bike = pd.read_csv(BIKE_DATA_FILEPATH, encoding='unicode_escape')

# Create the Dash app using Bootstrap
app = Dash(
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

# Create navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Home", href="/", active="exact"),
                dbc.DropdownMenuItem("Comments", href="/comments", active="exact")
            ],
            nav=True,
            in_navbar=True,
            label="Menu",
        ),
    ],
    brand="Seoul Bicycle",
    brand_href="#",
    color="Green",
    dark=True,
)

# Create the app layout using Bootstrap fluid container
app.layout = dbc.Container(
    children=[
        navbar,
        html.H1(children='Welcome to Seoul Public Bicycle Website!',
                className = "text-center p-4"),
        html.H3(children='Learn about the different variables that affect the usage of bike.',
                className = "text-center p-2"),
        html.Br(),

        dcc.Tabs(id="tabs-graph", value='tab-content-graph', children=[
            dcc.Tab(label='Variables Related to Day/Time', value='time_related'),
            dcc.Tab(label='Weather Variables', value='scatter_plots'),
        ]),
        html.Div(id='tabs-content-graph')

    ],
    fluid=True
)

# Callback for Tab
@app.callback(Output('tabs-content-graph', 'children'),
              Input('tabs-graph', 'value'))
def render_content(tab):
    if tab == 'time_related':
        return html.Div([
            html.Br(),
            html.H3('How does the average number of bike rented change '
                    'with Date/Time related variables?'),
            html.Label(['Choose variables:'],
                       style={'font-weight': 'bold', "text-align": "center"}),
            # Create Dropdown for bar graph x variables
            dcc.Dropdown(
                id='bar_dropdown',
                options=[
                    {'label': 'Before/After 6pm', 'value': 'Day_Night'},
                    {'label': 'Day of Week', 'value': 'DayofWeek'},
                    {'label': 'Month', 'value': 'Month'},
                    {'label': 'Holiday', 'value': 'Holiday'}],
                disabled=False,
                multi=False,
                placeholder='Please select...',
                style={'width': "100%"},
            ),
            dcc.Graph(
                id='bar_bike'
            ),
        ])
    elif tab == 'scatter_plots':
        return html.Div([
            html.H4('Live adjustable subplot-width'),
        ])

# Connecting the Dropdown values to the graph
@app.callback(Output("bar_bike", "figure"),
              Input("bar_dropdown", "value"))
def make_bar_graph(time_variable):
    fig = px.bar(
        data_frame=df_bike.groupby([time_variable]).mean('Count').reset_index(),
        x=time_variable,
        y="Count",
        labels={'x': time_variable, 'Count': 'Average Bike Used'},
        template="simple_white"
    )
    fig.update_layout(title_text=time_variable + ' VS Average Rented Bike',
                      title_x=0.5)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)