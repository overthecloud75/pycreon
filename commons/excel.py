from openpyxl import Workbook, load_workbook
import os

from config.publicconfig import RESULT_PATH

# https://goodthings4me.tistory.com/487
def writeInExcel(dataList, dataType='data', fileName='분석 결과', sheetName='결과'):
    '''
        1. file이 있는지 확인 - 파일이 있다면 load 없으면 새로운 workbook 생성
        2. sheet가 있는지 확인 - 없으면 새로운 sheet 생성
        3. dataList를 행단위로 추가
    '''
    if os.path.exists(RESULT_PATH):
        pass
    else:
        os.mkdir(RESULT_PATH)
    filePath = os.path.join(RESULT_PATH, fileName+'.xlsx')

    if os.path.isfile(filePath):
        wb = load_workbook(filePath)
    else:
        wb = Workbook()

    # 이름이 있는 시트를 생성
    try:
        ws = wb[sheetName]
    except Exception as e:
        print(e)
        ws = wb.create_sheet(sheetName)

    # 행 단위로 추가
    if dataType == 'title':
        for i, data in enumerate(dataList):
            ws.cell(1, i+2, data)
    else:
        ws.append(dataList)
    wb.save(filePath)
