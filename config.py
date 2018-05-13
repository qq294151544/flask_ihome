# coding=utf-8
import redis


class Config(object):
    '''工程配置信息'''
    SECRECT_KEY = '1+LWdsiotKtsOYb9/frWRRw0JGLlQUsmLn36Foxp4+p0clIIHhjnoIY1iGR1UoIt'
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # 配置flask_session
    SESSION_TYPE = 'redis'  # 指定session保存到redis里
    SESSION_USE_SIGNER = True  # 让cookie中的session_id被加密处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用redis实例
    PERMANENT_SESSION_LIFETIME = 86400 * 2  # 设置有效期，单位为秒


class DevelopmentConfig(Config):
    '''开发环境配置类'''
    DEBUG = True


class ProductionConfig(Config):
    '''生产环境配置类'''
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome'


class TestingConfig(Config):
    '''测试环境配置类'''
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome'
    # 开启测试标志
    TESTING = True

config_dict={
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig
}