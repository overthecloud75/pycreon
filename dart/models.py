from pymongo import MongoClient

from .util import corpCodeToList
try:
    from config.privateconfig import MONGOURL
except Exception:
    MONGOURL = 'mongodb://localhost:27017/'

mongoClient = MongoClient(MONGOURL)
db = mongoClient['Daeshin']

def corpCodeToDB():
    collection = db['corpCode']
    stockCodeList = stockCodeInDB()
    corpCodeList = corpCodeToList()
    for result in corpCodeList:
        corpCode = result.findtext('corp_code')
        name = result.findtext('corp_name')
        stockCode = result.findtext('stock_code')
        if stockCode is not None:
            stockCode = 'A' + stockCode
        modified = result.findtext('modify_date')
        if stockCode is None:
            pass
        elif stockCode in stockCodeList:
            collection.update_one({'stockCode': stockCode},
                                  {'$set': {'corpCode': corpCode, 'name': name, 'stockCode': stockCode, 'modified': modified}}, upsert=True)

def stockCodeInDB():
    collection = db['codeInfo']
    codeDB = collection.find()
    stockCodeList = []
    for codeInfo in codeDB:
        stockCodeList.append(codeInfo['code'])
    return stockCodeList
