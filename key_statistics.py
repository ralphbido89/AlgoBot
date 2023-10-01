import requests
from bs4 import BeautifulSoup
import pandas as pd


tickers = ["AAPL", "META", "CSCO"]
key_statistics = {}

for ticker in tickers:

    url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker, ticker)
    
    
    headers = {"User-Agent" : "Chrome/117.0.5938.92"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    table = soup.find_all("table", {"class" : "W(100%) Bdcl(c)"})
    
    temp_stats = {}
    for t in table:
        rows = t.find_all("tr")
        for row in rows:
            temp_stats[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[-1]
    key_statistics[ticker] = temp_stats