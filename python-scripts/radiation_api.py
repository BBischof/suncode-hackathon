''' Request Data From NSRDB using Python API
NOTE: to get into generation (KwH/m^2 need SAM, couldn't install properly!)
from: https://nsrdb.nrel.gov/api-instructions'''

import pandas as pd
import numpy as np
import sys, os

def get_solar(lat = 33.2164, lon = -97.1292, year = 2016, api_key = 'FWJi89yv0jtx32Owfs92k8inmBmozxlv2TrwW2dt', your_name = 'Jeff+Larson', your_email = 'jeffonabike@gmail.com'):
	# Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.

	# Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
	attributes = 'ghi,dhi,dni,wind_speed_10m_nwp,surface_air_temperature_nwp,solar_zenith_angle'
	# Choose year of data
	year = '2011'
	# Set leap year to true or false. True will return leap day data if present, false will not.
	leap_year = 'false'
	# Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
	interval = '30'
	utc = 'false'
	# Your reason for using the NSRDB.
	reason_for_use = 'beta+testing'
	# Your affiliation
	your_affiliation = 'my+institution'
	# Please join our mailing list so we can keep you up-to-date on new developments.
	mailing_list = 'false'
	# Declare url string
	url = 'http://developer.nrel.gov/api/solar/nsrdb_0512_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
	# Return just the first 2 lines to get metadata:
	info = pd.read_csv(url, nrows=1)
	# See metadata for specified properties, e.g., timezone and elevation
	timezone, elevation = info['Local Time Zone'], info['Elevation']
	# Return all but first 2 lines of csv to get data:
	df = pd.read_csv('http://developer.nrel.gov/api/solar/nsrdb_0512_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes), skiprows=2)
	# Set the time index in the pandas dataframe:
	df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval+'Min', periods=525600/int(interval)))
	return info, df
