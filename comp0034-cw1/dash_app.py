from pathlib import Path
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State, MATCH
import dash_daq as daq

# ------------------------#
# Import Data and Prepare
# ------------------------#
# Import Data
BIKE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'Bike_data_adjusted.csv')
df_bike = pd.read_csv(BIKE_DATA_FILEPATH, encoding='unicode_escape')

# Convert 'Count' to integer
df_bike['Count'] = df_bike['Count'].astype(int)

# Dataframe with percent of holiday in each month for bar graph
bar_original_df = df_bike.groupby(['Month']).mean('Count').reset_index()
Month_Holiday = df_bike.groupby(['Month'])['Holiday'].\
    value_counts(normalize=True).reset_index(name='Holiday%')
Month_Holiday = Month_Holiday[Month_Holiday.Holiday == 'Holiday']
Month_Holiday['Holiday%'] = Month_Holiday['Holiday%'].apply(lambda x: x * 100)
Month_Holiday['Holiday%'] = Month_Holiday['Holiday%'].apply(lambda x: '{0:1.2f}%'.format(x))
bar_new_df = pd.merge(bar_original_df, Month_Holiday, how='left', on='Month')

# ------------------------#
# Create graphs
# ------------------------#
# Line plot for Hour VS Bicycle Rented
hour_line_plot1 = px.line(
    data_frame=df_bike.groupby(['DayofWeek', 'Hour']).mean('Count').reset_index(),
    x='Hour',
    y='Count',
    category_orders={'DayofWeek': ['Sunday', 'Monday', 'Tuesday',
                                   'Wednesday', 'Thurday', 'Friday',
                                   'Saturday']},
    color='DayofWeek',
    labels={'Hour': 'Time', 'Count': 'Average Bike Rented'},
    markers=True,
    template='simple_white'
)

# Make bar graph for Month vs Bicycle Rented
def month_bar_graph(df=bar_original_df, bar_text=None):
    fig = px.bar(
        data_frame=df,
        x='Month',
        y='Count',
        text=bar_text,
        labels={'Month': 'Month',
                'Count': 'Average Bike Rented per hour'},
        template='simple_white'
    )
    return fig

# Make Scatter Plot with different x-variables
def scatter_plot(x_var):
    fig = px.scatter(
        data_frame=df_bike,
        x=x_var,
        y='Count',
        trendline='ols',
        trendline_color_override='red',
        opacity=0.3,
        labels={'x': x_var,
                'Count': 'Bike Rented'},
        template='simple_white'
    )
    return fig

# ------------------------#
# Create App
# ------------------------#
# Create the Dash app using Bootstrap
app = Dash(external_stylesheets=[dbc.themes.LUX],
           meta_tags=[
               {"name": "viewport", "content": "width=device-width, initial-scale=1"}
           ],
           suppress_callback_exceptions=True
           )

# Create navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Home', href='/', active='exact'),
                dbc.DropdownMenuItem('Comments', href='/', active='exact')
            ],
            nav=True,
            in_navbar=True,
            label='Menu',
        ),
    ],
    brand='Seoul Bicycle',
    brand_href='#',
    color='secondary',
    className='nav-tab'
)

# Create the app layout using Bootstrap fluid container
app.layout = dbc.Container(
    children=[
        navbar,
        html.H1(children='Welcome to Seoul Public Bicycle Website!',
                className='text-center p-4'),
        html.Img(src=app.get_asset_url('seoul-bike.png'),
                 className='center'),
        html.P(children='Learn about the different variables that affect the usage of bike.',
               className='text-center p-2'),
        html.Br(),
        dcc.Tabs(id='nav-tabs', value='tab-content-graph',
                 children=[
            dcc.Tab(label='Time & Month', value='time-related'),
            dcc.Tab(label='Other Variables', value='others'),
        ]),
        html.Div(id='tabs-content-graph')
    ],
    fluid=True
)

# Callback for Tab
@app.callback(Output(component_id='tabs-content-graph', component_property='children'),
              Input(component_id='nav-tabs', component_property='value'))
def render_content(tab):
    if tab == 'time-related':
        return html.Div([
            dbc.Row([
                html.H4('Average Bike rented each hour of the day'),
                html.P('Add line by clicking on legend.'),
                dcc.Graph(id='hour_line', figure=hour_line_plot1.update_traces(
                    selector=lambda t: t.name != 'Monday', visible='legendonly'))
            ]),
            dbc.Row((
                html.Br(),
                html.H4('Average Bike rented each Month'),
                daq.BooleanSwitch(
                    id='boolean-switch',
                    on=False,
                    color='#78c2ad',
                    label='% of days that are Holiday'
                ),
                html.Div(
                    [dcc.Graph(id='bar')], id='boolean-switch-output')
            ))
        ]),
    elif tab == 'others':
        return html.Div([
            dbc.Row([
                html.Br(),
                html.H4('How does other variables effect the number of bike rented'),
                dbc.Col([
                    html.Button('Add Chart', id='add-chart', n_clicks=0),
                    html.Div(id='container', children=[])
                ]),
            ]),
        ])

#Bar Graph Boolean Switch to show percent of days that are holiday
@app.callback(
    Output(component_id='boolean-switch-output', component_property='children'),
    Input(component_id='boolean-switch', component_property='on')
)
def update_output(on):
    if on:
        fig = month_bar_graph(bar_new_df, 'Holiday%')
        fig = fig.update_traces(textposition='outside')
        dcc.Graph(figure=fig)
        return [dcc.Graph(figure=fig)]
    else:
        fig = month_bar_graph()
        return [dcc.Graph(figure=fig)]

#Display additional scatter plot
@app.callback(
    Output(component_id='container', component_property='children'),
    [Input(component_id='add-chart', component_property='n_clicks')],
    [State(component_id='container', component_property='children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '75%', 'display': 'inline-block',
               'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Graph(
                id={
                    'type': 'scatter-plot-add',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.Dropdown(id={'type': 'scatter-dropdown',
                             'index': n_clicks},
                         options=[
                             {'label': 'Humidity', 'value': 'Humidity'},
                             {'label': 'Wind Speed', 'value': 'Windspeed'},
                             {'label': 'Solar Radiation', 'value': 'Solar_Rad'},
                             {'label': 'Snow', 'value': 'Snowfall'},
                             {'label': 'Rain', 'value': 'Rainfall'},
                         ],
                         value=None,
                         placeholder='Please select ...',
                         )
        ])
    div_children.append(new_child)
    return div_children

#Update scatter plot through dropdown
@app.callback(
    Output(component_id={'type': 'scatter-plot-add', 'index': MATCH},  component_property='figure'),
    Input(component_id={'type': 'scatter-dropdown', 'index': MATCH}, component_property='value')
)
def update_scatter_plot(x_variable):
    # if no x-variable selected return blank graph
    if x_variable is None:
        return {'data': []}
    else:
        fig_new = scatter_plot(x_variable)
        fig_new.update_layout(title_text=str(x_variable) + ' VS Number of Bike Rented',
                              title_x=0.5)
        return fig_new


if __name__ == '__main__':
    app.run_server(debug=True)
