#! python
# Command: python get_stock.py $1
# Variables: $1 = file of symbols

import csv
import pandas as pd
import yfinance as yf
import time
import sys
#import pprint

tic = time.time()
file = sys.argv[1]

symbol_list = []
with open(file, newline='') as f:
	for row in csv.reader(f):
		symbol_list.append(row[0])

df = pd.DataFrame(
	columns=[
		'Symbol',
		'Sector',
		'Industry',
		'Price',
		'Price_to_Book',
		'Beta',
		'Div_Yield',
		'Div_Rate',
		'Payout_Ratio',
		'Trailing_1Y_Div_Yield'
	]
)

nf = 0
nf_list = []
for i in symbol_list:
	ticker = yf.Ticker(i)
	print("Gathering info for " + i.upper() + "...")
	
	try:
		ticker_symbol = ticker.info.get('symbol')
	except:
		print("NOT FOUND")
		nf = nf + 1
		nf_list.append(i)
		continue
	
	ticker_sector = ticker.info.get('sector')
	ticker_industry = ticker.info.get('industry')
	ticker_price = ticker.info.get('regularMarketPrice')
	ticker_book = ticker.info.get('priceToBook')
	ticker_beta = ticker.info.get('beta')
	ticker_div_yield = ticker.info.get('dividendYield')
	ticker_div_rate = ticker.info.get('dividendRate')
	ticker_payout = ticker.info.get('payoutRatio')
	ticker_trail_yield = ticker.info.get('trailingAnnualDividendYield')
	ticker_dict = dict({
		'Symbol' : ticker_symbol,
		'Sector' : ticker_sector,
		'Industry' : ticker_industry,
		'Price' : ticker_price,
		'Price_to_Book' : ticker_book,
		'Beta' : ticker_beta,
		'Div_Yield' : ticker_div_yield,
		'Div_Rate' : ticker_div_rate,
		'Payout_Ratio' : ticker_payout,
		'Trailing_1Y_Div_Yield' : ticker_trail_yield
	})
	df = df.append(ticker_dict, ignore_index=True)

df['Yield_to_Cost'] = df['Div_Rate'] / df['Price']

print('Applying filters ...')
indexNames = df[df['Trailing_1Y_Div_Yield'] < .02].index
df.drop(indexNames, inplace=True)

indexNames = df[df['Beta'] > 1.15].index
df.drop(indexNames, inplace=True)

indexNames = df[df['Payout_Ratio'] > 0.6].index
df.drop(indexNames, inplace=True)

indexNames = df[df['Div_Yield'] < 0.034].index
df.drop(indexNames, inplace=True)

indexNames = df[df['Yield_to_Cost'].isnull()].index
df.drop(indexNames, inplace=True)

df.sort_values(by=['Yield_to_Cost'], ascending=False, inplace=True)

print(df)
print("\n" + str(nf) + " symbols were not found:")
print(nf_list)

toc = time.time()
duration = round((toc - tic) / 60,0)
print("\nProcessing took " + str(duration) + " minutes.")