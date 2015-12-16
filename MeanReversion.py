"""SimpleRule.py"""
from pyspark import SparkContext
import os

def simpleRule(dataPoint):
	global canbuy
	global nbshares
	global capital
	global code
	global count
        global window
        global t_buy
        global t_sell
	global window_length

	if count < window_length-1:
		window[count] = dataPoint[1]
		count += 1
	else :
	
		window[count % window_length] = dataPoint[1]
	        mean = sum(window)/window_length
                std = map(lambda x: (x-mean)**2,window)
                std = sum(std)/window_length
                t_buy = mean - 2*std
                t_sell = mean + 2*std

		if dataPoint[1] < t_buy and canbuy:
			nbshares = int( capital / dataPoint[1] )
			capital = 0
			canbuy = False
		elif dataPoint[1] > t_sell and not canbuy:
			capital = nbshares * dataPoint[1]
			nbshares = 0
			canbuy = True
		current = capital + nbshares * dataPoint[1] - 1000
		with open("/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/quantquote_daily_sp500_83986/profits/" + code + ".csv", "a") as myfile:
			myfile.write(dataPoint[0] + ',' + str(current) + '\n')
		count += 1

sc = SparkContext("local", "SimpleRule")
for filename in os.listdir('/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/quantquote_daily_sp500_83986/quotes'):

	try:
		window_length = 50
		code = filename.split('_')[1].split('.')[0]
		canbuy = True
		nbshares = 0
		capital = 1000
		count = 0
		t_buy = 0
		t_sell = 0
		window = [0 for i in range(0,window_length)]	
		

		quoteFile = "/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/quantquote_daily_sp500_83986/quotes/" + filename
		quoteData = sc.textFile(quoteFile).cache()

		rdd = quoteData.map(lambda line: line.split(',')).map(lambda x: (x[0], (float(x[2])+float(x[5]))/2))
		rddValues = rdd.map(lambda tuple: tuple[1])

		#low = rddValues.reduce(lambda a, b: a if (a<b) else b)
		#high = rddValues.reduce(lambda a, b: a if (a>b) else b)
		#mean = rddValues.mean()
		#stdev = rddValues.stdev()

		#t_buy = max(mean - stdev, low)
		#t_sell = min(mean + stdev, high)

		rdd.foreach(simpleRule)

	except:
		print filename
