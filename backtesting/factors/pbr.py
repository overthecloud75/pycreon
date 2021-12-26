class PBR:
    def __init__(self, equityTermsList=[], period=12, stay=1, fee=0.0025, beforeStay=1):
        self.period = period
        self.stay = stay
        self.fee = fee
        self.beforeStay = beforeStay
        self.equityTermsList = equityTermsList

    def get(self, dataList, financeData):
        # 내림차순 data 0이 최신, -1이 제일 오래됨
        equity = None
        for key in financeData['data']['재무상태표']:
            if key in self.equityTermsList:
                equity = financeData['data']['재무상태표']

        if equity:
            growth = equity / round((dataList[self.stay + self.beforeStay] - dataList[-1])/dataList[-1], 4)
        else:
            growth = None
        result = round((dataList[0] * (1 - self.fee) - dataList[self.stay]) / dataList[self.stay], 4)
        return growth, result