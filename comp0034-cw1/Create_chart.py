from pathlib import Path
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

# Import Data
BIKE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'Bike_data_adjusted.csv')
df_bike = pd.read_csv(BIKE_DATA_FILEPATH, encoding='unicode_escape')

# ------------------------#
# Create Graphs
# ------------------------#
# Bar graph for Month vs Bicycle Rented
month_bar_graph = px.bar(
    data_frame=df_bike.groupby('Month').mean('Count').reset_index(),
    x='Month',
    y="Count",
    labels={'Month': 'Month', 'Count': 'Average Bike Used'},
    template="simple_white",
)


# Line plot for Hour VS Bicycle Rented
hour_line_plot = px.line(data_frame=df_bike.groupby('Hour').mean('Count').reset_index(),
                         x='Hour',
                         y='Count',
                         markers=True,
                         labels={'Hour': 'Time', 'Count': 'Average Bike Used'},
                         )

def hour_line_plot():
    df_hour_avg = df_bike.groupby('Hour').mean('Count').reset_index(),
    df_day = df_hour_avg.loc[df_hour_avg['DayofWeek'] == 'Sunday']
    fig = px.line(df_day, x='Hour', y='Count', markers=True,
                  labels={'Hour': 'Time', 'Count': 'Average Bike Used'},
                  )
    return fig

# Heatmap


# ------------------------#
# Create App
# ------------------------#
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
                className="text-center p-4"),
        html.P(children='Learn about the different variables that affect the usage of bike.',
               className="text-center p-2"),
        html.Br(),

        dcc.Tabs(id="tabs-graph", value='tab-content-graph', children=[
            dcc.Tab(label='Time & Month', value='time_related'),
            dcc.Tab(label='Other Variables', value='heatmap'),
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
            dbc.Row([
                html.H4('Average Bike rented per hour'),
                dbc.Col([
                    html.Label(['Choose variables:'],
                               style={'font-weight': 'bold', "text-align": "center"}),
                    dcc.Dropdown(id='line-dropdown',
                                 options=['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                                          'Thursaday', 'Friday', 'Saturday'],
                                 placeholder='Please select ...')], width=3
                ),
                dbc.Col(
                    dcc.Graph(
                        id='line-plot',
                        figure=hour_line_plot
                    )
                )
            ]),
            dbc.Row([
                html.Br(),
                html.H4('Average Bike rented each Month'),
                dcc.Graph(id='month_bar', figure=month_bar_graph)
            ])
        ])
    elif tab == 'heatmap':
        return html.Div([html.H4('Live adjustable subplot-width'), ])


# Connecting the Dropdown values to the line-graph
@app.callback(Output("hour-line", "figure"),
              Input("line-dropdown", "value"))
def update_line_chart(weekday):
    fig_r = hour_line_plot(weekday)
    return fig_r


if __name__ == '__main__':
    app.run_server(debug=True)