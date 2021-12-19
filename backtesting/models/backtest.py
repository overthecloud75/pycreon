import logging
import time

from commons.util import getDateList
from commons.custommodel import CustomModel
from backtesting.factors import Momentum

class BackTesting(CustomModel):
    def __init__(self, period=12, stay=1, categoryNo=20, portfolio=10, fee=0.0025):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' % __name__)
        self.codeListInDB = self.codeInDB()
        self.dateList = getDateList()

        self.period = period
        self.stay = stay
        self.categoryNo = categoryNo
        self.portfolio = portfolio
        self.fee = fee

        self.momentum = Momentum(period=self.period, stay= self.stay)

    def strategy(self, type='momentum'):
        '''
            1.  DB에서 stockCodeList를 확인
            2.  for dateList code
            3.  period및 stay 기간만큼 closeDataList 정보 수집 (date에 대한 내림 차순)
            4.  period및 stay 기간만큼 없는 경우 codeList에서 제외
            5.  codeList의 갯수가 categoryNo * portfolio 보다 작으면 break
        '''
        self.stopCodeList = []
        for date in self.dateList:
            codeDataList = []
            for code in self.codeListInDB:
                closeDataListInDB = self.closeDataInDB(code, endDate=date)
                if len(closeDataListInDB) != self.period + self.stay:
                    self.stopCodeList.append(code)
                else:
                    # if type =='momentum':
                    growth = self.momentum.get(closeDataListInDB, includeLastDate=False)
                    result = round((closeDataListInDB[0] * (1-self.fee) - closeDataListInDB[self.stay]) / closeDataListInDB[self.stay], 4)
                    codeDataList.append([growth, result, code])
            self.codeListInDB = self.getCodeWithoutStopCode()
            if len(self.codeListInDB) < self.categoryNo * self.portfolio:
                break
            else:
                # https://haesoo9410.tistory.com/193
                codeDataList.sort(key=lambda x:x[0])
                self.buyAndSell(date, codeDataList)
                time.sleep(5)
            self.stopCodeList = []

    def closeDataInDB(self, code, endDate=20211100):
        collection = self.db['chart']
        closeDataListInDB = []
        dataListInDB = collection.find({'code': code, 'type': 'M', 'date': {'$lte': endDate}},  sort=[('date', -1)]).limit(self.period + self.stay)
        for data in dataListInDB:
            closeDataListInDB.append(data['data'][4])
        return closeDataListInDB

    def getCodeWithoutStopCode(self):
        codeListInDB = []
        for code in self.codeListInDB:
            if code not in self.stopCodeList:
                codeListInDB.append(code)
        return codeListInDB

    def buyAndSell(self, date, codeDataList):
        lenCode = len(codeDataList)
        for i in range(self.categoryNo):
            first = round(i / self.categoryNo * lenCode)
            second = round( (i + 1) / self.categoryNo * lenCode)
            resultList = []
            for data in codeDataList[first: second]:
                resultList.append(data[1])
            avgResultList = sum(resultList) / len(resultList)
            print(date, i + 1, avgResultList)











