from pymongo import MongoClient
from pandas import DataFrame
from mongopw import username, passw
from ETF_tickers import ETF_tickers
import pandas as pd


client = MongoClient("mongodb+srv://{}:{}@cluster0.fogd9.mongodb.net/test?retryWrites=true&w=majority".format(username,passw))
dbs = client.list_database_names()
#print(dbs)

#select database ETF
database = client['ETF']
#select collection ETF
ETF_collection = database.get_collection("ETF")

def extract_ETF_cours(ETF_list):
    x   = []
    cur=ETF_collection.find({ "Ticker_ya": ETF_list })
    for i in cur:
        x.append(i)

    df = pd.DataFrame (x)

    del df["_id"]


    df_dateind=df.set_index('Date')

    df_sorted =df_dateind.sort_index(ascending=False)

    return df_sorted