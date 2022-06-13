# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import logging
import datetime
from datetime import date
from pymongo import MongoClient
from pandas import DataFrame
from mongopw import username, passw
from ETF_tickers import ETF_tickers


client = MongoClient("mongodb+srv://{}:{}@cluster0.fogd9.mongodb.net/test?retryWrites=true&w=majority".format(username,passw))
dbs = client.list_database_names()
#print(dbs)

#select database ETF
database = client['ETF']
#select collection ETF
ETF_collection = database.get_collection("ETF")

def extract_multi_ETF_cours(ETF_list):
    for i in ETF_tickers:
        x   = []
        cur=ETF_collection.find()
        for j in cur:
            x.append(j)
    df = pd.DataFrame (x)
    del df["_id"]

    df_dateind=df.set_index('Date')

    df_sorted =df_dateind.sort_index(ascending=False)
    #df_sorted =df.sort_index(ascending=False)
    df_sorted_newin=df_sorted.reset_index()
    return df_sorted_newin


all_ETF_data=extract_multi_ETF_cours(ETF_tickers)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#all_ETF_data=pd.read_csv('midterm.csv', parse_dates=['Date'])  

fig = px.line(all_ETF_data, x="Date", y="Close",color="Ticker_ya",template='none')

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig3 = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)


app.layout = html.Div(children=[
    html.H1(children='Analyse ETF par thématique'),

    html.H2(children='''
        ETF analysis with dash Plotly and Mongo db Atlas.
    '''),
    
    html.Div(children=[
        html.Label('ETF sélectionné'),
        dcc.Dropdown(all_ETF_data['Ticker_ya'].unique(), 'IWVL.MI',id='xaxis-column'),
    ]),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.RangeSlider(
        all_ETF_data['Date'].dt.year.min(),
        all_ETF_data['Date'].dt.year.max(),
        step=1,
        value=[all_ETF_data['Date'].dt.year.min(),all_ETF_data['Date'].dt.year.max()],
        marks={str(date): str(date) for date in all_ETF_data['Date'].dt.year.unique()},
        id='year-slider'
    ),
    dcc.Graph(
        id='example-graph2',
        figure=fig
    ),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig3
    )
])

@app.callback(
    Output('example-graph', 'figure'),
    Input('xaxis-column', 'value'),
    Input('year-slider', 'value'),
    )
def update_figure(xaxis_column_name,selected_year):
    #filtered_df = all_ETF_data[all_ETF_data['Date'].dt.year == selected_year]
    filtered_df2 = all_ETF_data[all_ETF_data['Ticker_ya'] == xaxis_column_name]
    years_list=[y for y in range(min(selected_year),max(selected_year)+1)]
    filtered_df=filtered_df2[filtered_df2['Date'].dt.year.isin(years_list)]

    #logging.warning(selected_year)
    fig = px.line(filtered_df, x="Date", y="Close",color="Ticker_ya",template='none')

                     

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)