from creon.api import *
from commons.util import getDiffDate
from commons.custommodel import CustomModel
from config.publicconfig import TICKLIST

class Stock(CustomModel):
    def __init__(self, id=None, pwd=None, pwdcert=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' %__name__)

        self.creon = Account()
        self.creon.login(id=id, pwd=pwd, pwdcert=pwdcert)

        self.codeMgr = CodeMgr()
        self.chart = Chart()

    def insertNewCode(self):
        '''
            1. 증권사로부터 codeList 정보 수집
            2. DB에 저장되어 있는 codeList 확인
            3. 비교하여 없는 경우 code 정보를 DB에 저장
        '''
        collection = self.db['codeInfo']
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
                collection.insert_one(codeInfo)
                self.logger.warn('new code: %s' %codeInfo)
                time.sleep(1)

    def insertNewChart(self):
        '''
            1. DB에 저장되어 있는 codeList 확인
            2. secondCode가 1인지 확인
            3. DB에 오늘 날짜 data가 있는지 확인 후 없으면 4를 진행
               -> 장 종료 전은 날짜를 1일 뺌
            4. 오늘 날짜가 없다면 기록된 마지막 날짜와의 날짜 차이만큼 numData 설정
            5. chartData DB에 저장
            6. 장종료 전의 data는 저장하지 않음
        '''
        collection = self.db['chart']
        codeInfoListInDB = self.codeInfoInDB()
        for codeInfo in codeInfoListInDB:
            code = codeInfo['code']
            name = codeInfo['name']
            for tick in TICKLIST:
                numData, today = self.getNumData(code, tick=tick)
                print(numData, today, tick, code)
                if numData:
                    chartDataList = self.chart.getChart(code=codeInfo['code'], tick=tick, numData=numData)
                    chartDataList.reverse()
                    for chartData in chartDataList:
                        date = chartData[0]
                        chartInfo = {'code': code, 'name': name, 'date': date, 'type': tick, 'data': chartData[1:]}
                        try:
                            if date > today:
                                # 장 종료전의 data가 수집되는 것을 막기 위함
                                pass
                            else:
                                collection.update_one({'code': codeInfo['code'], 'date': date, 'type': tick}, {'$set': chartInfo}, upsert=True)
                        except Exception as e:
                            self.logger.error('%s: %s' %(e, chartInfo))
                    self.logger.info('insertNewChart: %s, numData: %s, type: %s' %(code, str(numData), tick))
                    time.sleep(3)
        # cursor의 notimeout=True로 한 경우 사용 후 종료 필요
        # codeInfoListInDB.close()

    def getNumData(self, code, tick='D'):
        collection = self.db['chart']
        lastChartData = collection.find_one({'code': code, 'type': tick}, sort=[('date', -1)])
        if lastChartData is None:
            numData, today = getDiffDate(tick=tick)
        else:
            numData, today = getDiffDate(lastChartData['date'], tick=tick)
            # totalCount = collection.count_documents({'code': code})
            # pymongo에서 count()를 사용하면 에러 발생 (최신 버전에서 바뀐 듯)
        return numData, today
