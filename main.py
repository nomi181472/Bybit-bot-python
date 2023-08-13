import pandas as pd
from pybit import HTTP
from datetime import datetime
import time
import calendar
session= HTTP(endpoint='',
              api_key="",api_secret="")
while True:
    now=datetime.utcnow()
    unixtime=calendar.timegm(now.utctimetuple())
    since= unixtime-60*60*24*200
    response =session.query_kline(symbol='BTCUSD',interval="D",**{'from':since})
    responseResult=response["result"]
    df=pd.DataFrame(responseResult)
    df=df["close"]

    #macd and signal line calculation
    exp1 =df.ewm(span=12,adjust=False).mean()
    exp2= df.ewm(span=16,adjust=False).mean()

    macd=exp1-exp2
    exp3=macd.ewm(span=9,adjust=False).mean()

    #print("MACD:",macd.iloc[-1])
    #print("Signal",exp3.iloc[-1])

    #check to make recommendation
    test1=exp3.iloc[-2]-macd.iloc[-2]
    test2=exp3.iloc[-1]-macd.iloc[-1]
    call="No trade"
    if(test1<0 and test2>0):
        call="Sell"
    if(test1>0 and test2<0):
        call="Buy"
    print("Trade Recommendation",call)










