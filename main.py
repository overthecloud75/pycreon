import sys

from creon.util import *
from creon.models import Stock
from utils.customlogging import setupLogger
try:
    from config.privateconfig import USER
except Exception:
    USER = {'id': None, 'pwd': None, 'pwdcert': None}


def main():
    logger = setupLogger(identity='pycreon')
    logger.info('main start')
    creon = Account()
    creon.login(id=USER['id'], pwd=USER['pwd'], pwdcert=USER['pwdcert'])

    '''chart = Chart()
    data = chart.getChart(code='A000020', tick='M', numData=1)
    print(data)'''

    stock = Stock()
    stock.insertNewCode()
    stock.insertNewChart()
    # stock.deleteChart()

if __name__ == "__main__":
    main()





