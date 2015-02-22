# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
import redis


class TTM(object):
	def __init__(self):
		self.r = redis.Redis(host='localhost', port=6379, db=0)

	def setupTPH(self, name):
		return TPH(name, self.r)

	def TPH(self, name):
		return 0

class TPH(object):
	def __init__(self, name, r):
		self.name = name
		self.r = r
		self.key = "!trend-%s" % name
		self.r.delete(self.key)
		self.current = 0

	def add(self, trainID):
		self.r.zadd(self.key, trainID, epoch())
	
	@property
	def current(self):
	    #return 0 -> now-1 hour
		maxtime = time.mktime( (datetime.now() - timedelta(hours=1)).timetuple() )
		mintime = epoch()
		return len(self.r.zrangebyscore(self.key, maxtime, mintime))

	@current.setter
	def current(self, value):
	    self._foo = value	


def epoch(): return time.time()