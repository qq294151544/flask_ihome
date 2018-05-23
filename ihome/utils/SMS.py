# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf0708635e4ce001638acc43691b22'

# ���ʺ�Token
accountToken = '2ee0274286a24cb0aa24df511b0d503c'

# Ӧ��Id
appId = '8aaf0708635e4ce001638acc43be1b28'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id
class CCP(object):
    def __init__(self):
        # ��ʼ��REST SDK
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    def send_template_sms(self,to, datas, tempId):

        result = self.rest.sendTemplateSMS(to, datas, tempId)

        if result.get('statusCode') == '000000':
            return 1 #���ͳɹ�
        else:
            return 0 #����ʧ��


if __name__ == '__main__':
   CCP().send_template_sms('18670582657', ['232312', 5], 1)
