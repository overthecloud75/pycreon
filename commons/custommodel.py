from pymongo import MongoClient

try:
    from config.privateconfig import MONGO_URL, DB_NAME
except Exception:
    MONGOURL = 'mongodb://localhost:27017/'
    DB_NAME = 'Daeshin'

class CustomModel:

    def __init__(self):
        self.mongoClient = MongoClient(MONGO_URL)
        self.db = self.mongoClient[DB_NAME]

    def corpCodeInDB(self):
        collection = self.db['corpCode']
        corpCodeListInDB = []
        corpCodeDB = collection.find()
        for corp in corpCodeDB:
            corpCodeListInDB.append(corp)
        return corpCodeListInDB

    def codeInDB(self):
        collection = self.db['codeInfo']
        codeDB = collection.find()
        codeListInDB = []
        for codeInfo in codeDB:
            codeListInDB.append(codeInfo['code'])
        return codeListInDB

    def codeInfoInDB(self):
        collection = self.db['codeInfo']
        # MongoDB Cursor Not Found
        # https://velog.io/@rhs0266/MongoDB-Cursor-Not-Found-1
        # https://docs.mongodb.com/manual/reference/method/cursor.noCursorTimeout/
        # https://docs.mongodb.com/v4.4/reference/method/cursor.noCursorTimeout/
        # https://stackoverflow.com/questions/24199729/pymongo-errors-cursornotfound-cursor-id-not-valid-at-server
        # codeInfoList = collection.find(no_cursor_timeout=True)
        codeDB = collection.find()
        codeInfoListInDB = []
        for codeInfo in codeDB:
            if codeInfo['secondCode'] == 1:  # 주권
                codeInfoListInDB.append(codeInfo)
        return codeInfoListInDB