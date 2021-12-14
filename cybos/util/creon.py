import win32com.client
import os
from pywinauto import application
import time
import logging

class Creon:
    # 자동 접속
    # http://blog.quantylab.com/creonlogin.html
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' % __name__)
        self.com_obj = win32com.client.Dispatch('CpUtil.CpCybos')

    def kill_client(self):

        os.system('taskkill /IM coStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%coStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    def connect(self, id=None, pwd=None, pwdcert=None):
        if not self.connected():
            self.disconnect()
            self.kill_client()
            app = application.Application()
            app.start(
                'C:\CREON\STARTER\coStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwdcert} /autostart'.format(id=id, pwd=pwd, pwdcert=pwdcert
                )
            )
        while not self.connected():
            self.logger.warn('connecting to server')
            time.sleep(1)
        self.logger.info('connected to server')
        return True

    def connected(self):
        b_connected = self.com_obj.IsConnect
        if b_connected == 0:
            return False
        return True

    def disconnect(self):
        if self.connected():
            self.com_obj.PlusDisconnect()

    def waitForRequest(self):
        remainCount = self.com_obj.GetLimitRemainCount(1)
        if remainCount <= 0:
            time.sleep(self.com_obj.LimitRequestRemainTime / 1000)

    #@property
    #def IsConnect(self):
    #    return self.com_obj.IsConnect

    @property
    def ServerType(self):
        return self.com_obj.ServerType

    @property
    def LimitRequestRemainTime(self):
        return self.com_obj.LimitRequestRemainTime

    def GetLimitRemainCount(self, limitType):
        value = self.com_obj.GetLimitRemainCount(limitType)
        return value

