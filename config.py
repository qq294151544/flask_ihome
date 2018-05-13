#coding =utf-8
import redis


class Config(object):
    '''配置工程信息'''
    DEBUG = True
    SECRET_KEY = 'qqp9IhqYgyKOslo6WkESzmQPjLSS3s6jBL880hc/7eOlETQfeqXDKsww1RiOHZu9'
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306//ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭数据追踪

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask_session配置
    SESSION_TYPE = 'redis'  # 指定session保存到redis中
    SESSION_USE_SIGER = True  # 让cookie中的session_id被加密处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用redis实例
    PERMANENT_SESSION_LIFETIME = 86400 * 2  # 设置有效期，单位秒