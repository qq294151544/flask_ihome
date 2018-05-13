# coding=utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app,db

app = create_app('development')

# 数据库脚本迁移
manager = Manager(app)
Migrate(app,db)
manager.add_command('db', MigrateCommand)


@app.route('/',methods=['GET','POST'])
def index():
    return 'hello'


if __name__ == '__main__':
    manager.run()
