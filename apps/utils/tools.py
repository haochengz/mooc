
from datetime import datetime, timedelta


def minutes_ago(now, minutes):
    now = datetime.now()
    ago = now - timedelta(minutes=30)
    return ago
