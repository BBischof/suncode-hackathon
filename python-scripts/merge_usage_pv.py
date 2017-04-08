''' merge PV production with usage '''

import pandas as pd


def foo(pv_file, bldg_file):
	pv = pd.read_csv('data-sources/{}'.format(pv_file))
	bldg = pd.read_csv('data-sources/{}'.format(bldg_file), header=None)
	bldg.columns = ['date', 'time', 'kw']
	bldg.index = pd.to_datetime(bldg['date'] + ' ' +bldg['time'])
	bldg = bldg.drop(['date', 'time'], axis  = 1)
	max_bldg = bldg['kw'].max()

	pv.index = pd.to_datetime(pv['date'])
	pv = pv.drop('date', axis = 1)
	pv = pv.rename(columns = {' kwh' : 'kw'})
	max_pv = pv['kwh'].max()

	merged = pv.merge(bldg, left_index = True, right_index = True, suffixes = ['_prod', '_used'])
	scaler = max_pv/max_bldg
	merged['kw_used'] *= scaler
	return merged
