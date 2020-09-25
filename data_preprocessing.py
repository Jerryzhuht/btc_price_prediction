"""
This file is used for data preprecessing, including:
    feature normalization
    tranform data into DL model input
    
"""
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import RobustScaler
from numpy.lib.stride_tricks import as_strided

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
    
    norm_features = normalize_feature(df_features, test_start, alpha)
    labels = np.log(df['Close'].shift(-predict_horizon)  / df['Close'])
    norm_features['label'] = labels 

    return norm_features.dropna()

def get_strided(data, window_len):
    row, col = data.shape
    row_stride, col_stride = data.strides
    return as_strided(
        x=data, 
        shape=(row-window_len+1, window_len, cols), 
        strides=(row_stride, row_stride, col_stride),
        )

def get_x_y(df, y_label, window_x):
    y = df[y_label].values[window_x-1:]
    x = df.drop(labels=y_label, axis=1).values
    return get_strided(x, window_x), y

def get_train_val_test(df, window_x, y_label, val_start='2019-07-01', test_start='2020-01-01'):
    data = {}
    train_end = pd.to_datetime(val_start) + timedelta(days=window_x-1)
    train_df = df.loc[:train_end,:]
    data['train_x'], data['train_y'] = get_x_y(train_df, y_label, window_x)
    val_df = df.loc[val_start:test_start,:]
    data['val_x'], data['val_y'] = get_x_y(val_df, y_label, window_x)
    test_df = df.loc[test_start:,:]
    data['test_x'], data['test_y'] = get_x_y(test_df, y_label, window_x)
    return data