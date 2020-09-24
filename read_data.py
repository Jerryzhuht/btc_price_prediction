import os 
import pandas as pd 

def read_data(start='2012-01-01', end='2020-09-20', pathname='datasets.h5'):
    path = "../data/" + pathname
    if os.path.exists(path): 
        df = pd.read_hdf(path)
    else:
        df = pd.DataFrame()
        df = data.DataReader("BTC-USD", start=start, end=end, data_source='yahoo')
        df['S&P Close'] = data.DataReader("^GSPC", start=start, end=end, data_source='yahoo')['Adj Close']
        df['Gold Close'] = data.DataReader("GC=F", start=start, end=end, data_source='yahoo')['Adj Close']
        df['VIX'] = data.DataReader("^VIX", start=start, end=end, data_source='yahoo')['Adj Close']
        df['10y Treasury Yield'] = data.DataReader("^TNX", start=start, end=end, data_source='yahoo')['Adj Close']
    return df 