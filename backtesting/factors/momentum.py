from commons.custommodel import CustomModel

class Momentum(CustomModel):
    def __init__(self, period=12, stay=1, fee=0.0025, beforeStay=1):
        super().__init__()
        self.period = period
        self.stay = stay
        self.fee = fee
        self.beforeStay = beforeStay
        self.limit = self.period + self.stay + 1

    def get(self, dataList):
        # 내림차순 data 0이 최신, -1이 제일 오래됨
        growth = round((dataList[self.stay + self.beforeStay] - dataList[-1])/dataList[-1], 4)
        result = round((dataList[0] * (1 - self.fee) - dataList[self.stay]) / dataList[self.stay], 4)
        return growth, result

    def closeDataInDB(self, code, endDate=20211100):
        collection = self.db['chart']
        closeDataListInDB = []
        dataListInDB = collection.find({'code': code, 'type': 'M', 'date': {'$lte': endDate}},  sort=[('date', -1)]).limit(self.limit)
        for data in dataListInDB:
            closeDataListInDB.append(data['data'][4])
        return closeDataListInDB


