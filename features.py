"""
This file contains features to be constructed and used.
Inputs are all df datasets, outputs are all feature series.
"""

def get_features():
    return ['Return', 'Rela_volume']

def Return(df):
    close = df['Close']
    return np.log(close).diff() # log return

# relative volume
def Rela_volume(df):
    volume = df['']