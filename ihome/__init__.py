# coding=utf-8
from flask import Flask,session
from config import Config
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect
from flask_session import Session
from config import config_dict

db = SQLAlchemy()


# 工厂方法：传入不同的参数，返回不同的对象
def create_app(config_name):
    app = Flask(__name__)
    # 获取配置类
    config_cls = config_dict[config_name]
    app.config.from_object(config_cls)
    # db对象进行app关联
    db.init_app(app)

    # 创建redis数据窟链接对象
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    CSRFProtect(app)

    Session(app)

    return app
