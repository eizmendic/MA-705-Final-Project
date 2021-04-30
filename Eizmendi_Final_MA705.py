#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:49:28 2021

@author: franco
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime


site= "http://api.currencylayer.com/live?access_key=a7d0b5ce71984ed7b433f6a5e59ef25a&format=1"


forexrates = requests.get(site)
forexrates.raise_for_status()
currency = forexrates.json()
forex = currency['quotes']
forex = pd.Series(forex)
forex = pd.DataFrame(forex)
forex.reset_index(inplace=True)
forex.columns =['Currencies','Rate']
forex['Currencies'] = forex['Currencies'].map(lambda x: x[3:6])
ts = int(currency['timestamp'])
GMT = (datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')), "GMT"

list = "http://api.currencylayer.com/list?access_key=a7d0b5ce71984ed7b433f6a5e59ef25a"

forexlist = requests.get(list)
forexlist.raise_for_status()
forexlist = forexlist.json()
forexlist = forexlist['currencies']
forexlist = pd.Series(forexlist)
forexlist = pd.DataFrame(forexlist)
forexlist.reset_index(inplace=True)
forexlist.columns =['Currencies','Longname']

forexcombined = forex.merge(forexlist, left_on='Currencies', right_on='Currencies')
forexcombined['Fname']=forexcombined['Currencies']+'-'+forexcombined['Longname']
forexcombined = pd.DataFrame(forexcombined)


history = pd.read_csv('Currencyhist.csv')

fig = px.line(history, y=history.columns[1:11], x='Dates')

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)


app.layout = html.Div([
    html.H1('Convert USD to other currencies',
            style={'textAlign' : 'center','color':'green','font-size':'70px'}),
     html.H2('Franco Eizmendi, MA705 - Bentley University, April 2021',
            style={'textAlign' : 'left','color':'blue','font-size':'30px'}),
      html.H2('Rates as of:',
            style={'textAlign' : 'center','color':'black','font-size':'18px'}),
     html.H2(GMT,'Time Stamp of data collected:',
            style={'textAlign' : 'center','color':'black','font-size':'18px'}),
     html.A('Information Source: currencylayer.com- API',
         href='http://api.currencylayer.com/',
          target='_blank'),
     html.P([html.Br(), 'Select Currency to be converted to:']),
     dcc.Dropdown(
    id='dropdown', options=[
        {'label': i, 'value': i} for i in forexcombined.Fname.unique()
    ], multi=False, placeholder='Select Currency...'),
    html.Div(id='tablecontainer'),
    html.H2('Enter USD ($) to be converted:',
            style={'textAlign' : 'left','color':'black','font-size':'18px'}),
    dcc.Input(
    placeholder='USD ($)',type='number',value='', id='IUSD') , 
    html.Div (id='HUSD'),
    html.H2('Conversion:',
            style={'textAlign' : 'left','color':'black','font-size':'18px'}),
    html.Div(id='conversion_box'), 
    html.Br(),
    html.Br(),
    html.Br(),
    html.H4('Historical Values for Major Currencies Against the USD',
            style={'textAlign' : 'center','color':'green','font-size':'50px'}),
    html.Br(),
    html.A('Information Source: ofx.com',
         href='https://www.ofx.com/en-us/forex-news/historical-exchange-rates/',
          target='_blank'),
    html.Br(),
    dcc.Graph(figure=fig, id='moneyplot'),
    html.Div([html.H4('Select Currency to Display:'),
              dcc.Checklist(
                  options=[{'label': 'AUD - Australian Dollar ', 'value': 'AUD'},
                           {'label': 'EUR - Euro', 'value': 'EUR'},
                           {'label': 'GBP - British Pound', 'value': 'GBP'},
                           {'label': 'JPY - Japnese Yen', 'value': 'JPY'},
                           {'label': 'BRL - Brazilian Rial', 'value': 'BRL'},
                           {'label': 'ZAR - South Africa Rand', 'value': 'ZAR'},
                           {'label': 'MXP - Mexican Peso', 'value': 'MXP'},
                           {'label': 'CAD - Canadian Dollar', 'value': 'CAD'},
                           {'label': 'AED - UAE Dirham', 'value': 'AED'},
                           {'label': 'CNY - Chinese Yuan Renminbi', 'value': 'CNY'}],
                  value=['EUR'],
                  id = 'currency_checklist')],
             style={'width':'49%'}),
    html.Div(id='graph_div')
    ])

@app.callback(
    Output(component_id="moneyplot", component_property="figure"),
    [Input(component_id="currency_checklist", component_property="value")]
)
def update_graph(money):
    fig = px.line(history, y=money, x='Dates')
    return fig
     

@app.callback(
    Output(component_id='conversion_box', component_property='children'),
    [Input(component_id='dropdown',component_property='value')]
     )
def update_div(Converted):
    new = forexcombined[forexcombined['Fname'] == 'dropdown'][['Rate']]
    new1 = new['Rate']
    return new1 * 'IUSD'

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
    
