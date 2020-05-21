from sklearn.cluster import KMeans
import numpy as np
import pandas_datareader as pdr
import pandas as pd
from pykrx import stock

# Documentation from
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

def fnMACD(m_Df, m_NumFast=12, m_NumSlow=26, m_NumSignal=9):
    m_Df['EMAFast'] = m_Df['종가'].ewm( span = m_NumFast, min_periods = m_NumFast - 1).mean()
    m_Df['EMASlow'] = m_Df['종가'].ewm( span = m_NumSlow, min_periods = m_NumSlow - 1).mean()
    m_Df['MACD'] = m_Df['EMAFast'] - m_Df['EMASlow']
    m_Df['MACDSignal'] = m_Df['MACD'].ewm( span = m_NumSignal, min_periods = m_NumSignal-1).mean()
    m_Df['MACDDiff'] = m_Df['MACD'] - m_Df['MACDSignal']
    return m_Df

def fnRSI(m_Df, m_N):
    
    U = np.where(m_Df.diff(1) > 0, m_Df.diff(1), 0)
    D = np.where(m_Df.diff(1) < 0, m_Df.diff(1) *(-1), 0)

    AU = pd.DataFrame(U).rolling( window=m_N, min_periods=m_N).mean()
    AD = pd.DataFrame(D).rolling( window=m_N, min_periods=m_N).mean()
    RSI = AU.div(AD+AU) *100
    return RSI

# 1. Get array data (KOSPI Top 100)
# 1.1. Get code list
code_list = pd.read_csv('data/kospi_100.csv')
name_list = list(code_list["name"])
code_list = list(code_list["code"])


def addZeroToCode(code):
    code = str(code)
    return '0'*(6-len(code))+code

A = []

for code in code_list:
    code = addZeroToCode( code )
    p = stock.get_market_ohlcv_by_date("20200401", "20200520", code)
    macd = fnMACD( p ).iloc[-1][-2]
    rsi = fnRSI( p, 12 ).iloc[-1][3]

    A.append( [macd,rsi] )

A = np.array(A)

# Calculate MACD 5 (X), MACD 20 (Y)
kmeans = KMeans(n_clusters=4, random_state=0).fit(A)

labels = kmeans.labels_

# match labels with stock name

result = {}

for i in range(len( labels) ):
    label = str(labels[i])

    if label in result.keys():
        result[label].append( name_list[i] )
    else:
        result[label] = [name_list[i]]

w = open('data/cluster_result.txt', 'w')

for key in result.keys():
    print("===" + key + "===")
    print(result[key])
    print()

    w.write(key+'\n')
    w.write(str(result[key])+'\n\n')

w.close()


#print( kmeans.predict([[0, 0], [12, 3]]) )
#print( kmeans.cluster_centers_ )


