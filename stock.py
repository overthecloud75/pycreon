import logging
from pymongo import MongoClient

from cybos.util import *
from utils.util import checkTime
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
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' %__name__)

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
        '''
            1. 증권사로부터 codeList 정보 수집
            2. DB에 저장되어 있는 codeList 확인
            3. 비교하여 없는 경우 code 정보를 DB에 저장
        '''
        collection = db['codeInfo']
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
                self.logger.warn('new code: %s' %codeInfo)
                time.sleep(1)

    def insertNewChart(self):
        '''
            1. DB에 저장되어 있는 codeList 확인
            2. secondCode가 1인지 확인
            3. DB에 오늘 날짜 data가 있는지 확인 후 없으면 4를 진행
            4. chartData DB에 저장
        '''
        collection = db['chart']
        codeListInDB = self.codeInfoInDB()
        for codeInfo in codeListInDB:
            if codeInfo['secondCode'] == 1: # 주권
                code = codeInfo['code']
                name = codeInfo['name']
                tick = 'D'
                if self.DoesNeedProceed(code, tick):
                    chartDataList = self.chart.getChart(code=codeInfo['code'], tick=tick, numData=1000)
                    chartDataList.reverse()
                    for chartData in chartDataList:
                        date = chartData[0]
                        chartInfo = {'code': code, 'name': name, 'date': date, 'type': tick, 'data': chartData[1:]}
                        try:
                            collection.update_one({'code': codeInfo['code'], 'date': date}, {'$set': chartInfo}, upsert=True)
                        except Exception as e:
                            self.logger.error('%s: %s' %(e, chartInfo))
                    time.sleep(5)

    def DoesNeedProceed(self, code, tick):
        needProceed = True
        hour, today = checkTime()

        collection = db['chart']
        lastChartData = collection.find_one({'code': code, 'type': tick}, sort=[('date', -1)])
        if lastChartData is None:
            return needProceed
        elif lastChartData['date'] != today:
            return needProceed
        else:
            '''totalCount = collection.count_documents({'code': code})
            # pymongo에서 count()를 사용하면 에러 발생 (최신 버전에서 바뀐 듯)
            if totalCount == 1000:
                needProceed = False
                return needProceed
            else:
                self.logger.warn('code: %s, chartCount: %s' %(code, totalCount))
                return needProceed'''
            needProceed = False
            return needProceed





