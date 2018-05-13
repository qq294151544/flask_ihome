# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from  flask_wtf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from  flask_migrate import Migrate, MigrateCommand
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
# 创建SQLAlchemy对象
db = SQLAlchemy(app)
# 创建数据库连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# flask-script 数据库迁移
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 开启CSRF防护
CSRFProtect(app)

# 创建session实例
Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # redis_store.set('name', 'ihome') #测试redis成功
    return 'hello'


if __name__ == '__main__':
    app.run()
