from pymongo import MongoClient
from pandas import DataFrame
from mongopw import username, passw
from ETF_tickers import ETF_tickers
import pandas as pd


client = MongoClient("mongodb+srv://{}:{}@cluster0.fogd9.mongodb.net/test?retryWrites=true&w=majority".format(username,passw))
dbs = client.list_database_names()
#print(dbs)

#selectionne la datbase ETF
database = client['ETF']
#selectionne la collection ETF
ETF_info = database.get_collection("Info")   

def extract_ETF_info(ETF_symbol):
   # for i in ETF_tickers:
        x   = []
        cur=ETF_info.find({'symbol': ETF_symbol})
        for j in cur:
            x.append(j)
        df = pd.DataFrame (x)
        return df

data_ETF_info=extract_ETF_info('CSSPX.MI') 

def sectorweight(ETF_symbol):
  data_ETF_info=extract_ETF_info(ETF_symbol)#('sectorWeightings')
  datasector=data_ETF_info['sectorWeightings'][0]
  sector_list=[]

  for item in datasector:
    
    for i,j in item.items():
      sector_list.append(tuple([i, j]))

  sect=pd.DataFrame(sector_list,columns=['sector','weight']) 
  sect['weight'] = sect['weight'].multiply(100)
  sect_weight=sect.sort_values(by=['weight'],ascending=False).round(2) 
  return sect_weight


def data_holding(ETF_symbol):
  data=extract_ETF_info(ETF_symbol)
  dataholding=data["holdings"][0]
  pd_dataholding=pd.DataFrame(dataholding)
  pd_dataholding['holdingPercent']=pd_dataholding['holdingPercent'].multiply(100)
  stocks_hold=pd_dataholding.sort_values(by=['holdingPercent'],ascending=False).round(2)
  return stocks_hold  