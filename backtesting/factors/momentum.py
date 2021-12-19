
class Momentum:
    def __init__(self, period=12, stay=1):
        self.period = period
        self.stay=stay

    def get(self, dataList, includeLastDate=False):
        if includeLastDate:
            growth = round((dataList[self.stay] - dataList[-1])/dataList[-1], 4)
        else:
            growth = round((dataList[self.stay + 1] - dataList[-1])/dataList[-1], 4)
        return growth


