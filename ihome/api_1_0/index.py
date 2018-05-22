
#coding=utf-8
from . import api
# 2、使用蓝图对象注册路由
@api.route('/', methods=['GET', 'POST'])
def index():

    return 'hello'
