import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('V00 All Views.csv')
cols = df.columns.values.tolist() # cols for y
for col in ['Date','view']:
    cols.remove(col)

views = df['view'].unique()

app.layout = html.Div([
    
    dcc.Dropdown(
        id='views',
        options=[{'label': i, 'value': i} for i in views],
        value='V02 M1 9 Stocks'
    ),

    dcc.Graph(id='return'),
    
])

@app.callback(
    Output('return', 'figure'), # graph_id, object to output
    [Input('views', 'value')]) # dropdown_id, value to input
def update_graph(views_value):
    dff = df[df['view']==views_value] # filter to user selected views dropdown value

    return { # dict w two elements: data, layout
        'data': [go.Scatter(
            x=dff['Date'],
            y=dff[col],
            name=col
        ) for col in cols], # value for data is a list of "lines".. for now I keep x and y
        'layout': go.Layout(
            xaxis={
                'title': 'Date',
            },
            yaxis={
                'title': 'Return1',
            }
        ) # value for layout is one object.. returned by go.Layout()
    }

if __name__ == '__main__':
    app.run_server(debug=True)