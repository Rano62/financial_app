from pymongo import MongoClient
from pandas import DataFrame
from mongopw import username, passw
from indice_ticker import indices_tickers
import pandas as pd


client = MongoClient("mongodb+srv://{}:{}@cluster0.fogd9.mongodb.net/test?retryWrites=true&w=majority".format(username,passw))
dbs = client.list_database_names()
#print(dbs)

#select database ETF
database = client['ETF']
#select collection ETF
Indice_collection = database.get_collection("Indices")

def extract_multi_indices_cours(indices_list):
    for i in indices_tickers:
        x   = []
        cur=Indice_collection.find()
        for j in cur:
            x.append(j)
    df = pd.DataFrame (x)
    del df["_id"]

    df_dateind=df.set_index('Date')

    df_sorted =df_dateind.sort_index(ascending=False)
    #df_sorted =df.sort_index(ascending=False)
    df_sorted_newin=df_sorted.reset_index()
    return df_sorted_newin

all_indices_data=extract_multi_indices_cours(indices_tickers)
#print(all_indices_data.head(10))
   