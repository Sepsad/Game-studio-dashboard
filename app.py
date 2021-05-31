import dash
from flask import Flask


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__) # define flask app.server

app = dash.Dash(__name__,    server=server, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
