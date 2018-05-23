# coding=utf-8

from . import api
from ihome.utils.captcha.captcha import captcha
from flask import make_response, request, jsonify, current_app
from ihome.utils.response_code import RET
from ihome import redis_store, constants
import json
import re
import random
from ihome.utils.SMS import CCP


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


@api.route('/sms_code', methods=['POST'])
def send_sms_code():
    '''发送短信验证码'''
    # 1、接收参数（1.手机号，图片验证码，图片验证码标识）并进行校验
    req_dict = request.json
    mobile = req_dict.get('mobile')
    image_code = req_dict.get('image_code').upper()
    image_code_id = req_dict.get('image_code_id')

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r"^1[356789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码格式错误')

    # 2、从redis中获取图片验证码（如果获取不到，说明图片验证码过期）
    try:
        real_image_code = redis_store.get('imagecode:%s' % image_code_id)
        print real_image_code
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取图片验证码失败')

    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg='图片验证码已过期')

    # 3、对比图片验证码
    if real_image_code != image_code:
        print image_code
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')

    # 4、使用云通讯发送短信验证码
    # 4.1、随机生成一个6位的短信验证码 (%06s,格式化输出，字符串s有六位，不足六位补0）
    sms_code = "%06s" % random.randint(0, 999999)
    # 4.2、发送短信验证码
    try:
        res = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES / 60], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信失败')
    if res != 1:
        # 发送短信验证码失败
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信验证码失败')
    # 4.3、保存短信验证码在redis中
    try:
        redis_store.set('smscode:%s' % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='保存短信验证码失败')

    # 5、返回应答发送成功
    return jsonify(errno=RET.OK, errmsg='手机验证码发送成功')
