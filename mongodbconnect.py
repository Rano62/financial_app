import pandas as pd
import yfinance as yf
import datetime
from datetime import date
import dns
from pymongo import MongoClient
from pandas import DataFrame
from mongopw import username, passw

ETF_tickers=['CSSPX.MI','IWDA.AS','EMIM.AS','IEAC.L','CSNDX.MI','IMEU.AS','INRG.MI','SEMB.L','EXW1.DE','IWVL.MI','IHYG.MI']

# find today and yesterday
today = date.today()
yesterday=today - datetime.timedelta(days=1)

#connect to mongo db atlas

client = MongoClient("mongodb+srv://{}:{}@cluster0.fogd9.mongodb.net/test?retryWrites=true&w=majority".format(username,passw))
dbs = client.list_database_names()
print(dbs)