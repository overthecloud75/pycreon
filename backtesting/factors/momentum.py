import logging

from commons.custommodel import CustomModel

class Momentum(CustomModel):
    def __init__(self, period=12, stay=1, fee=0.0025, beforeStay=1):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' % __name__)

        self.period = period
        self.stay = stay
        self.fee = fee
        self.beforeStay = beforeStay
        self.limit = self.period + self.stay + 1

        self.codeListInDB = self.codeInDB()

    def getGrowthResult(self, date=None):
        growthResultList = []
        stopCodeList = []
        for code in self.codeListInDB:
            closeDataListInDB = self.closeDataInDB(code, endDate=date)
            if len(closeDataListInDB) != self.limit:
                stopCodeList.append(code)
            else:
                # if sr =='momentum':
                if closeDataListInDB[-1] <= 0:
                    self.logger.warning('the close price is strange, date: %s, code: %s' % (date, code))
                    stopCodeList.append(code)
                else:
                    growth, result = self.get(closeDataListInDB)
                    growthResultList.append([growth, result, code])

        self.codeListInDB = self.getCodeWithoutStopCode(stopCodeList)
        return growthResultList, len(self.codeListInDB)

    def closeDataInDB(self, code, endDate=20211100):
        collection = self.db['chart']
        closeDataListInDB = []
        dataListInDB = collection.find({'code': code, 'type': 'M', 'date': {'$lte': endDate}},  sort=[('date', -1)]).limit(self.limit)
        for data in dataListInDB:
            closeDataListInDB.append(data['data'][4])
        return closeDataListInDB

    def get(self, dataList):
        # 내림차순 data 0이 최신, -1이 제일 오래됨
        growth = round((dataList[self.stay + self.beforeStay] - dataList[-1])/ dataList[-1], 4)
        result = round((dataList[0] * (1 - self.fee) - dataList[self.stay]) / dataList[self.stay], 4)
        return growth, result

    def getCodeWithoutStopCode(self, stopCodeList):
        codeListInDB = []
        for code in self.codeListInDB:
            if code not in stopCodeList:
                codeListInDB.append(code)
        return codeListInDB

