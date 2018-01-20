# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 02:46:14 2017

@author: Anurag
"""
import os
import time
import gdax
import pandas as pd
from pandas import HDFStore
import numpy as np

#os.getcwd()
os.chdir('D:\Math Finance\ETH data')

public_client = gdax.PublicClient()

last_ti=0
j=0
for i in range(0,30000):
    try:
        order_book = public_client.get_product_order_book('ETH-USD', level=3)
        current_price = public_client.get_product_ticker(product_id='ETH-USD')
#        if current_price['trade_id'] == last_ti:
#            pass
#        else:
        j=j+1
        cp = float(current_price['price'])
        ct = current_price['time']
        cv = float(current_price['volume'])
        ask = pd.DataFrame(order_book['asks'], columns=['price', 'volume', 'id'])
        bid = pd.DataFrame(order_book['bids'], columns=['price', 'volume', 'id'])
        ob = ask.sort_index(axis=0,ascending = False).append(bid, ignore_index=True)
        ob = ob.loc[:,['price','volume']]
        ob[['price','volume']] = ob[['price','volume']].apply(pd.to_numeric)
        ob['price_percent'] = ob['price']/cp - 1
        ob['current_price'] = cp
        ob['current_time'] = ct
        ob['current_volume'] = cv
        ob['i'] = i
        ob['j'] = j
        df = ob[abs(ob.price_percent) <= 0.01]
        df = df.reset_index(drop=True)
        print('Done: ' + str(i))
        if i==0:
            hdf = HDFStore('storage5.h5')
            hdf.put('d5', df, format='table', data_columns=True)
        else:
            hdf.append('d5', df, format='table', data_columns=True)   
        last_ti = current_price['trade_id']
        time.sleep(3)
    except:
        time.sleep(10)
        pass
hdf.close() # closes the file

from pandas import read_hdf
# this query selects the columns A and B
# where the values of A is greather than 0.5
df = read_hdf('storage5.h5', 'd5')



df=df.reset_index(drop=True)


a= df.loc[:,('i','current_time', 'current_price')]

ab = a.drop_duplicates()
abc = ab['current_price']
abc.plot()

a.shape
a=pd.DataFrame(a)
df.shape
a.to_excel('outpuuuu.xlsx', header=True, index=False)
print('Finished!')
