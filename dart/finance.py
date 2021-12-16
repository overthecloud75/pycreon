from .util import requestData


# 단일회사 전체 재무제표
def fnlttSinglAcntAll(corpCode='00126380', bsnsYear=2018, reprtCode=11011, fsDiv='OFS'):
    apiPath = 'fnlttSinglAcntAll'
    params = {'corp_code': corpCode, 'bsns_year': bsnsYear, 'reprt_code': reprtCode, 'fs_div': fsDiv}
    data = requestData(apiPath, params=params)

    # sj_nm = ['재무상태표', '손익계산서', '포괄손익계산서', '현금흐름표', '자본변동표']

    dataDict = {}
    sjNmList = []

    if data['status'] == '000':
        for x in data['list']:
            if x['sj_nm'] not in sjNmList:
                sjNmList.append(x['sj_nm'])
            if x['sj_nm'] in dataDict:
                dataDict[x['sj_nm']][x['account_id']] = x['bfefrmtrm_amount']
            else:
                dataDict[x['sj_nm']] = {}
            if x['sj_nm'] == '손익계산서':
                print(x)
        print(dataDict)