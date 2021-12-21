from commons.customlogging import setupLogger
from backtesting.models import *

def main():
    logger = setupLogger(identity='backtest')
    logger.info('main start')

    backtest = BackTesting()
    backtest.strategy(stay=1)
    backtest.strategy(stay=2)
    backtest.strategy(stay=3)
    backtest.strategy(stay=6)

if __name__ == '__main__':
    main()