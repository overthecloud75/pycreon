import time
import logging
import sys

from dart.util import corpCodeToList
from dart.api.finance import fnlttSinglAcntAll
from commons.custommodel import CustomModel


class Dart(CustomModel):
    def __init__(self, bsnsYearList=[], reprtCodeList=[]):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' % __name__)
        self.bsnsYearList = bsnsYearList
        self.reprtCodeList = reprtCodeList

    def corpCodeToDB(self):
        '''
            corpCode를 DB 저장
            1.  DB에서 stockCode를 확인
            2.  DART API를 이용하여 corpCode 정보를 수집
                -> binary 파일을 zip으로 저장 후 unzip 후 xml file을 list로 변환
            3.  coroCode 정보중 stockCode가 있는 경우에 DB에 update
        '''
        collection = self.db['corpCode']
        stockCodeListInDB = self.codeInDB()
        corpCodeListInDB = corpCodeToList()
        for result in corpCodeListInDB:
            corpCode = result.findtext('corp_code')
            name = result.findtext('corp_name')
            stockCode = result.findtext('stock_code')
            modified = result.findtext('modify_date')
            if stockCode is not None:
                stockCode = 'A' + stockCode
                if stockCode in stockCodeListInDB:
                    collection.update_one({'stockCode': stockCode},
                                          {'$set': {'corpCode': corpCode, 'name': name, 'stockCode': stockCode, 'modified': modified}}, upsert=True)

    def insertNewFinanceData(self):
        '''
            1.  DB에서 corpCode 정보를 확인
            2.  DB에 원하는 finance data가 있는지 확인 후 없으면
            3.  DART API를 이용하여 finance정보를 수집
            4.  terms에 대한 정보도 수집
                -> accountId와 accountName을 매칭한 정보
        '''
        collection = self.db['finance']
        corpCodeListInDB = self.corpCodeInDB()
        terms = {}
        for corp in corpCodeListInDB:
            corpCode = corp['corpCode']
            for bsnsYear in self.bsnsYearList:
                for reprtCode in self.reprtCodeList:
                    financeDataInDB = collection.find_one({'corpCode': corpCode, 'bsnsYear': bsnsYear, 'reprtCode': reprtCode})
                    if financeDataInDB is None:
                        dataDict, terms, status = fnlttSinglAcntAll(corpCode=corpCode, bsnsYear=bsnsYear, reprtCode=reprtCode, fsDiv='OFS', terms=terms)
                        if dataDict or status == '013':
                            corpFinanceDict = {'corpCode': corpCode, 'stockCode': corp['stockCode'], 'bsnsYear': bsnsYear,
                                               'reprtCode': reprtCode, 'status': status, 'data': dataDict}
                            collection.insert_one(corpFinanceDict)
                        else:
                            self.logger.error('sys exit because of status : %s' %status)
                            sys.exit('exit because of status %s' %status)
                        time.sleep(2)
                    # 일 10,000 분 1,000
        self.saveTerms(terms)

    def saveTerms(self, terms):
        collection = self.db['terms']
        termsDB = collection.find()
        termsDictInDB = {}
        # DB에서 terms 확인
        for term in termsDB:
            termsDictInDB[term['accountId']] = term['accountName']

        for accountId in terms:
            if accountId in termsDictInDB:
                if terms[accountId] != termsDictInDB[accountId]:
                    self.logger.info('term is different')
                    self.logger.info('terms %s: %s' %(accountId, terms[accountId]))
                    self.logger.info('termsInDB %s: %s' %(accountId, termsDictInDB[accountId]))
                    for accountName in termsDictInDB[accountId]:
                        if accountName not in terms[accountId]:
                            terms[accountId].append(accountName)
                    collection.update_one({'accountId': accountId}, {'$set': {'accountId': accountId, 'accountName': terms[accountId]}}, upsert=True)
            else:
                self.logger.info('term is absent')
                self.logger.info('terms %s: %s' % (accountId, terms[accountId]))
                collection.update_one({'accountId': accountId}, {'$set': {'accountId': accountId, 'accountName': terms[accountId]}}, upsert=True)


