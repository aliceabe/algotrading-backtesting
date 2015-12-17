import os
import csv
import json
import math

for filename in os.listdir('/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/quantquote_daily_sp500_83986/profits_2'):
	returns = []
	print filename
	with open("/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/quantquote_daily_sp500_83986/profits_2/" + filename, "r") as myfile:	
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
	if(max_val != 0):
		sharpe = map(lambda x : (x-1000/1000) , returns)
		sharpe = map(lambda x : (x - (0.05**(1/12))), sharpe)
		mean_excess = sum(sharpe)/len(sharpe)
		std_excess = map(lambda x: (x - mean_excess)**2,sharpe)
		std_excess = sum(std_excess)/len(sharpe)
		sharpe = mean_excess/std_excess
	dict = {}
	dict["Mean"] = mean
	dict["Std"] = std
	dict["Max Drawdown"] = max_drawdown
	dict["Sharpe Ratio"] = sharpe

	code = filename.split(".")[0]	
	with open('/Users/akshaankakar/Desktop/Big_Data_Analytics/Final/json/metrics_2/' + code.upper() + ".csv", 'w') as outfile:
		json.dump(dict,outfile)

