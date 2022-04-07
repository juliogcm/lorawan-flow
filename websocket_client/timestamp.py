import calendar
from datetime import datetime

def timestamp():
    d = datetime.utcnow()
    timestamp=calendar.timegm(d.utctimetuple())
    timestamp=timestamp-10800
    return int(timestamp)
