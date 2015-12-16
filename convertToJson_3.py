import csv
import time
import json
import os

for filename in os.listdir('quantquote_daily_sp500_83986/profits_2'):

	try:
		code = filename.split('.')[0]

		result = {'pos': [], 'neg': []}
		
		with open('quantquote_daily_sp500_83986/profits/' + filename , 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				ts = int(time.mktime(time.strptime(row[0], '%Y%m%d'))) * 1000
				val = float(row[1])
				if val > 0:
					result['pos'].append([ts, round(val, 2)])
					result['neg'].append([ts, 0])
				else:
					result['pos'].append([ts, 0])
					result['neg'].append([ts, round(val, 2)])

		with open('json/profits_2/' + code.upper() + '.json', 'wb') as f:
			json.dump(result, f)

	except:
		print filename

