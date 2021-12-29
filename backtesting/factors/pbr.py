import logging

from commons.custommodel import CustomModel

class PBR(CustomModel):
    def __init__(self, period = 0, stay = 1, fee=0.0025, beforeStay=1):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' % __name__)

        self.period = period
        self.stay = stay
        self.fee = fee
        self.beforeStay = beforeStay
        self.limit = self.period + self.stay + self.beforeStay + 1
        # momemntum 같은 경우 beforstay가 self.period안에 포함되어 있음

        self.equityTermsList = self.equityTerms()
        self.codeListInDB = self.codeInDB()

    def getGrowthResult(self, date=None):
        growthResultList = []
        stopCodeList = []
        for code in self.codeListInDB:
            financeData = self.financeDataInDB(code, date)
            if financeData is not None:
                closeDataListInDB = self.closeDataInDB(code, endDate=date)
                noStock = self.getNoStock(code, endDate=date)
                if len(closeDataListInDB) != self.limit:
                    stopCodeList.append(code)
                else:
                    if closeDataListInDB[-1] <= 0:
                        self.logger.warning('the close price is strange, date: %s, code: %s' % (date, code))
                        stopCodeList.append(code)
                    else:
                        growth, result = self.get(closeDataListInDB, noStock, financeData)
                        if growth is not None:
                            growthResultList.append([growth, result, code])
                        else:
                            stopCodeList.append(code)

            else:
                stopCodeList.append(code)

        self.codeListInDB = self.getCodeWithoutStopCode(stopCodeList)
        return growthResultList, len(self.codeListInDB)

    def financeDataInDB(self, code, date):
        collection = self.db['finance']
        bsnsYear, reprtCode = self.getBsnsYear(date)
        financeData = collection.find_one({'stockCode': code, 'bsnsYear': bsnsYear, 'reprtCode': reprtCode})
        if financeData is not None:
            if financeData['status'] == '000':
                pass
            else:
                financeData = None
        return financeData

    def closeDataInDB(self, code, endDate=20211100):
        collection = self.db['chart']
        closeDataListInDB = []
        if str(endDate)[-2] != '00':
            dataListInDB = collection.find({'code': code, 'type': 'D', 'date': {'$lte': endDate}}, sort=[('date', -1)]).limit(self.limit)
        else:
            dataListInDB = collection.find({'code': code, 'type': 'M', 'date': {'$lte': endDate}},  sort=[('date', -1)]).limit(self.limit)
        for data in dataListInDB:
            closeDataListInDB.append(data['data'][4])
        return closeDataListInDB

    def getNoStock(self, code, endDate=20211100):
        endDate = int(str(endDate)[0:6] + '31')
        collection = self.db['chart']
        data = collection.find_one({'code': code, 'type': 'D', 'date': {'$lte': endDate}},  sort=[('date', -1)])
        noStock = None
        if data is not None:
            noStock  = data['data'][7]
        return noStock

    def get(self, dataList, noStock, financeData):
        # 내림차순 data 0이 최신, -1이 제일 오래됨
        # equity 오름차순으로 정렬하기 위함
        equity = None
        for key in financeData['data']['재무상태표']:
            if key in self.equityTermsList:
                equity = int(financeData['data']['재무상태표'][key])
        if equity:
            growth = round(equity / (dataList[-1] * noStock), 4)
        else:
            growth = None
        result = round((dataList[0] * (1 - self.fee) - dataList[self.stay]) / dataList[self.stay], 4)
        if growth is None:
            self.logger.info('Growth is None, finaceData: %s' %str(financeData['data']['재무상태표']))
        return growth, result

    def equityTerms(self):
        collection = self.db['terms']
        equity = collection.find_one({'accountId': 'ifrs-full_Equity'})
        equityTermsListInDB = equity['accountName']
        return equityTermsListInDB

    def getCodeWithoutStopCode(self, stopCodeList):
        codeListInDB = []
        for code in self.codeListInDB:
            if code not in stopCodeList:
                codeListInDB.append(code)
        return codeListInDB

    def getBsnsYear(self, date):
        date = str(date)
        year = int(date[0:4])
        month = int(date[4:6]) - self.limit + 1
        if month < 1:
            month = 12 + month
            if month % 12 != 0:
                year = year - month // 12
            else:
                year = year - month // 12 - 1
        bsnsYear = year - 1
        if month < 4:
            bsnsYear = year - 1
            reprtCode = 11011
        elif month < 7:
            reprtCode = 11013
        elif month < 10:
            reprtCode = 11012
        else:
            reprtCode = 11014
        return bsnsYear, reprtCode



