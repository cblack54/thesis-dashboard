import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import data_prep
import datetime as dt
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.read_csv('./Sensor Data for Projects/cleaned/all_cleaned_2.csv')
patients = df.patient_id.unique()
patients.sort()

# one_day = data_prep.clean('3012')
ticktext = ['12:00am','1:00am','2:00am','3:00am','4:00am','5:00am','6:00am','7:00am','8:00am','9:00am','10:00am','11:00am','12:00pm','1:00pm','2:00pm','3:00pm','4:00pm','5:00pm','6:00pm','7:00pm','8:00pm','9:00pm','10:00pm','11:00pm']

# one_day = df[df['patient_id']==patients[0]]
# fig = px.scatter_polar(one_day, r='n_day', theta='minutes', color='mod_desc',
#     hover_data=['Date','Time'],size='size', size_max=3.5,opacity=0.8,
#     labels= {'Date':'date'}, range_r=[-10, 150], height=1000,
#     template={'layout':
#     {'polar':{'angularaxis':{'tickmode':'array','tickvals':list(range(0,360,15)),'ticktext':ticktext},'radialaxis':{'showticklabels':False}}
#     }})

# fig = go.Figure(
#     go.Scatterpolar(
#         r = one_day['n_day'],
#         theta = one_day['minutes'],
#         mode='markers',
#         marker = {'size':3.6}
#     ))
# df2 = [dict(Task="Job-1", Start='2017-01-01 01:00', Finish='2017-01-01 02:00', Resource='Complete'),
#         dict(Task="Job-1", Start='2017-01-01 02:00', Finish='2017-01-01 02:30', Resource='Not Started'),
#         dict(Task="Job-1", Start='2017-01-01 02:05', Finish='2017-01-01 02:55', Resource='Incomplete')]

df2 = pd.read_csv('./Sensor Data for Projects/cleaned/gantt_cleaned_1.csv')
df2['Task'] = pd.to_datetime(df2['Task']).dt.date
# df_intial_2 = df2[df2['patient_id']==3018]
# print(df_intial_2.head())
# print('wtf',df_intial_2.Task)
# print(dt.datetime.strptime(df2.Task.min(),'%Y-%m-%d')+dt.timedelta(days=35))
# df_intial_2 = df_intial_2[df_intial_2['Task'] < df_intial_2.Task.min() + dt.timedelta(days=35)]

# fig2 = ff.create_gantt(df_intial_2, show_colorbar=True, group_tasks=True)

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
        start_date=dt.datetime(2017, 5, 3),
        end_date_placeholder_text='Select a date!'
    ),
    dcc.Graph(
        id='polar_plot',
        style= {
            'height' : '100vh'
        },
        # figure=fig
    ),
    html.Div(),
    dcc.Graph(
        id='line_plot',
        style={
            'height':'80vh'
        },
        # figure= fig2
    )
])

@app.callback([
    Output('polar_plot','figure'),
    Output('line_plot','figure')],
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
        {'polar':{'angularaxis':{'tickmode':'array','tickvals':list(range(0,360,15)),'ticktext':ticktext},'radialaxis':{'showticklabels':False, 'showline': False}}
        }}
        )
    print(patient)
    line_plot_df = df2[df2['patient_id']==patient]
    
    line_plot_df = line_plot_df[line_plot_df['Task']<line_plot_df.Task.min() + dt.timedelta(days=35)].reset_index(drop=True)
    # print(line_plot_df.shape)
    # print(line_plot_df.head())
    fig2 = ff.create_gantt(line_plot_df, index_col='Resource', show_colorbar=True, group_tasks=True, bar_width=0.3)
    # fig2 = ff.create_gantt(line_plot_df, show_colorbar=True, group_tasks=True)


#     # fig = go.Figure(
#     # go.Scatterpolar(
#     #     r = one_day['n_day'],
#     #     theta = one_day['minutes'],
#     #     mode='markers',
#     #     marker = {'size':3.6}
#     # ))
 
    return(fig, fig2)

if __name__ == '__main__':
    app.run_server(debug=True)
