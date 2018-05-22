# coding=utf-8
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from ihome.utils.commons import RegexConvter
from config import config_dict
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
redis_store = None


def set_logging(log_level):
    # 设置日志的记录等级
    logging.basicConfig(level=log_level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 工厂方法：传入不同的参数，返回不同的对象
def create_app(config_name):
    app = Flask(__name__)
    # 获取配置类
    config_cls = config_dict[config_name]

    #日志的存储设置
    set_logging(config_cls.LOG_LEVEL)

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
