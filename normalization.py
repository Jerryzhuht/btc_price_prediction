"""
This file is used for feature normalization.
"""
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import RobustScaler

def normalize_feature(df_features, test_start):
    trainset = df_features[df_features.index < test_start]
    testset = df_features[df_features.index >= test_start]
    
    scaler = RobustScaler()
    norm_train = scaler.fit_transform(trainset)
    norm_test = scaler.transform(testset)

    norm_features = np.concatenate([norm_train, norm_test], axis=0)
    norm_features = pd.DataFrame(norm_features, index=df_features.index, columns=df_features.columns)

    return norm_features[norm_features.index<test_start], norm_features[norm_features._index>=test_start]
