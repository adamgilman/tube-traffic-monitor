import rethinkdb as r
from tube import Tube
from datetime import datetime
from time import sleep
import sys

from rethinkdb.errors import ReqlOpFailedError

conn = r.connect('localhost', 28015).repl()
try: r.table_create('tube_monitor').run(conn)
except ReqlOpFailedError: pass

tube = Tube()

line = sys.argv[1]

while True:
    for train in tube.getAllTrainsForLine(line):
        data = {    'leadingcar_id': train.leadingcar_id,
                    'set_number': train.set_number,
                    'track_code': train.track_code,
                    'line':line,
                    'when_observed': r.expr(datetime.now(r.make_timezone('+1:00')))
                }
        r.table('tube_monitor').insert( data ).run(conn)
        print "inserting: %s \n" % data
    sleep(10)
    print "- sleeping \n"
