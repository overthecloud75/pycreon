from commons.customlogging import setupLogger
from backtesting.models import *

def main():
    logger = setupLogger(identity='backtest')
    logger.info('main start')

    backtest = BackTesting()
    # momentum
    #for period in [12]:
    #     for stay in [1, 2, 3, 6]:
    #        backtest.strategy(period=period, stay=stay, beforeStay=0)

    # pbr
    for stay in [1, 2, 3, 6]:
        backtest.strategy(sr='pbr', period=0, stay=stay, beforeStay=0)

if __name__ == '__main__':
    main()