# coding=utf-8
from flask import Blueprint

# 1、创建蓝图对象
api = Blueprint('api', __name__)


# 2、使用蓝图对象注册路由
@api.route('/', methods=['GET', 'POST'])
def index():

    return 'hello'
