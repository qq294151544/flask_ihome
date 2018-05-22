# coding=utf-8
from . import api
from flask import current_app


# 2、使用蓝图对象注册路由
@api.route('/', methods=['GET', 'POST'])
def index():
    # current_app.logger.fatal('Fatal Message')
    return 'hello'
