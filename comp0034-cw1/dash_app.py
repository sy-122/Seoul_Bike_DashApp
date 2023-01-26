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
    template="simple_white"
)

# Line plot for Hour VS Bicycle Rented
hour_line_plot1 = px.line(
    data_frame=df_bike.groupby(['DayofWeek','Hour']).mean('Count').reset_index(),
    x='Hour', y='Count', color='DayofWeek', markers=True,
    labels={'Hour': 'Time', 'Count': 'Average Bike Used'},
    template="simple_white"
)

# Scatter Plot
def scatter_plot(x_var):
    fig = px.scatter(
        data_frame=df_bike,
        x=x_var,
        y="Count",
        trendline='ols',
        trendline_color_override="red",
        opacity=0.3,
        labels={'x': x_var, 'Count': 'Bike Rented'},
        template="simple_white"
)
    return fig

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
    color="secondary",
)

# Create the app layout using Bootstrap fluid container
app.layout = dbc.Container(
    children=[
        navbar,
        html.H1(children='Welcome to Seoul Public Bicycle Website!',
                className = "text-center p-4"),
        html.P(children='Learn about the different variables that affect the usage of bike.',
                className = "text-center p-2"),
        html.Br(),

        dcc.Tabs(id="nav-tabs", value='tab-content-graph', children=[
            dcc.Tab(label='Time & Month', value='time-related'),
            dcc.Tab(label='Other Variables', value='others'),
        ]),
        html.Div(id='tabs-content-graph')

    ],
    fluid=True
)

# Callback for Tab
@app.callback(Output('tabs-content-graph', 'children'),
              Input('nav-tabs', 'value'))
def render_content(tab):
    if tab == 'time-related':
        return html.Div([
            dbc.Row([
                html.H4('Average Bike rented each hour of the day'),
                dcc.Graph(id='hour_line', figure=hour_line_plot1)
            ]),
            dbc.Row([
                html.Br(),
                html.H4('Average Bike rented each Month'),
                dcc.Graph(id='month_bar', figure=month_bar_graph)
            ])
        ]),
    elif tab == 'others':
        return html.Div([
            dbc.Row([
                html.Br(),
                html.H4('How does other variables effect the number of bike rented'),
                #dbc.Col([
                    #dcc.Graph(id='heatmap', figure=heatmap),
                    #]),
                dbc.Col([
                    html.Label(['Choose variables:'],
                               style={'font-weight': 'bold', "text-align": "center"}),
                    dcc.Dropdown(id='scatter-dropdown',
                                 options=[
                                     {'label': 'Humidity', 'value': 'Humidity'},
                                     {'label': 'Wind Speed', 'value': 'Windspeed'},
                                     {'label': 'Solar Radiation', 'value': 'Solar_Rad'},
                                     {'label': 'Snow', 'value': 'Snowfall'},
                                     {'label': 'Rain', 'value': 'Rainfall'},
                                 ],
                                 placeholder='Please select ...'),
                    dcc.Graph(id='scatter-plot')
                ]),
            ]),
        ])

@app.callback(Output("scatter-plot", "figure"),
              Input("scatter-dropdown", "value"))
def change_scatter_plot(x_variable):
    fig_new = scatter_plot(x_variable)
    fig_new.update_layout(title_text=str(x_variable) + ' VS Number of Bike Rented',
                      title_x=0.5)
    return fig_new

if __name__ == '__main__':
    app.run_server(debug=True)


#pip install statsmodels