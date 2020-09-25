"""
This file is used for feature normalization.
"""
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import RobustScaler

def normalize_feature(df_features, test_start='2020-01-01', alpha=0.05):
    """
    alpha: the percentile to be clipped.
    """
    trainset = df_features[df_features.index < test_start]
    testset = df_features[df_features.index >= test_start]
    
    scaler = RobustScaler()
    norm_train = scaler.fit_transform(trainset)
    norm_test = scaler.transform(testset)

    lower = np.nanpercentile(norm_train, 100*alpha, axis=0)
    upper = np.nanpercentile(norm_train, 100*(1-alpha), axis=0)
    
    norm_features = np.concatenate([norm_train, norm_test], axis=0)
    norm_features = pd.DataFrame(norm_features, index=df_features.index, columns=df_features.columns)
    norm_features.clip(lower, upper, axis=1, inplace=True)

    return norm_features

def get_norm_feature_and_label(df_features, df, test_start='2020-01-01', alpha=0.05, predict_horizon=7):
    """
    predict_horizon: 7 means predict next 7-day return.
    """
    norm_features = normalize_feature(df_features, test_start, alpha)
    labels = np.log(df['Close'].shift(-predict_horizon)  / df['Close'])
    norm_features['label'] = labels 
    
    return norm_features.dropna()