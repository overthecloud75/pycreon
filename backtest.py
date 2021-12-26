from commons.customlogging import setupLogger
from backtesting.models import *

def main():
    logger = setupLogger(identity='backtest')
    logger.info('main start')

    backtest = BackTesting()
    for period in [24]:
        for stay in [1, 2, 3, 6]:
            backtest.strategy(period=period, stay=stay, beforeStay=0)

if __name__ == '__main__':
    main()