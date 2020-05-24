import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
#from chart_studio.grid_objs import Column, Grid
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.express as px
print(px.data.__doc__)

from IPython.display import IFrame



neutral_tstamp = list()
neutral_values = list()
positive_tstamp = list()
positive_values = list()
negative_tstamp = list()
negative_values = list()

engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')
connection = engine.connect()
neutral_results = connection.execute("SELECT str_to_date(cast(concat(substr(timestamp , 5, 15), \" 2020\") as char(25)),\
                \"%%M %%d %%T %%Y\") \"timestamp\", count(*) \"NEUTRAL\"\
                from twitter.sentiment_score\
                where SUBSTR(score, 1, length(score) - 1) = \"Neutral\"\
                group by str_to_date(cast(concat(substr(timestamp , 5, 15), "
                                     "\" 2020\") as char(25)), '%%M %%d %%T %%Y');").fetchall()

positive_results = connection.execute("SELECT str_to_date(cast(concat(substr(timestamp , 5, 15), \" 2020\") as char(25)),\
                \"%%M %%d %%T %%Y\") \"timestamp\", count(*) \"POSITIVE\"\
                from twitter.sentiment_score\
                where SUBSTR(score, 1, length(score) - 1) = \"Positive\"\
                group by str_to_date(cast(concat(substr(timestamp , 5, 15), "
                                      "\" 2020\") as char(25)), '%%M %%d %%T %%Y');").fetchall()

negative_results = connection.execute("SELECT str_to_date(cast(concat(substr(timestamp , 5, 15), \" 2020\") as char(25)),\
                \"%%M %%d %%T %%Y\") \"timestamp\", count(*) \"NEGATIVE\"\
                from twitter.sentiment_score\
                where SUBSTR(score, 1, length(score) - 1) = \"Negative\"\
                group by str_to_date(cast(concat(substr(timestamp , 5, 15), "
                                      "\" 2020\") as char(25)), '%%M %%d %%T %%Y');").fetchall()
for row in neutral_results:
    #print(str(row[0]) + " " + str(row[1]))
    neutral_tstamp.append(str(row[0]))
    neutral_values.append(str(row[1]))
for row in positive_results:
    print(str(row[0]) + " " + str(row[1]))
    positive_tstamp.append(str(row[0]))
    positive_values.append(str(row[1]))
for row in negative_results:
    negative_tstamp.append(str(row[0]))
    negative_values.append(str(row[1]))

snp_date = list()
snp_close = list()
with open('SNP500.csv') as f:
    print("{0}".format(f.readline().split(",")))
    for x in f:
        x = x.split(",")
        snp_date.append(str(x[0]))
        snp_close.append(str(x[4]))

d1 = {'tstamp':positive_tstamp, 'neutral': neutral_values, 'positive': positive_values, 'negative':negative_values}
df = pd.DataFrame(d1)
print(df.head(10))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#333333',
    'text': '#7FDBFF'
}

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Sentiment Score',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Public Sentiment on COVID-19', style={
        'textAlign': 'center',
        'color': colors['text']
    }),



    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                #{'x': df['tstamp'], 'y': df['neutral'], 'type': 'line', 'name': 'Neutral'},
                #{'x': df['tstamp'], 'y': df['positive'], 'type': 'line', 'name': 'Positive'},
                {'x': df['tstamp'], 'y': df['negative'], 'type': 'line', 'name': 'Negative'},
                {'x': snp_date, 'y': snp_close, 'type': 'line', 'name': 'Stocks'},

            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

# if __name__ == '__main__':
app.run_server(debug=True)
