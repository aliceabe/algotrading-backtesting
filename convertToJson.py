import csv
import time
import json
import os

names = {}
with open('symbol_map_comnam.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		try:
			names[row[0]] = row[2]
		except:
			print row

for filename in os.listdir('quantquote_daily_sp500_83986/quotes'):

	try:
		code = filename.split('_')[1].split('.')[0]
		name = names[code]

		result = []
		
		with open('quantquote_daily_sp500_83986/quotes/' + filename , 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				ts = int(time.mktime(time.strptime(row[0], '%Y%m%d'))) * 1000
				val = (float(row[2]) + float(row[5])) / 2
				result.append([ts, round(val, 2)])

		with open('json/quotes/' + code.upper() + '.json', 'wb') as f:
			json.dump(result, f)

	except:
		print filename