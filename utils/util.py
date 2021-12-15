import datetime

def getDiffDate(lastDate):
    lastDate = str(lastDate)
    today = datetime.date.today()
    now = datetime.datetime.now()
    if today.weekday() == 5:
        today = today - datetime.timedelta(1)
    elif today.weekday() == 6:
        today = today - datetime.timedelta(2)
    elif now.hour < 16:
        today = today - datetime.timedelta(1)
    lastDateToDatetime = datetime.date(int(lastDate[0:4]), int(lastDate[4:6]), int(lastDate[6:]))
    numData = (today - lastDateToDatetime).days
    return numData






