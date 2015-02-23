#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime as dt, timedelta as td
from freezegun import freeze_time
from mock import patch
from mockredis import mock_redis_client

from tubetrafficmonitor import TTM
from tubetrafficmonitor.TTM import TPHArchive

#@unittest.skip("bork")
@patch('redis.Redis', mock_redis_client)
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
		tph.add("trainID:test_TPH1")
		tph.add("trainID:test_TPH1.1")
		self.assertEqual( tph.current, 2 )

	def test_TPH1then3(self):
		#send 1 train down
		#1 hour later, send 3
		tph = self.ttm.setupTPH("testing")
		tph.add("trainID1.1")
		self.assertEqual( tph.current, 1 )
		onehour = td(hours=1, minutes=1)
		timetarget = dt.now() + onehour
		with freeze_time( timetarget ):
			tph.add("trainID2.1")
			tph.add("trainID2.2")
			tph.add("trainID2.3")
			self.assertEqual( tph.current, 3 )

	def tearDown(self):
		self.ttm.r.flushdb()
		pass

@patch('redis.Redis', mock_redis_client)
class TestTPMtphArchive(unittest.TestCase):
	def setUp(self):
		self.ttm = TTM()

	def test_2TPH_ThenArchive(self):
		#send 2 trains/h then check that they are in the archive
		#in the next hour
		key = "testing"
		tph = self.ttm.setupTPH(key)
		tph.add("trainID:test_TPH1")
		tph.add("trainID:test_TPH1.1")
		self.assertEqual( tph.current, 2 )

		#should be in current hours archive
		self.assertEqual( len( tph.archive( key, dt.now() ) ), 2 )

	def test_2TPH_Archive_Check1HourBackwards(self):
		key = "testing"
		tph = self.ttm.setupTPH(key)
		tph.add("trainID:test_TPH2")
		tph.add("trainID:test_TPH2.1")
		self.assertEqual( tph.current, 2 )

		#should be in current hours archive
		self.assertEqual( len( tph.archive( key, dt.now() ) ), 2 )

		#should be in previous hours archive
		onehour = td(hours=1)
		timetarget = dt.now() + onehour
		#go forward in time 1 hour
		with freeze_time( timetarget ):
			tph.add("trainID:test_TPH2.1")
			#check the archive an hour ago 
			onehourago = dt.now() - onehour
			self.assertEqual( len( tph.archive( key, onehourago ) ), 2 )





	#archive is divided into boxes start/stop :00/:59
	#check day rollover

	def tearDown(self):
		self.ttm.r.flushdb()



class TestTPMtphArchiveTools(unittest.TestCase):
	def setUp(self):
		self.tpmarchive = TPHArchive()
		
	def testTimeBoxBoundsBoxing(self):
		#given a time, deliver the lower bounded hour start
		#start a bounding box for archive
		base = dt(month=2, day=23, year=2015, hour=2)

		self.assertEqual( self.tpmarchive._boundTime( base.replace(minute=13) ), base)
		self.assertEqual( self.tpmarchive._boundTime( base.replace(minute=00) ), base)
		self.assertEqual( self.tpmarchive._boundTime( base.replace(minute=59) ), base)

	def testArchiveKeyGeneration(self):
		base = dt(month=2, day=23, year=2015, hour=2)
		self.assertEqual( self.tpmarchive._archiveKey( "testTrain", base), "!archive-testTrain-1424656800.0")
		
		pass

if __name__ == '__main__':
    unittest.main()
