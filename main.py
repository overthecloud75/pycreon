import sys

from creon.util import *
from creon.stock import Stock
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

    stock = Stock()
    stock.insertNewCode()
    try:
        stock.insertNewChart()
    except Exception as e:
        logger.error('error: %s' %e)
        sys.exit(e)
        # https://it-neicebee.tistory.com/53

if __name__ == "__main__":
    main()





