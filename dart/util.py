import os
import requests
import json
import zipfile
from xml.etree.ElementTree import parse

from config.publicconfig import DART_URL, DART_SAVE_PATH
from config.privateconfig import DART_KEY

def requestData(apiPath, verb='GET', dataType='json', data=None, params=None):
    '''
        dataType = json -> data 반환
        dataType = xml -> binaryfile을 zip으로 변환 후 unzip 진행
    '''
    urlPath = DART_URL + apiPath + '.' + dataType
    if params:
        params['crtfc_key'] = DART_KEY
    else:
        params = {'crtfc_key': DART_KEY}
    try:
        r = requests.request(verb, urlPath, json=data, params=params, timeout=5.0)
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
                if os.path.exists(DART_SAVE_PATH):
                    pass
                else:
                    os.mkdir(DART_SAVE_PATH)
                fileName = apiPath + '.zip'
                binarySave(fileName, content=r.content)
                unZip(fileName)
                return None
        else:
            msg = str(r.status_code) + ' ' + apiPath + ' ' + str(r.text)
            print(msg)
            return None

def binarySave(fileName, content=b''):
    f = open(os.path.join(DART_SAVE_PATH, fileName), 'wb')
    f.write(content)
    f.close()

def unZip(fileName):
    xlmZip = zipfile.ZipFile(os.path.join(DART_SAVE_PATH, fileName))
    xlmZip.extractall(DART_SAVE_PATH)
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
    tree = parse(os.path.join(DART_SAVE_PATH, 'corpCode.xml'))
    root = tree.getroot()

    corpCodeList = root.findall('list')
    return corpCodeList


