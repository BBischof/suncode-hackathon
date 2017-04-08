import datetime

# May 1 to Oct 31
summer_tou = {'weekday':{'0.0,30600':0.202, '30600.00001,43200':0.230, '43200.00001,64800':0.253, '64800.00001,77400':0.230, '77400.00001,86400.0':0.202}, 'weekend':{'0.0,86400.0':0.202}}

# Nov 1 to Mar 30
winter_tou = {'weekday':{'0.0,30600':0.2, '30600.00001,77400':0.22, '77400.00001,86400':0.2},'weekend':{'0.0,86400':0.2}}

day_week_tou = {'sat':tou['weekend'],'sun':tou['weekend'],'mon':tou['weekday'], 'tue':tou['weekday'],'wed':['weekday'],'thu':['weekday'],'fri':['weekday']}



def date_tou_rate(t):
	'''if passing t as a string
    t = datetime.strptime(timestamp, '%d %m %Y %H:%M:%S')'''
	seconds = float(t.hour*3600 + t.minute*60 + t.second)
	if t.month >= 5 and t.month <= 10:
		if t.weekday() in range(5):
			return summer_tou['weekday'][summer_tou['weekday'].keys()[[(lambda x: 1 if seconds>=x[0] and seconds<x[1] else 0)(x) for x in [(float(key.split(',')[0]), float(key.split(',')[1])) for key in summer_tou['weekday'].keys()]].index(1)]]
		else: 
			return 0.202
	else:
		if t.weekday() in range(5):
			return winter_tou['weekday'][winter_tou['weekday'].keys()[[(lambda x: 1 if seconds>=x[0] and seconds<x[1] else 0)(x) for x in [(float(key.split(',')[0]), float(key.split(',')[1])) for key in winter_tou['weekday'].keys()]].index(1)]]
		else:
			return 0.2