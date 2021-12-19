from commons.customlogging import setupLogger
from backtesting.models import *

def main():
    logger = setupLogger(identity='backtest')
    logger.info('main start')

    backtest = BackTesting()
    backtest.strategy()

if __name__ == '__main__':
    main()