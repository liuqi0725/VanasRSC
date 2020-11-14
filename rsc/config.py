# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : config.py
# @Created  : 2020/11/9 3:35 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 项目的配置文件
# -------------------------------------------------------------------------------

import os
from datetime import timedelta

from vanaspyhelper.util.crypto import AESTool

basedir = os.path.abspath(os.path.dirname(__file__))

global aes

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Vanas-Hanman-Security-KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        # 初始化日志
        from vanaspyhelper.LoggerManager import init_global_logger

        # 要么传入配置路径，要么获取当前目录的上一级 `os.path.dirname(basedir)`
        current_dir_parent = os.path.dirname(basedir)

        if 'APP_LOG_DIR' in app.config:
            log_dir = app.config['APP_LOG_DIR']
        else:
            log_dir = current_dir_parent

        if 'APP_LOG_LEVEL' in app.config:
            log_level = app.config['APP_LOG_LEVEL']
        else:
            log_level = "error"

        from konfig import Config

        # 初始化 aes
        c = Config(app.config['SECURITY_CONF_PATH'])

        global aes
        aes = AESTool(key=c.get_map('AES').get('AES_SECRET_KEY'))

        # 初始化 client_id ,client_secret
        app.config.update(c.get_map('CLIENT_DATA'))

        # 初始化日志对象
        init_global_logger(log_dir, level=log_level, log_prefix="VanasRSC")


class DevelopmentConfig(config):
    DEBUG = True

    # 日志相关
    APP_LOG_DIR = '/Users/alexliu/tmp/vanas_rsc/logs'
    APP_LOG_LEVEL = "debug"

    # 下载
    DATA_DOWNLOAD_PATH = "/Users/alexliu/tmp/vanas_rsc/download"
    # 缓存、临时文件
    DATA_TEMP_PATH = "/Users/alexliu/tmp/vanas_rsc/temp"
    # 运行时
    DATA_RUNTIME_PATH = "/Users/alexliu/tmp/vanas_rsc/runtime"

    # 默认值
    DEFAULT = {
        "IMAGE" : "/Users/alexliu/tmp/vanas_rsc/default_img.jpeg"
    }

    # 错误编码头,防止与其他系统编码重复
    ERROR_CODE_REX = "50{}"

    # 系统安全配置文件路径
    SECURITY_CONF_PATH = '/Users/alexliu/tmp/vanas_rsc/security.ini'

    # celery
    CELERY_CONFIG = {
        # Broker settings.
        "broker_url" : 'redis://:fxredis0725@192.168.0.198:6379/3',      # 使用Redis作为消息代理
        # Result_BACKEND
        "result_backend": 'redis://:fxredis0725@192.168.0.198:6379/4',  # 把任务结果存在了Redis
        # List of modules to import when the Celery worker starts.
        "imports": ('rsc.tasks'),
        # Result serialization format.
        "task_serializer": 'msgpack', # 任务序列化和反序列化使用msgpack方案
        "result_serializer": 'json',  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
        "result_expires": 60 * 60 * 24,  # 任务过期时间
        "accept_content": ['json', 'msgpack'],  # 指定接受的内容类型
        "enable_utc": False,
        "timezone": 'Asia/Shanghai',  # 默认 UTC  当`enable_utc` 不是 UTC 时，需要指定时区
        "worker_prefetch_multiplier": 20, # 默认 4 workder 进程数
        "beat_schedule": {
            # 定时任务
            # 注意：添加定时任务后，调用celery 需要加上 `-B` 参数
            'get-new-token-12-hour': {
                # 每 12 小时获取一次新 token
                'task': 'rsc.tasks.get_token',
                'schedule': timedelta(hours=12),
            },

        }
    }



