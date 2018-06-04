# coding=utf-8
import functools

from flask import session, jsonify, g
from werkzeug.routing import BaseConverter

from ihome.utils.response_code import RET


class RegexConvter(BaseConverter):
    '''自定义路由转换器类'''

    def __init__(self, url_map, regex):
        super(RegexConvter, self).__init__(url_map)
        # 保存转换器匹配规则
        self.regex = regex


# 自定义登陆验证装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 进行登陆验证
        user_id = session.get('user_id')
        if user_id:
            # 用户已经登陆，调用视图函数
            # 使用g变量临时保存登陆用户的id，g变量中的内容可以在每次请求开始到请求范围内使用
            # 之所以使用g变量临时保存登陆用户的id，是为了在视图中获取user_id时候不再取session中读取
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            # 用户未登录
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')

    return wrapper
