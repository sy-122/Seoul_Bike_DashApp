import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

dash.register_page(__name__)

# Comment page layout using Bootstrap fluid container
layout = html.Div([
    html.H3(children='Write Comments'),
    html.P(children='Please share your thoughts about the app so we can improve.'),
    dcc.Textarea(
        id='comment-area',
        value='',
        style={'width': '100%', 'height': 200},
    ),
    html.Button('Submit', id='button', n_clicks=0),
    html.Div(id='comment-output', style={'whiteSpace': 'pre-line'})
])


# Submit comment when pushed 'Submit' and record all comments submitted
@callback(
    Output('comment-output', 'children'),
    Input('button', 'n_clicks'),
    [
        State('comment-area', 'value'),
        State('comment-output', 'children'),
    ],
)
def update_output(n_clicks, value, children):
    if n_clicks > 0:
        return f'{children}\n Submitted Comment: {value}'
    else:
        return ''
