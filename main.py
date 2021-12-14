from cybos.util import *

from stock import Stock
from utils.customlogging import setupLogger
try:
    from config import USER
except Exception:
    USER = {'id': None, 'pwd': None, 'pwdcert': None}


def main():
    logger = setupLogger(identity='pycreon')
    logger.info('main start')
    creon = Creon()
    creon.connect(id=USER['id'], pwd=USER['pwd'], pwdcert=USER['pwdcert'])

    stock = Stock()
    stock.insertNewCode()
    stock.insertNewChart()


if __name__ == "__main__":
    main()





