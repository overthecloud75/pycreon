from pycybos.cputil import *
from pymongo import MongoClient
try:
    from config import *
except Exception:
    USER = {'id': None, 'pwd': None, 'pwdcert': None}
    MONGOURL = 'mongodb://localhost:27017/'

mongoClient = MongoClient(MONGOURL)
db = mongoClient['Daeshin']


class Stock:

    codeMgr = CpCodeMgr()
    def __init__(self):
       pass

    def codeInfo(self):
        self.collection = db['codeInfo']
        codeDB = self.collection.find()
        codeListInDB = []
        for codeInfo in codeDB:
            codeListInDB.append(codeInfo['code'])
        return codeListInDB

    def insertNewCode(self):

        '''
            1. 증권사로부터 codeList 정보 수집
            2. DB에 저장되어 있는 codeList 확인
            3. 비교하여 없는 경우 code 정보를 DB에 저장
        '''

        codeList = self.codeMgr.GetStockListByMarket(1) + self.codeMgr.GetStockListByMarket(2) # 1 거래소 2 코스닥
        codeListInDB = self.codeInfo()

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
                self.collection.update_one({'code': code}, {'$set': codeInfo}, upsert=True)
                print(codeInfo)
                time.sleep(1)


