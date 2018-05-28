# coding=utf-8
# 次文件定义用户个人相关api接口
from flask import session, current_app, jsonify, request

from ihome import db, constants
from ihome.models import User
from ihome.utils.image_storage import storage_image
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
    '''   resp = {
            'user_id': self.id,
            'username': self.name,
            'avatar_url': constants.QINIU_DOMIN_PREFIX + self.avatar_url if user.avatar_url else '',
        }
    '''
    return jsonify(errno=RET.OK, errmsg='ok', data=User.to_dict())


@api.route('/user/avatar', methods=['POST'])
def set_user_avatar():
    '''
    设置用户头像信息：
    1、获取用户上传头像的对象
    2、头像文件上传到七牛云
    3、设置用户头像记录
    4、返回应答，上传成功
    '''

    # 1、获取用户上传头像的对象
    file = request.files.get('avatar')
    if not file:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少数据')

    # 2、头像文件上传到七牛云
    try:
        key = storage_image(file.read())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传用户头像失败')
    # 3、设置用户头像记录
    user_id = session.get('user_id')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')
    # 设置用户头像地址
    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='设置用户头像记录')

    # 4、返回应答，上传成功
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='上传头像成功', data={'avatar_url': avatar_url})


@api.route('/user/name', methods=['PUT'])
def set_user_name():
    '''
    设置用户的用户名
    todo：判断用户是否登陆
    1、接收参数（用户名）进行校验
    2、判断用户名是否重复
    3、设置用户的用户名
    4、返回应答，设置成功
    '''
    # 1、接收参数（用户名）进行校验
    req_dict = request.json
    username = req_dict.get('username')
    if not username:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 2、判断用户名是否重复
    try:
        user = User.query.filter(User.name == username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg='用户名已存在')

    # 3、设置用户的用户名
    user.name == username
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='设置用户名失败')


    # 4、返回应答，设置成功
    return jsonify(errno=RET.OK, errmsg='设置用户名成功')
