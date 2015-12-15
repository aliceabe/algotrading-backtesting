"""SimpleRule.py"""
from pyspark import SparkContext
import os

def simpleRule(dataPoint):
	global canbuy
	global nbshares
	global capital
	global code
	if dataPoint[1] < t_buy and canbuy:
		nbshares = int( capital / dataPoint[1] )
		capital = 0
		canbuy = False
	elif dataPoint[1] > t_sell and not canbuy:
		capital = nbshares * dataPoint[1]
		nbshares = 0
		canbuy = True
	current = capital + nbshares * dataPoint[1] - 1000
	with open("/home/alice/Documents/algotrading-backtesting/quantquote_daily_sp500_83986/profits/" + code + ".csv", "a") as myfile:
		myfile.write(dataPoint[0] + ',' + str(current) + '\n')

sc = SparkContext("local", "SimpleRule")
for filename in os.listdir('/home/alice/Documents/algotrading-backtesting/quantquote_daily_sp500_83986/quotes'):

	try:
		code = filename.split('_')[1].split('.')[0]
		canbuy = True
		nbshares = 0
		capital = 1000

		quoteFile = "/home/alice/Documents/algotrading-backtesting/quantquote_daily_sp500_83986/quotes/" + filename
		quoteData = sc.textFile(quoteFile).cache()

		rdd = quoteData.map(lambda line: line.split(',')).map(lambda x: (x[0], (float(x[2])+float(x[5]))/2))
		rddValues = rdd.map(lambda tuple: tuple[1])

		low = rddValues.reduce(lambda a, b: a if (a<b) else b)
		high = rddValues.reduce(lambda a, b: a if (a>b) else b)
		mean = rddValues.mean()
		stdev = rddValues.stdev()

		t_buy = max(mean - stdev, low)
		t_sell = min(mean + stdev, high)

		rdd.foreach(simpleRule)

	except:
		print filename







