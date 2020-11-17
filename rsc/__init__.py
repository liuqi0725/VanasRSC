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

from rsc.config import config,basedir
from celery import Celery

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化蓝图
    register_blueprint(app)
    return app

def make_celery(app=None):
    import os

    app = app or create_app(os.getenv('VANAS_PROJECT_ENV') or 'default')

    # 关键点，往celery推入flask信息，使得celery能使用flask上下文
    # app.app_context().push()

    celery = Celery(app.import_name)
    celery.conf.update(app.config['CELERY_CONFIG'])

    class ContextTask(celery.Task):
        # 将app_context 包含在celery.Task中，这样让其他的Flask扩展也能正常使用
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def register_blueprint(app):
    from rsc.api import blueprint
    for bp in blueprint:
        app.register_blueprint(bp)