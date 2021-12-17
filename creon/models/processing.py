from pymongo import MongoClient
import logging

try:
    from config.privateconfig import MONGOURL, DB_NAME
except Exception:
    MONGOURL = 'mongodb://localhost:27017/'
    DB_NAME = 'Daeshin'

mongoClient = MongoClient(MONGOURL)
db = mongoClient[DB_NAME]

class Processing():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' %__name__)

    def codeInfoInDB(self):
        collection = db['codeInfo']
        codeDB = collection.find()
        codeInfoListInDB = []
        for codeInfo in codeDB:
            if codeInfo['secondCode'] == 1:  # 주권
                codeInfoListInDB.append(codeInfo)
        return codeInfoListInDB

    def processingData(self):
        codeInfoListInDB = self.codeInfoInDB()
        for codeInfo in codeInfoListInDB:
            code = codeInfo['code']
            self.getChartAndMaToDB(code)
            self.logger.info('%s ma is done' %code)

    def getChartAndMaToDB(self, code):
        '''
            1. code에 해당하는 dateList 확인 (date에 대한 내림 차순으로 정리)
            2. code와 date를 정보를 바탕으로 최근 120개 정보 확인
            3. close, ma5, ma20, ma60, ma120 정보 계산 및 저장
        '''
        dateListInDB = self.getDateInDB(code)
        for date in dateListInDB:
            self.maDataToDB(code, date)

    def getDateInDB(self, code, tick='D'):
        '''
            1. maData에 저장 되어 있는 data중 마지작 날짜와 시작 날짜 정보를 확인
            2. 마지막 날짜 보다 이후 날짜에 대해서만 date 정보 수집
        '''
        collection = db['chart']
        beginDate, endDate = self.maDateInDB(code)
        dateListInDB = []
        dataInDB = collection.find({'code': code, 'type': tick}, sort=[('date', -1)])
        if beginDate is None:
            for data in dataInDB:
                dateListInDB.append(data['date'])
        else:
            for data in dataInDB:
                if data['date'] > endDate: # or data['date'] < beginDate:
                    dateListInDB.append(data['date'])
                else:
                    break
        return dateListInDB

    def maDateInDB(self, code):
        collection = db['ma']
        dataInDB = collection.find_one({'code': code}, sort=[('date', 1)])
        if dataInDB is None:
            beginDate = None
            endDate = None
        else:
            beginDate = dataInDB['date']
            dataInDB = collection.find_one({'code': code}, sort=[('date', -1)])
            endDate = dataInDB['date']
        return beginDate, endDate

    def maDataToDB(self, code, date):
        collection = db['ma']
        maDataInDB = collection.find_one({'code': code, 'date': date})
        maData = {}
        if maDataInDB is None:
            closeDataListInDB = self.closeDataInDB(code, date, tick='D')

            maItemList = []
            periodList = [5, 20, 60, 120]
            for period in periodList:
                ma = int(sum(closeDataListInDB[0:period]) / len(closeDataListInDB[0:period]))
                maItemList.append(ma)
            maData = {'code': code, 'date': date, 'close': closeDataListInDB[0],
                      'ma5': maItemList[0], 'ma20': maItemList[1], 'ma60': maItemList[2], 'ma120': maItemList[3]}
            collection.insert_one(maData)
        return maData

    def closeDataInDB(self, code, date, tick='D'):
        collection = db['chart']
        dataListInDB = collection.find({'code': code, 'date': {'$lte': date}, 'type': tick}, sort=[('date', -1)]).limit(120)
        closeDataListInDB = []
        for data in dataListInDB:
            closeDataListInDB.append(data['data'][4])  # data['date'][4] 종가
        return closeDataListInDB

    def deleteChart(self):
        collection = db['chart']
        collection.delete_many({'type': 'M'})
