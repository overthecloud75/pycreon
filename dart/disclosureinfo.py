from .util import requestData

def corpCode():
    apiPath = 'corpCode'
    requestData(apiPath, dataType='xml')


