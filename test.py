from dart.models import Dart
from dart.api import corpCode
from commons.customlogging import setupLogger


def main():
    logger = setupLogger(identity='dart')
    logger.info('main start')
    corpCode()
    dart = Dart(bsnsYearList=[2019], reprtCodeList=[11011])
    dart.corpCodeToDB()
    dart.insertNewFinanceData()

if __name__ == '__main__':
    main()




