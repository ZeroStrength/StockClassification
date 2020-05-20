from sklearn.cluster import KMeans
import numpy as np
import pandas_datareader as pdr
import pandas as pd

# Documentation from
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

def get_macd(df, short=5, long=20, t=9):
    # 입력받은 값이 dataframe이라는 것을 정의해줌
    df = pd.DataFrame(df)
    # MACD 관련 수식
    ma_12 = df.Close.ewm(span=12).mean() # 단기(12) EMA(지수이동평균)
    ma_26 = df.Close.ewm(span=26).mean() # 장기(26) EMA
    macd = ma_12 - ma_26 # MACD
    macds = macd.ewm(span=t).mean() # Signal
    macdo = macd - macds # Oscillator
    
    df = df.assign(macd=macd, macds=macds, macdo=macdo).dropna()
    
    return df

def fnMACD(m_Df, m_NumFast=12, m_NumSlow=26, m_NumSignal=9):
    m_Df['EMAFast'] = m_Df['Close'].ewm( span = m_NumFast, min_periods = m_NumFast - 1).mean()
    m_Df['EMASlow'] = m_Df['Close'].ewm( span = m_NumSlow, min_periods = m_NumSlow - 1).mean()
    m_Df['MACD'] = m_Df['EMAFast'] - m_Df['EMASlow']
    m_Df['MACDSignal'] = m_Df['MACD'].ewm( span = m_NumSignal, min_periods = m_NumSignal-1).mean()
    m_Df['MACDDiff'] = m_Df['MACD'] - m_Df['MACDSignal']
    return m_Df

# 1. Get array data (KOSPI Top 100)
# 1.1. Get code list
code_list = pd.read_csv('data/kospi_100.csv')
code_list = list(code_list["code"])

def addZeroToCode(code):
    code = str(code)
    return '0'*(6-len(code))+code

X = np.array([])

for code in code_list:
    code = addZeroToCode( code )
    p = pdr.get_data_yahoo( code+'.KS', start='2020-03-01', end='2020-05-20' )
    print( fnMACD( p ))
    break


print( X )

# Calculate MACD 5 (X), MACD 20 (Y)
# kmeans = KMeans(n_clusters=8, random_state=0, verbose=1).fit(X)


# print( kmeans.labels_ )

# print( kmeans.predict([[0, 0], [12, 3]]) )

# print( kmeans.cluster_centers_ )


