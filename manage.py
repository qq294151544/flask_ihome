# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect
app = Flask(__name__)


class Config(object):
    '''工程配置信息'''
    DEBUG = True
    SECRECT_KEY = '1+LWdsiotKtsOYb9/frWRRw0JGLlQUsmLn36Foxp4+p0clIIHhjnoIY1iGR1UoIt'
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome'
    SQLAlCHEMY_TRACK_MODIFICATION = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379


app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
CSRFProtect(app)

@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
