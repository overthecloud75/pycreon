import logging

from dart.util import requestData

logger = logging.getLogger(__name__)
'''
    단일회사 전체 재무제표

    reprtCode 
        - 1분기보고서 : 11013
        - 반기보고서 : 11012
        - 3분기보고서 : 11014
        - 사업보고서 : 11011
'''
def fnlttSinglAcntAll(corpCode='00126380', bsnsYear=2018, reprtCode=11012, fsDiv='OFS', terms={}):
    apiPath = 'fnlttSinglAcntAll'
    params = {'corp_code': corpCode, 'bsns_year': bsnsYear, 'reprt_code': reprtCode, 'fs_div': fsDiv}
    data = requestData(apiPath, params=params)

    # sj_nm = ['재무상태표', '손익계산서', '포괄손익계산서', '현금흐름표', '자본변동표']

    dataDict = {}
    sjNmList = []
    accountIdDict = {}
    accountNmDict = {}

    if data is None:
        status = 'error'
    elif data['status'] == '000':
        for x in data['list']:
            if x['sj_nm'] not in sjNmList:
                sjNmList.append(x['sj_nm'])

            if x['sj_nm'] in dataDict:
                dataDict[x['sj_nm']][x['account_nm']] = x['thstrm_amount']
                if x['account_id'] not in accountIdDict[x['sj_nm']]:
                    accountIdDict[x['sj_nm']].append(x['account_id'])
                if x['account_nm'] not in accountNmDict[x['sj_nm']]:
                    accountNmDict[x['sj_nm']].append(x['account_nm'])
            else:
                dataDict[x['sj_nm']] = {}
                dataDict[x['sj_nm']][x['account_nm']] = x['thstrm_amount']
                accountIdDict[x['sj_nm']] = [x['account_id']]
                accountNmDict[x['sj_nm']] = [x['account_nm']]

            if x['account_id'] in terms:
                if x['account_nm'] not in terms[x['account_id']]:
                    terms[x['account_id']].append(x['account_nm'])
            else:
                terms[x['account_id']] = [x['account_nm']]
        status = data['status']
        logger.info('status: %s, corpCode: %s, year: %s, reprtCode: %s' %(status, corpCode, str(bsnsYear), str(reprtCode)))
    else:
        status = data['status']
        logger.warn('status: %s, corpCode: %s, year: %s, reprtCode: %s' %(status, corpCode, str(bsnsYear), str(reprtCode)))

        # print(sjNmList)
        # print(accountIdDict)
        # print(accountNmDict)

    return dataDict, terms, status