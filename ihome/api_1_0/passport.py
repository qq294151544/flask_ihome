# coding=utf-8
# 此文件定义用户登陆注册有关api
import re

import redis

from ihome import redis_store, db
from ihome.models import User
from ihome.utils.response_code import RET
from . import api
from flask import request, jsonify, current_app, session


@api.route('/users', methods=['POST'])
def register():
    '''
    1、接收参数（手机号，短信验证码，密码）并验证
    2、从redis中获取短信验证码，如果获取不到说明过期
    3、对比短信验证码
    4、创建User对象并保存注册用户的信息
    5、把注册信用户信息添加进数据库
    6、返回应答，注册成功
    '''
    # 1、接收参数（手机号，短信验证码，密码）并验证
    req_dict = request.json
    mobile = req_dict.get('mobile')
    sms_code = req_dict.get('sms_code')
    password = req_dict.get('password')

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r"^1[356789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码格式错误')

    # 2、从redis中获取短信验证码，如果获取不到说明过期
    try:
        real_sms_code = redis_store.get('smscode:%s' % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取短信验证码失败')
    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码已过期')

    # 3、对比短信验证码
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码错误')
    # 判断手机号是否已经被注册
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg='手机已被注册')

    # 4、创建User对象并保存注册用户的信息
    user = User()
    user.mobile = mobile
    user.name = mobile
    # todo:密码加密
    user.password = password

    # 5、把注册信用户信息添加进数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存用户信息失败')
    # 记住用户登陆状态
    session['user_id'] = user.id
    session['user_name'] = user.name
    session['mobile'] = mobile

        # 6、返回应答，注册成功
    return jsonify(errno=RET.OK, errmsg='注册成功')


@api.route('/sessions', methods=['POST'])
def login():
    '''
    用户登陆
    1、接收参数（手机号，密码），进行校验
    2、根据手机号查询User的信息，若查不到说明用户不存在
    3、校验登陆密码是否正确
    4、记住用户的登陆状态
    5、返回应答
    '''
    # 1、接收参数（手机号，密码），进行校验
    req_dict = request.json
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 2、根据手机号查询User的信息，若查不到说明用户不存在
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    # 3、校验登陆密码是否正确
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='登陆密码错误')

    # 4、记住用户的登陆状态（用session保存）
    session['user_id'] = user.id
    session['user_name'] = user.name
    session['mobile'] = mobile

    # 5、返回应答
    return jsonify(errno=RET.OK, errmsg='登陆成功')