class TestingConfig(config):
    DEBUG = True

    # 日志相关
    APP_LOG_DIR = '/Users/alexliu/tmp/vanas_rsc/logs'
    APP_LOG_LEVEL = "debug"

    # 下载
    DATA_DOWNLOAD_PATH = "/Users/alexliu/tmp/vanas_rsc/download"
    # 缓存、临时文件
    DATA_TEMP_PATH = "/Users/alexliu/tmp/vanas_rsc/temp"
    # 运行时
    DATA_RUNTIME_PATH = "/Users/alexliu/tmp/vanas_rsc/runtime"

    # 默认值
    DEFAULT = {
        "IMAGE": "/Users/alexliu/tmp/vanas_rsc/default_img.jpeg"
    }

    # 错误编码头,防止与其他系统编码重复
    ERROR_CODE_REX = "50{}"

    # 系统安全配置文件路径
    SECURITY_CONF_PATH = '/Users/alexliu/tmp/vanas_rsc/security.ini'

    # celery
    CELERY_CONFIG = {
        # Broker settings.
        "broker_url": 'redis://:fxredis0725@192.168.0.198:6379/3',  # 使用Redis作为消息代理
        # Result_BACKEND
        "result_backend": 'redis://:fxredis0725@192.168.0.198:6379/4',  # 把任务结果存在了Redis
        # List of modules to import when the Celery worker starts.
        "imports": ('rsc.tasks'),
        # Result serialization format.
        "task_serializer": 'msgpack',  # 任务序列化和反序列化使用msgpack方案
        "result_serializer": 'json',  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
        "result_expires": 60 * 60 * 24,  # 任务过期时间
        "accept_content": ['json', 'msgpack'],  # 指定接受的内容类型
        "enable_utc": False,
        "timezone": 'Asia/Shanghai',  # 默认 UTC  当`enable_utc` 不是 UTC 时，需要指定时区
        "worker_prefetch_multiplier": 20,  # 默认 4 workder 进程数
        "beat_schedule": {
            # 定时任务
            # 注意：添加定时任务后，调用celery 需要加上 `-B` 参数
            'get-new-token-12-hour': {
                # 每 12 小时获取一次新 token
                'task': 'rsc.tasks.get_token',
                'schedule': timedelta(hours=12),
            },

        }
    }

class ProductionConfig(config):
    # 日志相关
    APP_LOG_DIR = '/logs'
    APP_LOG_LEVEL = "info"

    # 下载
    DATA_DOWNLOAD_PATH = "/workdir/download"
    # 缓存、临时文件
    DATA_TEMP_PATH = "/workdir/temp"
    # 运行时
    DATA_RUNTIME_PATH = "/workdir/runtime"

    # 默认值
    DEFAULT = {
        "IMAGE": "/workdir/default_img.jpeg"
    }

    # 错误编码头,防止与其他系统编码重复
    ERROR_CODE_REX = "50{}"

    # 系统安全配置文件路径
    SECURITY_CONF_PATH = '/workdir/security.ini'

    # celery
    CELERY_CONFIG = {
        # Broker settings.
        "broker_url": 'redis://:fxredis0725@192.168.0.198:6379/3',  # 使用Redis作为消息代理
        # Result_BACKEND
        "result_backend": 'redis://:fxredis0725@192.168.0.198:6379/4',  # 把任务结果存在了Redis
        # List of modules to import when the Celery worker starts.
        "imports": ('rsc.tasks'),
        # Result serialization format.
        "task_serializer": 'msgpack',  # 任务序列化和反序列化使用msgpack方案
        "result_serializer": 'json',  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
        "result_expires": 60 * 60 * 24,  # 任务过期时间
        "accept_content": ['json', 'msgpack'],  # 指定接受的内容类型
        "enable_utc": False,
        "timezone": 'Asia/Shanghai',  # 默认 UTC  当`enable_utc` 不是 UTC 时，需要指定时区
        "worker_prefetch_multiplier": 20,  # 默认 4 workder 进程数
        "beat_schedule": {
            # 定时任务
            # 注意：添加定时任务后，调用celery 需要加上 `-B` 参数
            'get-new-token-12-hour': {
                # 每 12 小时获取一次新 token
                'task': 'rsc.tasks.get_token',
                'schedule': timedelta(hours=12),
            },

        }
    }



config= {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}