from creon.models import Stock, Processing
from commons.customlogging import setupLogger
try:
    from config.privateconfig import USER
except Exception:
    USER = {'id': None, 'pwd': None, 'pwdcert': None}


def main():
    logger = setupLogger(identity='pycreon')
    logger.info('main start')

    '''chart = Chart()
    data = chart.getChart(code='A000020', tick='M', numData=1)
    print(data)'''

    # data 수집
    stock = Stock(id=USER['id'], pwd=USER['pwd'], pwdcert=USER['pwdcert'])
    stock.insertNewCode()
    stock.insertNewChart()

    # data 가공
    process = Processing()
    process.processingData()

if __name__ == '__main__':
    main()





