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