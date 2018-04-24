
from datetime import timedelta


def minutes_ago(now, minutes):
    ago = now - timedelta(minutes=minutes)
    return ago
