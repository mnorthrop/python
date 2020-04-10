#! python
# Command: python get_div_growth.py $1
# Variables:
# 		$1 = ticker symbol to get dividends and splits

import yfinance as yf
import datetime
import sys

date_now = datetime.datetime.now().strftime('%Y-%m-%d')
date_10ya = (datetime.datetime.now() - datetime.timedelta(days=10*365)).strftime('%Y-%m-%d')
symbol = sys.argv[1]
ticker = yf.Ticker(symbol)

splits = ticker.splits.loc[date_10ya : date_now]
dividends = ticker.dividends.loc[date_10ya : date_now]

print(dividends)
print(splits)