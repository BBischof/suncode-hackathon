''' merge PV production with usage and TOU rates '''
import os
import datetime
import pandas as pd

# May 1 to Oct 31
summer_tou = {'weekday':{'0.0,30600':0.202, '30600.0,43200':0.230, '43200.0,64800':0.253, '64800.0,77400':0.230, '77400.0,86400.0':0.202}, 'weekend':{'0.0,86400.0':0.202}}

# Nov 1 to Mar 30
winter_tou = {'weekday':{'0.0,30600':0.2, '30600.0,77400':0.22, '77400.0,86400':0.2},'weekend':{'0.0,86400':0.2}}

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

def merge_pv_usage(pv_file, bldg_file):
	pv = pd.read_csv('data-sources/{}'.format(pv_file))
	bldg = pd.read_csv('data-sources/{}'.format(bldg_file), header=None)
	bldg.columns = ['date', 'time', 'kw']
	bldg.index = pd.to_datetime(bldg['date'] + ' ' + bldg['time'])
	bldg = bldg.drop(['date', 'time'], axis  = 1)
	max_bldg = bldg['kw'].max()

	pv.index = pd.to_datetime(pv['date'])
	pv = pv.drop('date', axis = 1)
	pv = pv.rename(columns = {' kwh' : 'kw'})
	max_pv = pv['kw'].max()

	merged = pv.merge(bldg, left_index = True, right_index = True, suffixes = ['_prod', '_used'])
	scaler = max_bldg/max_pv
	merged['kw_prod'] *= scaler
	# merged['kw_used'] *= -1
	merged = merged.fillna(method = 'ffill')
	return merged

def merge_pv_usage_cost(df):
	tou_rate = map(date_tou_rate, df.index)
	df['tou_rate'] = tou_rate
	return df

def jack_up_production(df, production_multiplier = 1.5):
	df['kw_prod_jacked'] = df['kw_prod'] * production_multiplier
	df = df.rename(columns= {
					'kw_used': 'demand', 
					'tou_rate' : 'gridcost',
					'kw_prod_jacked' : 'pv'}
					)
	df = df.drop('kw_prod', axis = 1)
	return 	df
	
if __name__ == '__main__':
	building_files = filter(lambda x: x.startswith('BLd'), os.listdir('data-sources/'))
	pv_file = 'pv-data-jan2015.csv'
	# bldg_file = 'BLd1_15min_kW_250kWmax.csv'
	for bldg_file in building_files:
		print("working on {}".format(bldg_file))
		merged = merge_pv_usage(pv_file, bldg_file)
		merged = merge_pv_usage_cost(merged)
		merged = jack_up_production(merged, 1.5)
		merged.to_csv('data-sources/{}.csv'.format(bldg_file.split('_')[0]))
