#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime as dt, timedelta as td
from random import random

from freezegun import freeze_time
from mock import patch
from mockredis import mock_redis_client

from tubetrafficmonitor import TTM
from tubetrafficmonitor.TTM import TPHArchive

#@unittest.skip("bork")
@patch('redis.Redis', mock_redis_client)
class TestTPMDayLoad(unittest.TestCase):
	def setUp(self):
		self.ttm = TTM()

	def test_1TPHFullDay(self):
		#send 1 TPH for 24 hours
		key = "VictoriaNB"
		tph = self.ttm.setupTPH(key)
		base = dt(month=2, day=23, year=2015)
		for dayHour in range(24):
			timetarget = base.replace(hour=dayHour, minute=random_minute())
			with freeze_time( timetarget ):
				tph.add("trainID:test_Day:%s" % dayHour) 

		check = base.replace(hour=random_hour(), minute=random_minute())
		self.assertEqual( len(tph.archive( key, check )), 1 )

	def test_1TPHFullDay(self):
		#send 1 TPH for 24 hours
		key = "VictoriaNB"
		check_key = {}
		tph = self.ttm.setupTPH(key)
		base = dt(month=2, day=23, year=2015)
		for dayHour in range(24):
			timetarget = base.replace(hour=dayHour, minute=random_minute())
			with freeze_time( timetarget ):
				number_of_trains = random_minute()
				check_key[dayHour] = number_of_trains
				for i in range(number_of_trains):
					tph.add("trainID(%s):test_Day:%s" % (i, dayHour)) 

		check_hour = random_hour()
		check = base.replace(hour=check_hour, minute=random_minute())
		self.assertEqual( len(tph.archive( key, check )), check_key[check_hour] )

	def tearDown(self):
		self.ttm.r.flushdb()
		pass

@unittest.skip("bork")
@patch('redis.Redis', mock_redis_client)
class TestTPMWeekLoad(unittest.TestCase):
	def setUp(self):
		self.ttm = TTM()

	def tearDown(self):
		self.ttm.r.flushdb()
		pass

@unittest.skip("bork")
@patch('redis.Redis', mock_redis_client)
class TestTPMWeekLoad(unittest.TestCase):
	def setUp(self):
		self.ttm = TTM()

	def tearDown(self):
		self.ttm.r.flushdb()
		pass

def random_minute(): return int(random()*60)
def random_hour(): return int(random()*24)



if __name__ == '__main__':
    unittest.main()
