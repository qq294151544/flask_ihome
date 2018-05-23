# coding=utf-8
# 该蓝图给浏览器提供静态页面
from flask import Blueprint
from flask import current_app, make_response
from flask_wtf.csrf import generate_csrf

html = Blueprint('html', __name__)


# @html.route('/<file_name>')
@html.route("/<re('.*'):file_name>")
def get_static_html(file_name):
    # 获取静态文件目录下的静态文件内容并返回给浏览器
    if file_name == '':
        # 如果用户访问路径为空，则默认访问首页，返回index.html
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        # 当浏览器访问一个网站的时候，浏览器会自动访问网站下的一个favicon文件，网站图标
        file_name = 'html/' + file_name
    response = make_response(current_app.send_static_file(file_name))

    # 生成一个csrf_token cookie
    csrf_token = generate_csrf()
    response.set_cookie('csrf_token', csrf_token)
    return response
