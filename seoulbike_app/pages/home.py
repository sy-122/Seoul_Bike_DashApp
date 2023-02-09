import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import dash_daq as daq
from seoulbike_app import create_charts as cc

dash.register_page(__name__, path='/')

# Create the app layout using Bootstrap fluid container
layout = dbc.Container(
    children=[
        html.H1(children='Welcome to Seoul Public Bicycle Website!',
                className='text-center p-4'),
        html.Img(src=dash.get_asset_url('seoul-bike.png'),
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
@callback(Output(component_id='tabs-content-graph', component_property='children'),
          Input(component_id='nav-tabs', component_property='value'))
def render_content(tab):
    if tab == 'time-related':
        return html.Div([
            dbc.Row([
                html.H4('Average Bike rented each hour of the day'),
                html.P('Add line by clicking on legend.'),
                dcc.Graph(id='hour_line', figure=cc.hour_line_plot.update_traces(
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


# Bar Graph Boolean Switch to show percent of days that are holiday
@callback(
    Output(component_id='boolean-switch-output', component_property='children'),
    Input(component_id='boolean-switch', component_property='on')
)
def update_output(on):
    if on:
        fig = cc.month_bar_graph(cc.bar_new_df, 'Holiday%')
        fig = fig.update_traces(textposition='outside')
        dcc.Graph(figure=fig)
        return [dcc.Graph(figure=fig)]
    else:
        fig = cc.month_bar_graph()
        return [dcc.Graph(figure=fig)]


# Display additional scatter plot
@callback(
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


# Update scatter plot through dropdown
@callback(
    Output(component_id={'type': 'scatter-plot-add', 'index': MATCH}, component_property='figure'),
    Input(component_id={'type': 'scatter-dropdown', 'index': MATCH}, component_property='value')
)
def update_scatter_plot(x_variable):
    # if no x-variable selected return blank graph
    if x_variable is None:
        return {'data': []}
    else:
        fig_new = cc.scatter_plot(x_variable)
        fig_new.update_layout(title_text=str(x_variable) + ' VS Number of Bike Rented',
                              title_x=0.5)
        return fig_new
