"""
This file contains features to be constructed and used.
Inputs are all df datasets, outputs are all feature series.
"""
import pandas as pd
import numpy as np

def get_features():
    return ['Return', 'Rela_volume', 'vix', 'snp_return', 'gold_return', 'yield_10y']

def Return(df):
    close = df['Close']
    return np.log(close).diff() # log return

# relative volume
def Rela_volume(df):
    volume = df['']
    
def vix(df):
    return np.log(df['VIX'])

def snp_return(df):
    r = df['S&P Close']
    return np.log(r).diff() # log return
                  
def gold_return(df):
    r = df['Gold Close']
    return np.log(r).diff() # log return

def yield_10y(df):
    return df['10y Treasury Yield']

