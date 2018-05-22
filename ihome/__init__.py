# coding=utf-8
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from ihome.utils.commons import RegexConvter
from config import config_dict

db = SQLAlchemy()
redis_store = None


# 工厂方法：传入不同的参数，返回不同的对象
def create_app(config_name):
    app = Flask(__name__)
    # 获取配置类
    config_cls = config_dict[config_name]
    app.config.from_object(config_cls)
    # db对象进行app关联
    db.init_app(app)

    # 创建redis数据窟链接对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    # 开启csrf防护
    CSRFProtect(app)

    # session信息的储存
    Session(app)

    # 添加路由转换器
    app.url_map.converters['re'] = RegexConvter

    # 注册蓝图对象
    from ihome.api_1_0.index import api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    from ihome.web_html import html
    app.register_blueprint(html)
    return app
