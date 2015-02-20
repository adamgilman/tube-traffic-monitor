#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime as dt, timedelta as td

from freezegun import freeze_time
from mock import patch
from mockredis import mock_redis_client

from tubetrafficmonitor import TTM

class TestTPMtph(unittest.TestCase):

	def setUp(self):
		self.ttm = TTM()

	def test_TPH(self):
		#setup a train per hour object
		#current TPH should be 0
		tph = self.ttm.setupTPH("testing")
		self.assertEqual( tph.current, 0 )

	def test_TPH1(self):
		#send one train w/ trainID in
		#get 1 TPH back
		tph = self.ttm.setupTPH("testing")
		tph.add("trainID")
		tph.add("trainID")
		self.assertEqual( tph.current, 2 )

	@patch('redis.Redis', mock_redis_client)
	def test_TPH1then3(self):
		#send 1 train down
		#1 hour later, send 3
		tph = self.ttm.setupTPH("testing")
		tph.add("trainID1")
		self.assertEqual( tph.current, 1 )
		onehour = td(hours=1, minutes=1)
		timetarget = dt.now() + onehour
		with freeze_time( timetarget ):
			tph.add("trainID1")
			tph.add("trainID1")
			tph.add("trainID1")
			self.assertEqual( tph.current, 3 )

		

if __name__ == '__main__':
    unittest.main()
