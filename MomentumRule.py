"""SimpleRule.py"""
from pyspark import SparkContext
import os

#path = '/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/'
path = '/home/alice/Documents/algotrading-backtesting/'

def simpleRule(dataPoint):
	global canbuy
	global nbshares
	global capital
	global code
	global last	
	global decreasing	

	if dataPoint[1] > last and canbuy and decreasing:
		nbshares = int( capital / dataPoint[1] )
		capital = 0
		canbuy = False
		decreasing = False
	elif dataPoint[1] < last and not canbuy and not decreasing:
		capital = nbshares * dataPoint[1]
		nbshares = 0
		canbuy = True
		decreasing = True
	current = capital + nbshares * dataPoint[1] - 1000
	with open(path + "quantquote_daily_sp500_83986/profits_2/" + code + ".csv", "a") as myfile:
		myfile.write(dataPoint[0] + ',' + str(current) + '\n')
	last = dataPoint[1]

sc = SparkContext("local", "SimpleRule")
for filename in os.listdir(path + 'quantquote_daily_sp500_83986/quotes'):

	try:
		window_length = 50
		code = filename.split('_')[1].split('.')[0]
		canbuy = True
		nbshares = 0
		capital = 1000
		#count = 0
		#t_buy = 0
		#t_sell = 0
		#window = [0 for i in range(0,window_length)]	
		last = 0	
		decreasing = True

		quoteFile = path + "quantquote_daily_sp500_83986/quotes/" + filename
		quoteData = sc.textFile(quoteFile).cache()

		rdd = quoteData.map(lambda line: line.split(',')).map(lambda x: (x[0], (float(x[2])+float(x[5]))/2))
		rddValues = rdd.map(lambda tuple: tuple[1])

		#t_buy = max(mean - stdev, low)
		#t_sell = min(mean + stdev, high)

		rdd.foreach(simpleRule)

	except:
		print filename
