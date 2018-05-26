# coding=utf-8
# 次文件定义用户个人相关api接口
from flask import session, current_app, jsonify

from ihome.models import User
from ihome.utils.response_code import RET
from . import api


@api.route('/user')
def get_user_info():
    '''
    获取用户个人的信息：
    判断用户是否登陆
    1、获取登陆用户id
    2、根据id查询用户信息（如果查不到则用户不存在）
    3、查到数据，组织数据，返回应答
    '''
    # 1、获取登陆用户id
    user_id = session.get('user_id')

    # 2、根据id查询用户信息（如果查不到则用户不存在）
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    # 3、查到数据，组织数据，返回应答
    resp = {
        'user_id': user.id,
        'username': user.name,
        'avatar_url': user.avatar_url
    }
    return jsonify(errno=RET.OK, errmsg='ok', data=resp)
