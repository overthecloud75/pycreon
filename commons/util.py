import datetime

from config.publicconfig import NUMDATA_DAY, NUMDATA_MONTH, TRADING_END_TIME

def getDiffDate(lastDate=None, tick='D'):
    now = datetime.datetime.now()
    if tick=='D':
        today = datetime.date.today()
        if today.weekday() == 5:
            today = today - datetime.timedelta(1)
        elif today.weekday() == 6:
            today = today - datetime.timedelta(2)
        elif now.hour < TRADING_END_TIME:
            today = today - datetime.timedelta(1)
        if lastDate:
            lastDate = str(lastDate)
            lastDateToDatetime = datetime.date(int(lastDate[0:4]), int(lastDate[4:6]), int(lastDate[6:]))
            numData = (today - lastDateToDatetime).days
        else:
            numData = NUMDATA_DAY
        today = int(today.strftime('%Y%m%d'))
    else:
        thisYear = now.year
        thisMonth = now.month - 1
        if thisMonth == 0:
            thisMonth = 12
            thisYear = thisYear - 1
        today = datetime.date(thisYear, thisMonth, 1)
        if lastDate:
            lastDate = str(lastDate)
            lastDateToDatetime = datetime.date(int(lastDate[0:4]), int(lastDate[4:6]), 1)
            numData = diffMonth(today, lastDateToDatetime)
        else:
            numData = NUMDATA_MONTH
        today = int(today.strftime('%Y%m%d')) - 1
    return numData, today

def diffMonth(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def getDateList(tick='M'):
    _, today = getDiffDate(tick=tick)
    dateList = [today]
    today = str(today)
    thisYear = int(today[0:4])
    thisMonth = int(today[4:6])

    for i in range(NUMDATA_MONTH - 1):
        thisMonth = thisMonth - 1
        if thisMonth < 1:
            thisMonth = 12
            thisYear = thisYear - 1
        if thisMonth < 10:
            today = int(str(thisYear) + '0'+ str(thisMonth) + '00')
        else:
            today = int(str(thisYear) + str(thisMonth) + '00')
        dateList.append(today)
    return dateList











