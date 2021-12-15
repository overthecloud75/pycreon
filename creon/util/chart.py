import win32com.client


class Chart:
    def __init__(self):
        self.chart = win32com.client.Dispatch('CpSysDib.StockChart')
        self.chartFields = (0, 1, 2, 3, 4, 5, 8, 9, 12, 14, 15, 16, 17, 18, 20, 21, 24)
        # 필드 0: 날짜, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 8: 거래량, 9: 거래대금, 14: 외국인주문한도수량, 15: 외국인 주문가능 16
        # 20211214 21250 21450 20900 21050 140240 2958000000 50773000 50773400 42816774 7956626 15.670000076293945 20211214 100.0 -26179 -26179 0

    def getChart(self, code=None, tick='D', numData=1):
        self.setValue(code, tick=tick, numData=numData)
        self.chart.BlockRequest()
        chartData = self.getValue()
        return chartData

    def setValue(self, code, tick='D', numData=1):
        # ord(c)는 문자의 유니코드 값을 돌려주는 함수이다.

        self.chart.SetInputValue(0, code)        # 종목코드
        self.chart.SetInputValue(1, ord('2'))    # 요청 구분 '2' 개수 요청
        self.chart.SetInputValue(4, numData)          # 요청 개수
        self.chart.SetInputValue(5, self.chartFields)
        self.chart.SetInputValue(6, ord(tick))     # 차트 구분 'D', 'W', 'M'
        self.chart.SetInputValue(9, ord('1'))     # 수정 주가 '1' 수정 주가

    def getValue(self):
        chartDataList = []
        numData = self.chart.GetHeaderValue(3)   # 수신 개수
        numField = self.chart.GetHeaderValue(1)
        for i in range(numData):
            chartData = []
            for j in range(numField):
                chartData.append(self.chart.GetDataValue(j, i))
            chartDataList.append(chartData)
        return chartDataList
