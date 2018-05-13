# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect
from flask_session import Session

app = Flask(__name__)


class Config(object):
    '''工程配置信息'''
    DEBUG = True
    SECRECT_KEY = '1+LWdsiotKtsOYb9/frWRRw0JGLlQUsmLn36Foxp4+p0clIIHhjnoIY1iGR1UoIt'
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome'
    SQLAlCHEMY_TRACK_MODIFICATION = False
    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # 配置flask_session
    SESSION_TYPE = 'redis'  # 指定session保存到redis里
    SESSION_USE_SIGNER = True  # 让cookie中的session_id被加密处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用redis实例
    PERMANENT_SESSION_LIFETIME = 86400 * 2  # 设置有效期，单位为秒


app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
CSRFProtect(app)
Session(app)


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
