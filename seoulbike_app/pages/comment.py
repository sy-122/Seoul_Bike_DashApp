import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

dash.register_page(__name__)

layout = html.Div([
    html.H3(children='Write Comments'),
    dcc.Textarea(
        id='textarea',
        value='',
        style={'width': '100%', 'height': 200},
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='comment-output', style={'whiteSpace': 'pre-line'})
])


@callback(
    Output('comment-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('textarea', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        return 'Submitted Comment: {}'.format(value)
