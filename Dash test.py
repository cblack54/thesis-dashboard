import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import data_prep

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

one_day = data_prep.clean()

# fig = go.Figure(
#     go.Scatterpolar(
#         r = one_day['n_day'],
#         theta = one_day['Total Minutes'],
#         mode='markers',
#         marker = {'size':1}
#     ))

fig = px.scatter_polar(one_day, r='n_day', theta='Total Minutes', color='mod desc',
 hover_data=['Date','Time'],size='size', size_max=3.5,opacity=0.8,
 labels= {'n_day':'wtf_m8'})


app.layout = html.Div(children=[
    html.H1(
        'Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        style= {
            'height' : '80vh'
        },
        figure= fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
