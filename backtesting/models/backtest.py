import logging

from commons.util import getDateList
from commons.excel import category, writeInExcel, summarize
from backtesting.factors import Momentum, PBR

class BackTesting():
    def __init__(self, portfolio=10, categoryNo=20, fee=0.0025):
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' % __name__)

        self.dateList = getDateList()

        self.categoryNo = categoryNo
        self.portfolio = portfolio
        self.fee = fee

    def strategy(self, sr='momentum', period=12, stay=1, beforeStay=1):
        '''
            1.  initialize
                -> DB에서 stockCodeList를 확인
                -> excel data title 작성
                -> fileName 및 sheetName 반환
            2.  for dateList code
            3.  period + stay + 1 기간만큼 closeDataList 정보 수집 (date에 대한 내림 차순)
            4.  period + stay + 1 기간만큼 없는 경우 codeList에서 제외
            5.  codeList의 갯수가 categoryNo * portfolio 보다 작으면 break
            6.  growth(과거 성장), result (결과) 기록 확인
            7.  category별 averaging 진행
            7.  data를 excel 기록
            8.  기록된 data를 다시 summarize
        '''

        fileName, sheetName = self.initialize(sr=sr, period=period, stay=stay, beforeStay=beforeStay)

        categoryList = category(categoryNo=self.categoryNo, types=['growth', 'result'])
        writeInExcel(categoryList, dataType='title', fileName=fileName, sheetName=sheetName)

        for date in self.dateList:
            growthResultList, lenCodeListInDB = self.factor.getGrowthResult(date=date)
            if lenCodeListInDB < self.categoryNo * self.portfolio:
                break
            else:
                # https://haesoo9410.tistory.com/193
                growthResultList.sort(key=lambda x:x[0])
                avgGrowthList, avgResultList = self.avgGrowthResult(growthResultList)
                excelDataList = [date] + avgGrowthList + avgResultList
                writeInExcel(excelDataList, dataType='data', fileName=fileName, sheetName=sheetName)

        summarize(categoryNo=self.categoryNo, stay=self.stay, fileName=fileName, sheetName=sheetName)

    def initialize(self, sr= 'momentum', period=12, stay=1, beforeStay=1):
        self.period = period
        self.stay = stay
        self.limit = period + stay + 1
        self.beforeStay = beforeStay
        # period + stay + 1 만큼 data를 취하기 위함
        if sr == 'momentum':
            self.factor = Momentum(period=self.period, stay=self.stay, fee=self.fee, beforeStay=self.beforeStay)
        elif sr == 'pbr':
            self.factor = PBR(fee=self.fee, beforeStay=self.beforeStay)
        else:
            self.factor = Momentum(period=self.period, stay=self.stay, fee=self.fee, beforeStay=self.beforeStay)

        fileName = sr[0:2] + '_pe' + str(self.period) + '_bs' + str(self.beforeStay)
        sheetName = sr[0:2] + '_pe' + str(self.period) + '_st' + str(self.stay) + '_bs' + \
                         str(self.beforeStay) + '_fee' + str(self.fee)

        return fileName, sheetName

    def avgGrowthResult(self, codeDataList):
        lenCode = len(codeDataList)
        avgGrowthList = []
        avgResultList = []
        for i in range(self.categoryNo):
            first = round(i / self.categoryNo * lenCode)
            second = round( (i + 1) / self.categoryNo * lenCode)
            growthList = []
            resultList = []
            for data in codeDataList[first: second]:
                growthList.append(data[0])
                resultList.append(data[1])
            avgGrowthList.append(round(sum(growthList) / len(growthList), 4))
            avgResultList.append(round(sum(resultList) / len(resultList), 4))
        return avgGrowthList, avgResultList

    def getCompanyCode(self, sr='momentum', period=12, beforeStay=1, date=None, level=1):
        '''
            1.  initialize
            2.  beforestay = beforestay - 1, stay = 0, period = period - 1
            3.  분위에 맞는 code 확인
        '''
        beforeStay = beforeStay - 1
        period = period - 1
        stay = 0
        _, _ = self.initialize(sr=sr, period=period, stay=stay, beforeStay=beforeStay)
        if date is None:
            date = self.dateList[0 + beforeStay]
        growthResultList, lenCodeListInDB = self.factor.getGrowthResult(date=date)
        growthResultList.sort(key=lambda x: x[0])
        first = round((level - 1) / self.categoryNo * lenCodeListInDB)
        second = round(level / self.categoryNo * lenCodeListInDB)
        growthResultList = growthResultList[first: second]

        growthList = []
        codeList = []
        for data in growthResultList:
            growthList.append(data[0])
            codeList.append(data[2])
        return growthList, codeList

















