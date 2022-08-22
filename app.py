# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from typing import Container
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
#from pandas import DataFrame
from read_datahisto_multi import all_ETF_data
from data_info import data_ETF_info, extract_ETF_info, sectorweight, data_holding
import dash_bootstrap_components as dbc
from read_indiceshisto_multi import all_indices_data


# external_stylesheets = [
#     'https://codepen.io/chriddyp/pen/bWLwgP.css',
#     {
#         'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
#         'rel': 'stylesheet',
#         'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
#         'crossorigin': 'anonymous'
#     }
# ]
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets=[dbc.themes.MINTY, dbc.icons.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets,title='ETF Analytics',meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],)
#assets_external_path

#app.scripts.config.serve_locally = False

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#all_ETF_data=pd.read_csv('midterm.csv', parse_dates=['Date'])  

fig = px.line(all_ETF_data, x="Date", y="Close",color="Ticker_ya",template='none')
fig_indices = px.line(all_indices_data, x="Date", y="Close",color="Ticker_ya",template='none')

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig3 = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=100)

# fig_candel=go.Figure(data=[go.Candlestick(x=all_ETF_data['Date'],
#                 open=all_ETF_data['Open'],
#                 high=all_ETF_data['High'],
#                 low=all_ETF_data['Low'],
#                 close=all_ETF_data['Close'])]
                
#                 )
nav = dbc.Nav(
    dbc.Container(
        dbc.Row(
    [   html.I(className="bi bi-house", style={"font-size": "40px","width": "10%"}),
        dbc.NavItem(dbc.NavLink("ETF", active=True, href="/ETF")),
        dbc.NavItem(dbc.NavLink("Indices", href="/Indices")),
        dbc.NavItem(dbc.NavLink("Analyses", href="/Analyses")),
        dbc.NavItem(dbc.NavLink("Devises", disabled=True, href="#")),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("EUR"), dbc.DropdownMenuItem("USD")],
            label="Sélection",
            nav=True,
        ),
    ],
        align="center"
        ),
        class_name="mx-0"
    ),
    pills=True, 
    justified=True,
    
    )


#icon=  html.I(className="bi bi-bank"),
                


app.layout = html.Div(children=[
    
    nav,

    dbc.Container(
        html.H1(children='Analyse ETF par thématique'),
        class_name="mx-0"
        ),
     dbc.Col(  
    dbc.Container(
        [
    html.H2(children=data_ETF_info.longName, id='etf_lg_name'),
    html.Div(children=data_ETF_info.longBusinessSummary, id='etf_lg_businessSummary'),
    html.Div(children=[
        html.Label('ETF sélectionné'),
        dcc.Dropdown(all_ETF_data['Ticker_ya'].unique(), 'CSSPX.MI',id='xaxis-column',style={"width": "100%"}),
    ]),
    
    dcc.Graph(
        id='example-graph',
        figure=fig,
        style={"height": "100%","width": "100%"}
    ),

    dcc.RangeSlider(
        all_ETF_data['Date'].dt.year.min(),
        all_ETF_data['Date'].dt.year.max(),
        step=1,
        value=[all_ETF_data['Date'].dt.year.min(),all_ETF_data['Date'].dt.year.max()],
        marks={str(date): str(date) for date in all_ETF_data['Date'].dt.year.unique()},
        id='year-slider'
    ),
        ],
        class_name ="py-4 my-2"                 #py padding top and bottom
    ),
     #width="auto",
     #class_name="mx-0"                         #mx margin left and right
     ),
             
    dbc.Container(
    dbc.Row([
        html.Div("Secteur de l'ETF par poids",className ="py-4"),
        dbc.Col( 
            #dbc.Container([
                            dash_table.DataTable(
                            data= sectorweight('CSSPX.MI').to_dict('records'),
                            #columns=[{"name": i, "id": i} for i in sectorweight('CSSPX.MI').columns],
                            id='sect_weight', 
                            style_cell={'padding': '5px'},
                                style_header={
                                'backgroundColor': 'dark',
                                'fontWeight': 'bold'
                                },
                            ),
            #]),
        md=4
        ),  
         

        dbc.Col( 
                    dbc.Container([
                        dash_table.DataTable(
                        data= data_holding('CSSPX.MI').to_dict('records'),
                        #columns=[{"name": i, "id": i} for i in sectorweight('CSSPX.MI').columns],
                        id='holding_stocks', 
                        style_cell={'padding': '5px',
                                    'aligne':'center'},
                        style_header={
                            'backgroundColor': 'dark',
                            'fontWeight': 'bold'
                        },
                        )
        
                    ]),
        md=6
        ),
    ],
    justify ='center',
    ),
    class_name ="bg-light py-4 my-2 fluid"
    ),
    
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig3,
        style={"height": "100%","width": "100%"}
    ),

    dcc.Graph(
        id='ind-graph',
        figure=fig_indices,
        style={"height": "100%","width": "100%"}
    ),
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

# @app.callback(
#     Output('example-graph2', 'figure'),
#     Input('xaxis-column', 'value'),
#     )
# def update_figure_candelstick(xaxis_column_name):
#     filtered_df2 = all_ETF_data[all_ETF_data['Ticker_ya'] == xaxis_column_name]

#     fig_candel = go.Figure(data=[go.Candlestick(x=filtered_df2['Date'],
#                 open=filtered_df2['Open'],
#                 high=filtered_df2['High'],
#                 low=filtered_df2['Low'],
#                 close=filtered_df2['Close'])])

#     fig_candel.update_layout(transition_duration=200,height=800,xaxis_rangeslider_visible=True)
    
#     return fig_candel    



@app.callback(
    Output('etf_lg_name', 'children'),
    Input('xaxis-column', 'value')
)
def update_output_div(input_value):
    if input_value:

        ETF_name= extract_ETF_info(input_value)
        #logging.warning(input_value)
        #logging.warning(ETF_name.longName[0])
        ETF_lg_name=ETF_name.longName[0]
        return ETF_lg_name

    

@app.callback(
    Output('etf_lg_businessSummary', 'children'),
    Input('xaxis-column', 'value')
)
def update_output_div(input_value):
    if input_value:
        ETF_name= extract_ETF_info(input_value)
        #logging.warning(input_value)
        #logging.warning(ETF_name.longName[0])
        ETF_lg_businessSummary=ETF_name.longBusinessSummary[0]
        return ETF_lg_businessSummary
    


@app.callback(
   Output('sect_weight', 'data'),
    Input('xaxis-column', 'value'))
def update_table(input_value):
    if input_value:
        ETF_name_sectorweight=sectorweight(input_value).to_dict('records')
        #columns= [{"name": i, "id": i} for i in sectorweight(input_value).columns],
        return ETF_name_sectorweight


@app.callback(
   Output('holding_stocks', 'data'),
    Input('xaxis-column', 'value'))
def update_table(input_value):
    if input_value:
        ETF_holding=data_holding(input_value).to_dict('records')
        #columns= [{"name": i, "id": i} for i in sectorweight(input_value).columns],
        return ETF_holding        

if __name__ == '__main__':
    app.run_server(debug=True)