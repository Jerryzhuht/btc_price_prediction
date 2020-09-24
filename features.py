"""
This file contains features to be constructed and used.
Inputs are all df datasets, outputs are all feature series.
"""
import pandas as pd 
import numpy as np


def get_features():
    return ['Return', 'Rela_volume', 'HdL', 'Rvol', 'MACD', 'vix', 'snp_return', 'gold_return', 'yield_10y']

def Return(df):
    close = df['Close']
    return np.log(close).diff() # log return

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

def Rela_volume(df, window=30):
    volume = df['Volume']
    mean_vol = volume.rolling(window).mean()
    return np.log(volume / mean_vol)

# high/low
def HdL(df):
    return np.log(df['High'] / df['Low'])

# log(realized vol) = log(sum daily ret**2)
def Rvol(df, window=7):
    ret = Return(df)
    variance = ret ** 2
    return np.log(variance.rolling(window).sum())

# MACD
def MACD(df, fast=5, slow=12):
    short_term = df['Close'].rolling(fast).mean()
    long_term = df['Close'].rolling(slow).mean()
    return np.log(short_term/long_term)

def feature_generator(df):
    features = get_features()
    df_feature = pd.DataFrame()
    for feature in features:
        df_feature[feature] = globals()[feature](df)
    return df_feature
