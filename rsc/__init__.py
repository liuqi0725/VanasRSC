# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : __init__.py.py
# @Created  : 2020/11/12 10:02 上午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 初始化 flask，celery
# -------------------------------------------------------------------------------


from flask import Flask
from celery import Celery
from rsc.config import config,basedir

# Celery相关配置
CELERY_RESULT_BACKEND= "redis://localhost:6379/0"
CELERY_BROKER_URL= "redis://localhost:6379/0"

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.app_context().push()

    # 初始化蓝图
    register_blueprint(app)
    return app

def make_celery(app=None):
    import os

    app = app or create_app(os.getenv('VANAS_RSC_ENV')or 'default')
    celery=Celery(__name__)
    celery.conf.update(app.config['CELERY_CONFIG'])

    TaskBase= celery.Task
    class ContextTask(TaskBase):
        abstract= True
        def __call__(self,*args,**kwargs):
            with app.app_context():
                    return TaskBase.__call__(self,*args,**kwargs)

    celery.Task = ContextTask
    return celery

def register_blueprint(app):
    from rsc.api import blueprint
    for bp in blueprint:
        app.register_blueprint(bp)