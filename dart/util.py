import os
import requests
import json
import zipfile

from config.publicconfig import DARTURL, DARTSAVEPATH
from config.privateconfig import DARTKEY

def requestData(apiPath, verb='GET', ext='json', data=None, params=None, headers=None):
    urlPath = DARTURL + apiPath + '.' + ext
    if params:
        params['crtfc_key'] = DARTKEY
    else:
        params = {'crtfc_key': DARTKEY}
    try:
        r = requests.request(verb, urlPath, json=data, params=params, headers=headers, timeout=3.0)
    except Exception as e:
        print(e)
    else:
        if r.status_code == 200:
            if ext == 'json':
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
                f = open(os.path.join(DARTSAVEPATH, fileName), 'wb')
                f.write(r.content)
                f.close()
                unZip(fileName)
                return None
        else:
            msg = str(r.status_code) + ' ' + apiPath + ' ' + str(r.text)
            print(msg)
            return None

def unZip(fileName):
    xlmZip = zipfile.ZipFile(os.path.join(DARTSAVEPATH, fileName))
    xlmZip.extractall(DARTSAVEPATH)
    xlmZip.close()


