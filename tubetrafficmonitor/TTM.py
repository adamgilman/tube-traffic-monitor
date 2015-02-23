# -*- coding: utf-8 -*-
import time, logging, sys
from datetime import datetime, timedelta
import redis

lgr = logging.getLogger("TTM")
lgr.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.CRITICAL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lgr.addHandler(ch)

class TTM(object):
	def __init__(self):
		self.r = redis.Redis(host='localhost', port=6379, db=0)

	def setupTPH(self, name):
		return TPH(name, self.r)

	def TPH(self, name):
		return 0

class TPHArchive(object):
	def __init__(self):
		pass

	def _boundTime(self, givenTime):
		return givenTime.replace(minute=0, second=0, microsecond=0)

	def _archiveKey(self, key, givenTime):
		params = {'key' : key, 'start_epoch' : epoch(self._boundTime(givenTime))}
		return "!archive-{key}-{start_epoch}".format(**params)

	def archive_add(self, key, trainID):
		lgr.info("Adding %s to TPH(Archive @%s)" % (trainID, self._archiveKey(key, datetime.now())))
		self.r.sadd(self._archiveKey(key, datetime.now()), trainID)
		lgr.debug("Archive Contents: %s : %s " % ( self._archiveKey(key, datetime.now()), self.r.smembers(self._archiveKey(key, datetime.now())) ))

	def archive(self, key, dt):
		dt = self._boundTime(dt)
		lgr.debug( "Retrieve Archive: %s:@%s(%s: %s)" % (key, dt, self._archiveKey(key,dt), self.r.smembers( self._archiveKey(key, dt) )) )
		return self.r.smembers( self._archiveKey(key, dt) ) 

class TPH(TPHArchive):
	def __init__(self, name, r):
		self.name = name
		self.r = r
		self.key = "!trend-%s" % name
		self.r.delete(self.key)
		self.current = 0

	def add(self, trainID):
		lgr.info("Adding %s to TPH(Current)" % trainID)
		self.r.zadd(self.key, trainID, epoch())
		self.archive_add(self.name, trainID)

	@property
	def current(self):
	    #return 0 -> now-1 hour
		maxtime = time.mktime( (datetime.now() - timedelta(hours=1)).timetuple() )
		mintime = epoch()
		return len(self.r.zrangebyscore(self.key, maxtime, mintime))

	@current.setter
	def current(self, value):
	    self._foo = value	


def epoch(givenTime=None): 
	if not givenTime:
		return time.time()
	else:
		return time.mktime( givenTime.timetuple() )

def hourBlock():
	pass