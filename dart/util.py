import os
import requests
import json
import zipfile
from xml.etree.ElementTree import parse

from config.publicconfig import DARTURL, DARTSAVEPATH
from config.privateconfig import DARTKEY

def requestData(apiPath, verb='GET', dataType='json', data=None, params=None):
    '''
        dataType = json -> data 반환
        dataType = xml -> binaryfile을 zip으로 변환 후 unzip 진행
    '''
    urlPath = DARTURL + apiPath + '.' + dataType
    if params:
        params['crtfc_key'] = DARTKEY
    else:
        params = {'crtfc_key': DARTKEY}
    try:
        r = requests.request(verb, urlPath, json=data, params=params, timeout=3.0)
    except Exception as e:
        print(e)
    else:
        if r.status_code == 200:
            if dataType == 'json':
                try:
                    responseJson = json.loads(r.text)
                except Exception as e:
                    print(e)
                    return None
                else:
                    return responseJson
            else:
                if os.path.exists(DARTSAVEPATH):
                    pass
                else:
                    os.mkdir(DARTSAVEPATH)
                fileName = apiPath + '.zip'
                binarySave(fileName, content=r.content)
                unZip(fileName)
                return None
        else:
            msg = str(r.status_code) + ' ' + apiPath + ' ' + str(r.text)
            print(msg)
            return None

def binarySave(fileName, content=b''):
    f = open(os.path.join(DARTSAVEPATH, fileName), 'wb')
    f.write(content)
    f.close()

def unZip(fileName):
    xlmZip = zipfile.ZipFile(os.path.join(DARTSAVEPATH, fileName))
    xlmZip.extractall(DARTSAVEPATH)
    xlmZip.close()

def corpCodeToList():
    '''
        <result>
            <list>
                <corp_code>00434003</corp_code>
                <corp_name>다코</corp_name>
                <stock_code> </stock_code>
                <modify_date>20170630</modify_date>
            </list>
    '''
    # https://wikidocs.net/21140
    tree = parse(os.path.join(DARTSAVEPATH, 'corpCode.xml'))
    root = tree.getroot()

    corpCodeList = root.findall('list')
    return corpCodeList


