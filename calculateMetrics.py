import os
import csv
import json
import math

for filename in os.listdir('/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/quantquote_daily_sp500_83986/profits'):
	returns = []
	print filename
	with open("/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/quantquote_daily_sp500_83986/profits/" + filename, "r") as myfile:	
		reader = csv.reader(myfile)
		for row in reader:
			returns.append(float(row[1]))		
	mean = float(sum((returns)))/len(returns)
	std = map(lambda x: (x - mean)**2,returns)
	std = sum(std)/len(std)
	max_val = max(returns)
	min_val = min(returns)
	max_drawdown = 0
	if(max_val != 0):
		max_drawdown = (max_val - min_val)/max_val
	sharpe = [0 for x in range(0,len(returns))]
	if(max_val != 0):
		sharpe = map(lambda x : (x/std) * math.sqrt(365.35), returns)
	
	dict = {}
	dict["Mean"] = mean
	dict["Std"] = std
	dict["Max Drawdown"] = max_drawdown
	dict["Sharpe Ratio"] = sharpe

	code = filename.split(".")[0]	
	with open('/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/json/metrics/' + code.upper() + ".csv", 'w') as outfile:
		json.dump(dict,outfile)

