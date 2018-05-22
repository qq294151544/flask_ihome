# coding=utf-8
# 该蓝图给刘看齐提供静态页面
from flask import Blueprint
from flask import current_app

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

    return current_app.send_static_file(file_name)
