import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import data_prep
from datetime import datetime as dt
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.read_csv('./Sensor Data for Projects/cleaned/all_clean_1.csv')
patients = df.patient_id.unique()
patients.sort()

# one_day = data_prep.clean('3012')
ticktext = ['12:00am','1:00am','2:00am','3:00am','4:00am','5:00am','6:00am','7:00am','8:00am','9:00am','10:00am','11:00am','12:00pm','1:00pm','2:00pm','3:00pm','4:00pm','5:00pm','6:00pm','7:00pm','8:00pm','9:00pm','10:00pm','11:00pm']

one_day = df[df['patient_id']==patients[0]]
fig = px.scatter_polar(one_day, r='n_day', theta='minutes', color='mod_desc',
    hover_data=['Date','Time'],size='size', size_max=3.5,opacity=0.8,
    labels= {'Date':'date'}, range_r=[-10, 150], height=1000,
    template={'layout':
    {'polar':{'angularaxis':{'tickmode':'array','tickvals':list(range(0,360,15)),'ticktext':ticktext},'radialaxis':{'showticklabels':False}}
    }})

# fig = go.Figure(
#     go.Scatterpolar(
#         r = one_day['n_day'],
#         theta = one_day['minutes'],
#         mode='markers',
#         marker = {'size':3.6}
#     ))

app.layout = html.Div(children=[
    html.H1(
        'Patient Sensor Data Visualization Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Dropdown(
        id='patient-selector',
        options=[{'label': i, 'value': i} for i in patients],
        value=patients[0]   
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=dt(2017, 5, 3),
        end_date_placeholder_text='Select a date!'
    ),
    dcc.Graph(
        id='graph',
        style= {
            'height' : '100vh'
        },
        figure= fig
    )
])

@app.callback(
    Output('graph','figure'),
    [Input('patient-selector','value')])
def update_figure(patient):
    # one_day = data_prep.clean('3012')
    # fig = px.scatter_polar(one_day, r='n_day', theta='Total Minutes', color='mod desc',
    # hover_data=['Date','Time'],size='size', size_max=3.5,opacity=0.8,
    # labels= {'n_day':'wtf_m8'})  

    one_day = df[df['patient_id']==patient]
    fig = px.scatter_polar(one_day, r='n_day', theta='minutes', color='mod_desc',
        hover_data=['Date','Time'],size='size', size_max=3.6,opacity=1.0,
        labels= {'Date':'date'}, range_r=[-10, 150], height=800, 
        template={'layout':
        {'polar':{'angularaxis':{'tickmode':'array','tickvals':list(range(0,360,15)),'ticktext':ticktext},'radialaxis':{'showticklabels':False}}
        }}
        )

#     # fig = go.Figure(
#     # go.Scatterpolar(
#     #     r = one_day['n_day'],
#     #     theta = one_day['minutes'],
#     #     mode='markers',
#     #     marker = {'size':3.6}
#     # ))
 
    return(fig)

if __name__ == '__main__':
    app.run_server(debug=True)
