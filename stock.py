from pymongo import MongoClient

from cybos.util import *
try:
    from config import MONGOURL
except Exception:
    MONGOURL = 'mongodb://localhost:27017/'

mongoClient = MongoClient(MONGOURL)
db = mongoClient['Daeshin']


class Stock:

    codeMgr = CodeMgr()
    chart = Chart()
    def __init__(self):
       pass

    def codeInDB(self):
        collection = db['codeInfo']
        codeDB = collection.find()
        codeListInDB = []
        for codeInfo in codeDB:
            codeListInDB.append(codeInfo['code'])
        return codeListInDB

    def codeInfoInDB(self):
        collection = db['codeInfo']
        codeDB = collection.find()
        return codeDB

    def insertNewCode(self):
        collection = db['codeInfo']
        '''
            1. 증권사로부터 codeList 정보 수집
            2. DB에 저장되어 있는 codeList 확인
            3. 비교하여 없는 경우 code 정보를 DB에 저장
        '''

        codeList = self.codeMgr.GetStockListByMarket(1) + self.codeMgr.GetStockListByMarket(2) # 1 거래소 2 코스닥
        codeListInDB = self.codeInDB()

        for code in codeList:
            # http://cybosplus.github.io/cputil_rtf_1_/cpcodemgr.htm

            if code not in codeListInDB:
                codeInfo = {}
                codeInfo['code'] = code
                codeInfo['name'] = self.codeMgr.CodeToName(code)
                codeInfo['firstCode'] = self.codeMgr.GetStockMarketKind(code)
                codeInfo['secondCode'] = self.codeMgr.GetStockSectionKind(code) # 부 구분 코드
                codeInfo['stdPrice'] = self.codeMgr.GetStockStdPrice(code)  # 권리락 등으로 인한 기준가
                # {'code': 'A000020', 'name': '동화약품', 'firstCode': 1, 'secondCode': 1, 'stdPrice': 14500}
                collection.update_one({'code': code}, {'$set': codeInfo}, upsert=True)
                print(codeInfo)
                time.sleep(1)

    def insertNewChart(self):
        collection = db['chart']
        codeListInDB = self.codeInfoInDB()
        for codeInfo in codeListInDB:
            if codeInfo['secondCode'] == 1: # 주권
                code = codeInfo['code']
                name = codeInfo['name']
                chartDataList = self.chart.getChart(code=codeInfo['code'], numData=1000)
                for chartData in chartDataList:
                    date = chartData[0]
                    chartInfo = {'code': code, 'name': name, 'date': date, 'data': chartData[1:]}
                    collection.update_one({'code': codeInfo['code'], 'date': date}, {'$set': chartInfo}, upsert=True)
                time.sleep(5)





