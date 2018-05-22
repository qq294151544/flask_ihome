# coding=utf-8

from . import api
from ihome.utils.captcha.captcha import captcha
from flask import make_response, request, jsonify, current_app
from ihome.utils.response_code import RET
from ihome import redis_store, constants


@api.route('/image_code')
def get_image_code():
    '''产生图片验证码'''
    # 1.接收参数（图片验证码标识）并进行校验
    image_code_id = request.args.get('cur_id')
    if not image_code_id:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 2. 产生图片验证码,  1.文件名称，2.验证码文本，3.验证码图片内容
    name, text, content = captcha.generate_captcha()

    # 3.在redis中保存图片验证码
    # redis_store.set('key','value','expires')
    try:
        redis_store.set('imagecode:%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.loger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片验证码失败')

    # 4.返回验证码图片
    response = make_response(content)

    # 指定返回内容的类型
    response.headers['Content-Type'] = 'image/jpg'
    return response
