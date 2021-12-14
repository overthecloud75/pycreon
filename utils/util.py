import datetime

def checkTime():
    today = datetime.date.today()
    now = datetime.datetime.now()
    hour = now.hour
    if today.weekday() == 5:
        today = today - datetime.timedelta(1)
    elif today.weekday() == 6:
        today = today - datetime.timedelta(2)
    elif now.hour < 16:
        today = today - datetime.timedelta(1)
    today = int(today.strftime('%Y%m%d'))
    return hour, today



