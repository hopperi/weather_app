import datetime
import psycopg2

def get_local_time(timezone_offset):
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    tz = datetime.timezone(datetime.timedelta(seconds=timezone_offset))
    local_time = utc_now.astimezone(tz)
    return local_time.strftime('%H:%M:%S %Y-%m-%d')
