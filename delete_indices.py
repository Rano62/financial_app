
from read_datahisto_multi import client
from ETF_tickers import ETF_tickers

#select database ETF
database = client['ETF']
#select collection
col = database["Indices"]
#supprimer toutes les entrée de ETF qui sont dans indices
for i in ETF_tickers:
    myquery = { "Ticker_ya": i }

    x = col.delete_many(myquery)