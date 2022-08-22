import yfinance as yf
import datetime
from datetime import date
import pymongo
import dns
from pymongo import MongoClient
import pandas as pd


from mongopw import username, passw
from indice_ticker import indices_tickers


# find today and yesterday
today = date.today()
yesterday=today - datetime.timedelta(days=1)

#connect to mongo db atlas
client = MongoClient("mongodb+srv://{}:{}@cluster0.fogd9.mongodb.net/test?retryWrites=true&w=majority".format(username,passw))


#select database ETF
database = client['ETF']
#select collection ETF
ETF_collection = database.get_collection("Indices")

#empty list
x   = []
#find one ETF and add data to list x
cur=ETF_collection.find({ "Ticker_ya": "^DJI" })
for i in cur:
    x.append(i)

#change list to pandadataframe
df = pd.DataFrame (x)

#delete mongodb automatically added index
del df["_id"]

#define new index (date)
df_dateind=df.set_index('Date')
#sort index
df_sorted =df_dateind.sort_index(ascending=False)

#look at the most recent date
most_recent_date = df['Date'].max()

#add one day
most_recent_date_plus_one = most_recent_date+ datetime.timedelta(days=1)

startdate=most_recent_date_plus_one.date()

# télécharge l'historique recent en fonction des dates déjà présentes dans la base
df_histo =yf.download(indices_tickers, start=startdate, end=today)

df_histo
n = 1
  
df_histo.drop(df_histo.tail(n).index, 
        inplace = True) 


df_hi=df_histo.stack(level=-1)
df_hi.reset_index(inplace=True)
df_hi.rename(columns={'level_1': 'Ticker_ya'}, inplace=True)

df_hi_json = df_hi.to_dict("records")

#insert histo in pymongo

#selectionne la datbase ETF
database = client['ETF']
#selectionne la collection ETF
Indice_collection = database.get_collection("Indices")

Indice_collection.insert_many(df_hi_json)