import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN", "MSFT", "GOOG"]

start = dt.datetime.today()-dt.timedelta(20)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohlcv_data = {}


for ticker in stocks:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
    
cl_price.fillna(method='bfill', axis=0, inplace=True)

cl_price.dropna(axis=0, how='any')