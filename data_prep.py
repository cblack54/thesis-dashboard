import pandas as pd
import datetime as dt
import re
import os

def clean():
    # df = pd.read_csv('./Sensor Data for Projects/3001/113001 Event History, 2017 Dec.csv')
    
	directory = './Sensor Data for Projects/3001/'
	df = pd.concat([pd.read_csv(os.path.join(directory,f)) for f in os.listdir(directory)])


	# searchfor = ['notification', 'module signal', 'phone test', 'modem','vacant', 'vacated','idle', 'up & about']
	# df = df[~df.Description.str.contains('|'.join(searchfor), case=False)]
	df = df[df['Type']=='Monitor']

	searchfor = ['sensor']
	df = df[df.Description.str.contains('|'.join(searchfor), case=False)]

	searchfor = ['vacant', 'vacate','idle']
	df = df[~df.Description.str.contains('|'.join(searchfor), case=False)]

	df['Time ($TZ)'] = pd.to_datetime(df['Time ($TZ)'])
	df['size'] = 1
	min_date = df['Time ($TZ)'].min()

	def total_time(row):
	    # calculates the degrees out of 360
	    # gets the minute of the day (out of 1440) by multiplying
	    # number of hours by 60 minutes and adding the minutes
	    # then divides by 4 because 1440 minutes/ 360 degrees = 4min/degree
	    return((row.hour*60 + row.minute)/4)

	def date_to_nth_day(date):
	    # get the day of the year
	    # jan_1 = dt.datetime(date.year,1, 1)
	    return(date-min_date).days + 1

	def desc_cleaner(string):
	    regex = re.search('^.*(?=(\(sensor))', string.lower())
	    if regex:
	        return(regex.group().strip())

	one_day = df.loc[df['Time ($TZ)'] > '2017-12-01']
	one_day['Date'] = one_day['Time ($TZ)'].dt.date
	one_day['Time'] = one_day['Time ($TZ)'].dt.time
	one_day['Total Minutes']= one_day['Time'].apply(total_time)
	# one_day.loc[one_day['Time ($TZ)'] > '2017-12-31','filler'] = 2
	# one_day.loc[one_day['Time ($TZ)'] < '2017-12-31','filler'] = 1
	one_day['n_day'] = one_day['Time ($TZ)'].apply(date_to_nth_day)
	one_day['mod desc'] = one_day['Description'].apply(desc_cleaner)

	return(one_day)


# using day of the year be careful for end case when date wraps over a year
# ie dec 2017 to jan 2018, 31 dec 2017 = 365 and need 01 jan 2018 to be 364
# clean()