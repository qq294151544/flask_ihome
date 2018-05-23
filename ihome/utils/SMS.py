# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf0708635e4ce001638acc43691b22'

# 主帐号Token
accountToken = '2ee0274286a24cb0aa24df511b0d503c'

# 应用Id
appId = '8aaf0708635e4ce001638acc43be1b28'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
class CCP(object):
    def __init__(self):
        # 初始化REST SDK
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    def send_template_sms(self,to, datas, tempId):

        result = self.rest.sendTemplateSMS(to, datas, tempId)

        if result.get('statusCode') == '000000':
            return 1 #发送成功
        else:
            return 0 #发送失败


if __name__ == '__main__':
   CCP().send_template_sms('18670582657', ['232312', 5], 1)
