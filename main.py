import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AAPL", "META", "CSCO"]
income_statement_dict = {}
balance_sheet_dict = {}
cashflow_st_dict = {}

for ticker in tickers:
    #scrape income statement
    url = 'https://finance.yahoo.com/quote/{}/financials?p={}'.format(ticker, ticker)
    income_statement = {}
    table_title = {}
    
    
    headers = {"User-Agent" : "Chrome/117.0.5938.92"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    table = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in table:
        heading = t.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            income_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    
    data = pd.DataFrame(income_statement).T
    data.columns = table_title["Breakdown"]
    income_statement_dict[ticker] = data
    
    #scrape balance sheet
    url = 'https://finance.yahoo.com/quote/{}/balance-sheet?p={}'.format(ticker, ticker)
    balance_sheet = {}
    table_title = {}
    
    
    headers = {"User-Agent" : "Chrome/117.0.5938.92"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    table = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in table:
        heading = t.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            balance_sheet[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    
    data = pd.DataFrame(balance_sheet).T
    data.columns = table_title["Breakdown"]
    balance_sheet_dict[ticker] = data
    
    
    #scrape cash flow
    url = 'https://finance.yahoo.com/quote/{}/cash-flow?p={}'.format(ticker, ticker)
    cashflow_statement = {}
    table_title = {}
    
    
    headers = {"User-Agent" : "Chrome/117.0.5938.92"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    table = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in table:
        heading = t.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            cashflow_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    
    data = pd.DataFrame(cashflow_statement).T
    data.columns = table_title["Breakdown"]
    cashflow_st_dict[ticker] = data
    
for ticker in tickers:
    for col in income_statement_dict[ticker].columns:
        income_statement_dict[ticker][col] = income_statement_dict[ticker][col].str.replace(',|-', "")
        income_statement_dict[ticker][col] = pd.to_numeric(income_statement_dict[ticker][col], errors = "coerce")
    