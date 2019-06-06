# coding=utf-8

import os
import sys
import shutil
import multiprocessing as mp
from itertools import repeat as re
from collections import namedtuple
from itertools import chain
from dateutil.tz import tzutc
import json
import csv
import datetime
import time
from dateutil.rrule import rrule, DAILY
import binance.client 



class DataClient(object):

	def __init__(self,**kwargs):
		self.platform = sys.platform
		self.pathname = os.path.dirname(sys.argv[0])
		self.full_file_path = self.os_dir_suffix(os.path.abspath(self.pathname))
		self.titles = ['Opened','Open','High','Low','Close','Volume']
		self.fields = ['opened','open_','high','low','close_','volume']
		self.csv_dates = {}
		self.progress_statements = False

	def os_dir_suffix(self,intended_dir):
		if self.platform == 'win32':
			dir_format = '{}\\'.format(intended_dir)
		else:
			dir_format = '{}/'.format(intended_dir)
		return dir_format

	def get_binance_pairs(self,**kwargs):
		base_currencies = kwargs.get('base_currencies','')
		quote_currencies= kwargs.get('quote_currencies','')
		binance_pairs = list()
		if base_currencies and quote_currencies:
			input_pairs = [x+y for x in quote_currencies for y in base_currencies]
		for x,currency_pair in enumerate(binance.client.Client(None,None).get_all_tickers()):
			if base_currencies and quote_currencies:
				for pair in input_pairs:
					if currency_pair['symbol'] == pair.upper():
						binance_pairs.append(currency_pair['symbol'])
						break
			elif base_currencies:
				for base_currency in base_currencies:
					if currency_pair['symbol'][-len(base_currency):] == base_currency.upper():
						binance_pairs.append(currency_pair['symbol'])
						break
			elif quote_currencies:
				for quote_currency in quote_currencies:
					if currency_pair['symbol'][:len(quote_currency)] == quote_currency.upper():
						binance_pairs.append(currency_pair['symbol'])
						break
			else:
				binance_pairs.append(currency_pair['symbol'])
		if binance_pairs:
			return binance_pairs
		else:
			raise ValueError('Invalid Input: Binance returned no matching currency pairs.')

	def get_earliest_valid_timestamp(self, pair, interval):
		client = binance.client.Client(None,None)
		"""Get earliest valid open timestamp from Binance
		:param symbol: Name of symbol pair e.g BNBBTC
		:type symbol: str
		:param interval: Binance Kline interval
		:type interval: str
		:return: first valid timestamp
		"""
		kline = client.get_klines(
			symbol=pair,
			interval=interval,
			limit=1,
			startTime=0,
			endTime=int(time.time() * 1000)
		)
		return datetime.datetime.fromtimestamp(float(kline[0][0])/1000)

	def process_csv_dates(self,pair,interval,**kwargs):
		start_date = kwargs.get('start_date','')
		end_date = kwargs.get('end_date','')
		first_csv_date = self.csv_dates.get('first','')
		last_csv_date = self.csv_dates.get('last','')
		csv_dir = self.csv_dates.get('dir','')
		date_ranges=list()
		earliest_timestamp = self.get_earliest_valid_timestamp(pair,interval)
		if not start_date and not first_csv_date and not end_date:
			end_date = datetime.datetime.utcnow()
			date_ranges.append([earliest_timestamp,end_date])
		elif not start_date and not first_csv_date and end_date:
			if end_date<earliest_timestamp:
				raise ValueError('Invalid Date Range: end date is prior to Binance open date of 07/14/2017')
			date_ranges.append([earliest_timestamp,end_date])
		elif start_date and not first_csv_date and end_date:
			if start_date<earliest_timestamp:
				start_date = earliest_timestamp
			if end_date<start_date:
				raise ValueError('Invalid Date Range: end date is before start date')
			date_ranges.append([start_date,end_date])
		elif not start_date and not end_date and first_csv_date:
			end_date = datetime.datetime.utcnow()
			date_ranges.append([last_csv_date,end_date])
			past_csv_files = sorted(os.listdir(csv_dir))
			os.remove(''.join([csv_dir,past_csv_files[-1]]))
		else:
			if start_date<earliest_timestamp:
				start_date = earliest_timestamp
			if end_date<start_date:
				raise ValueError('Invalid Date Range: end date is before start date')
			elif start_date<=first_csv_date and end_date>=last_csv_date:
				date_ranges.append([start_date,first_csv_date-datetime.timedelta(days=1)])
				date_ranges.append([last_csv_date,end_date])
				past_csv_files = sorted(os.listdir(csv_dir))
				os.remove(''.join([csv_dir,past_csv_files[-1]]))
			elif start_date>=first_csv_date and end_date>=last_csv_date:
				date_ranges.append([last_csv_date,end_date])
				past_csv_files = sorted(os.listdir(csv_dir))
				os.remove(''.join([csv_dir,past_csv_files[-1]]))
			elif start_date<=first_csv_date and end_date<=last_csv_date:
				date_ranges.append([start_date,first_csv_date-datetime.timedelta(days=1)])
			else:
				return None
		dates = list(chain.from_iterable([[date for date in rrule(DAILY,dtstart=x[0], until=x[1]+datetime.timedelta(days=1))] for x in date_ranges]))
		return dates

	def process_kline_output(self,output):
		output_data = {
		'opened':{
			'title':'Opened',
			'var':'opened'
			},
		'open':{
			'title':'Open',
			'var':'open_'
			},
		'high':{
			'title':'High',
			'var':'high'
			},
		'low':{
			'title':'Low',
			'var':'low'
			},
		'close':{
			'title':'Close',
			'var':'close_'
			},
		'volume':{
			'title':'Volume',
			'var':'volume'
			},
		'closed':{
			'title':'Closed',
			'var':'closed'
			},
		'quote_volume':{
			'title':'Quote Asset Volume',
			'var':'quote_volume'
			},
		'total_trades':{
			'title':'Total Trades',
			'var':'total_trades'
			},
		'taker_buy_base_volume':{
			'title':'Taker Buy Base Asset Volume ',
			'var':'taker_buy_base_volume'
			},
		'taker_buy_quote_volume':{
			'title':'Take Buy Quote Asset Volume',
			'var':'taker_buy_quote_volume'
			},
		}
		if output:
			self.titles=[]
			self.fields =[]
			for x in output:
				try:
					self.titles.append(output_data.get(x,'')['title'])
					self.fields.append(output_data.get(x,'')['var'])
				except TypeError:
					raise ValueError('Invalid Output Field: valid fields include opened,open,high,low,close,volume,closed,quote_volume,total_trades,taker_buy_base_volume,taker_buy_quote_volume')


	def create_csv_directories(self,pair_list,kline_interval,historical_price_data_directory=None):
		if not historical_price_data_directory:
			historical_price_data_directory = '{}historical_price_data'.format(self.full_file_path)
		try:
			os.makedirs(historical_price_data_directory)
		except OSError:
			pass
		kline_interval_directory = ''.join([self.os_dir_suffix(historical_price_data_directory),'{}_data'.format(kline_interval)])
		try:
			os.makedirs(kline_interval_directory)
		except OSError:
			pass
		for x,p in enumerate(pair_list):
			pair_directory = ''.join([self.os_dir_suffix(kline_interval_directory),'{}'.format(str(p))])
			try:
				os.makedirs(pair_directory)
			except OSError:
				pass
			individual_csvs_directory = ''.join([self.os_dir_suffix(pair_directory),'individual_csvs'])
			try:
				os.makedirs(individual_csvs_directory)
			except OSError:
				pass
		return kline_interval_directory

	def date_to_milliseconds(self,date):
		epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=tzutc())
		return int((date - epoch).total_seconds() * 1000.0)

	def interval_to_milliseconds(self,interval):
		ms = None
		seconds_per_unit = {'m': 60,'h': 60 * 60,'d': 24 * 60 * 60,'w': 7 * 24 * 60 * 60}
		unit = interval[-1]
		if unit in seconds_per_unit:
			try:
				ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
			except ValueError:
				pass
		return ms

	def get_historical_klines(self,symbol, interval, start,end):
		client = binance.client.Client(None,None)
		output_data = []
		limit = 1000
		timeframe = self.interval_to_milliseconds(interval)
		start_ts = self.date_to_milliseconds(start)
		end_ts = self.date_to_milliseconds(end)
		idx = 0
		symbol_existed = False
		while True:
			try:
				temp_data = client.get_klines(symbol=symbol,interval=interval,limit=limit,startTime=start_ts,endTime=end_ts)
				if not symbol_existed and len(temp_data):
					symbol_existed = True
				if symbol_existed:
					output_data += temp_data
					start_ts = temp_data[len(temp_data) - 1][0] + timeframe
				else:
					start_ts += timeframe
				idx += 1
			except Exception as e:
				print (str(e))
				idx+=1
			if len(temp_data) < limit:
				break
		return output_data

	def past_csv_check(self,kline_interval_directory,pair):
		individual_csvs_directory = ''.join([self.os_dir_suffix(kline_interval_directory),self.os_dir_suffix(pair),self.os_dir_suffix('individual_csvs')])
		past_csv_files = sorted(os.listdir(individual_csvs_directory))
		if past_csv_files:
			self.csv_dates['first'] = datetime.datetime.strptime(past_csv_files[0].replace('.csv',''),'%Y-%m-%d')
			self.csv_dates['last'] = datetime.datetime.strptime(past_csv_files[-1].replace('.csv',''),'%Y-%m-%d')
			self.csv_dates['dir'] = individual_csvs_directory
		else:
			self.csv_dates = {}

	def concatenate_csvs(self,csv_file_info):
		for x,file_info in enumerate(csv_file_info):
			pair,output_path,interval = file_info
			concat_csv_path = self.os_dir_suffix(os.path.join(*(output_path.rsplit(os.path.sep,2)[:-2])))
			individual_csv_files = sorted([f for f in os.listdir(output_path) if f.endswith('.csv')])
			old_concat_csvs = [f for f in os.listdir(concat_csv_path) if f.endswith('.csv') ]
			concat_csv = '{}.csv'.format(pair)
			if concat_csv in old_concat_csvs:
				old_concat_csvs_path = '{}{}'.format(concat_csv_path,self.os_dir_suffix('old_concatenated_csvs'))
				try:
					os.makedirs(old_concat_csvs_path)
				except OSError:
					pass
				shutil.move('{}{}'.format(concat_csv_path,concat_csv),'{}{}'.format(self.os_dir_suffix(old_concat_csvs_path),concat_csv))
			if individual_csv_files:
				for x,csv_file in enumerate(individual_csv_files):
					outpath = '{}{}'.format(concat_csv_path,concat_csv)
					fout=open(outpath,'a')
					full_csv_file_path = '{}{}'.format(output_path,csv_file)
					writer = csv.writer(fout,lineterminator='\n')
					with open(full_csv_file_path) as f:
						if x != 0:
							f.__next__()
						for line in f:
							if len(line)>1:
								writer.writerow([x.strip() for x in line.split(',')])
					f.close()
					fout.close()


	def kline_to_csv(self,pair,start_date,end_date,kline_interval_directory,interval,csv_file_info):
		csv_dates = self.past_csv_check(kline_interval_directory,pair)
		date_range = self.process_csv_dates(pair,interval,start_date=start_date,end_date=end_date)
		if not date_range:
			return
		output_path = ''.join([self.os_dir_suffix(kline_interval_directory),self.os_dir_suffix(pair),self.os_dir_suffix('individual_csvs')])
		for x,date in enumerate(date_range):
			if date != date_range[-1]:
				if date_range[x+1]!=date+datetime.timedelta(days=1):
					continue
				else:
					year = str(date.year)
					numerical_month = str(date.month)
					start = date.replace(tzinfo=tzutc())
					end = date_range[x+1].replace(tzinfo=tzutc())
					if self.progress_statements==True:
						print ('currency pair: {} start: {} end: {}'.format(pair,start,end))
					klines = self.get_historical_klines(pair, interval, start, end)
					if klines:
						if int(date.day) in range(1,10):
							csv_day = '0{}'.format(str(date.day))
						else:
							csv_day = str(date.day)
						if int(date.month) in range(1,9):
							csv_month ='{}-0{}-'.format(year,numerical_month)
						else:
							csv_month = '{}-{}-'.format(year,numerical_month)
						results_csv = '{}{}{}.csv'.format(output_path,csv_month,csv_day)
						with open(results_csv, 'a') as f:
								writer = csv.writer(f)
								writer.writerow(self.titles)
						for y,kline in enumerate(klines):
							if kline != klines[-1]:
								self.open_timestamp,self.open_,self.high,self.low,self.close_,self.volume,self.close_timestamp,self.quote_volume,self.total_trades,self.taker_buy_base_volume,self.taker_buy_quote_volume,ignore = kline
								self.opened = datetime.datetime.utcfromtimestamp(float(self.open_timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S')
								self.closed = datetime.datetime.utcfromtimestamp(float(self.close_timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S')
								csv_fields = [getattr(self,field) for field in self.fields]
								with open(results_csv, 'a') as f:
									writer = csv.writer(f)
									writer.writerow(csv_fields)
		file_retrevial_info = pair,output_path,interval
		csv_file_info.append(file_retrevial_info)

	def kline_data(self,pair_list,interval,**kwargs):
		start_date = kwargs.get('start_date','')
		end_date = kwargs.get('end_date','')
		storage = kwargs.get('storage','')
		output = kwargs.get('output','')
		progress_statements = kwargs.get('progress_statements','')
		if start_date:
			start_date = datetime.datetime.strptime(start_date,'%m/%d/%Y')
		if end_date:
			end_date = datetime.datetime.strptime(end_date,'%m/%d/%Y')
		valid_kline_intervals = ['1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h']
		if interval not in set(valid_kline_intervals):
			raise ValueError('Invalid Interval: Kline interval should be one of the following - {}'.format(','.join(valid_kline_intervals)))
		output = self.process_kline_output(output)
		if not storage:
			storage = ['csv',None]
		try:
			storage_method,intended_dir = storage
		except ValueError:
			storage_method = storage[0]
			intended_dir = None
		if progress_statements:
			self.progress_statements = progress_statements
		if storage_method.lower() == 'csv':
			kline_interval_directory = self.create_csv_directories(pair_list,interval,intended_dir)
			csv_file_info = mp.Manager().list()
			pair = [currency_pair for i,currency_pair in enumerate(pair_list)]
			lock = mp.Lock()
			pool = mp.Pool(processes=mp.cpu_count(),initargs=(lock,))
			# data = pool.starmap(self.kline_to_csv,zip(pair,re(start_date),re(end_date),re(kline_interval_directory),re(interval),re(titles),re(fields),re(csv_file_info)))
			data = pool.starmap(self.kline_to_csv,zip(pair,re(start_date),re(end_date),re(kline_interval_directory),re(interval),re(csv_file_info)))
			pool.close()
			pool.join()
			self.concatenate_csvs(set(list(csv_file_info)))
		else:
			raise ValueError('Invalid Storage Type: Currently only csv storage supported')