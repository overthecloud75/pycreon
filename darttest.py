from dart.models import Dart
from dart.api import corpCode
from commons.customlogging import setupLogger


def main():
    logger = setupLogger(identity='dart')
    logger.info('main start')
    corpCode()
    '''
        단일회사 전체 재무제표

        reprtCode 
            - 1분기보고서 : 11013
            - 반기보고서 : 11012
            - 3분기보고서 : 11014
            - 사업보고서 : 11011
    '''
    dart = Dart(bsnsYearList=[2018], reprtCodeList=[11011, 11014])
    dart.corpCodeToDB()
    dart.insertNewFinanceData()

if __name__ == '__main__':
    main()




