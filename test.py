from dart.models import Dart
from dart.api import corpCode
from utils.customlogging import setupLogger



def main():
    logger = setupLogger(identity='dart')
    logger.info('main start')
    # corpCode()
    dart = Dart()
    dart.corpCodeToDB()
    dart.insertNewFinanceData()

if __name__ == "__main__":
    main()




