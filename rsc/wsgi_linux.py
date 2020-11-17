# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : manager.py
# @Created  : 2020/11/9 3:49 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : flask框架项目启动运行文件, 使用 gunicorn 启动
#
#               启动说明: 在 VanasRSC 目录
#               gunicorn -w 4 -b 127.0.0.1:4000 run:app
#               -w 4 指预定义的工作进程数为4
#               -b 127.0.0.1:4000  指绑定地址和端口  指定任意为 0.0.0.0
#               run 是 python 文件  app 是 run 文件内要运行的 flask 对象实例名称
# -------------------------------------------------------------------------------
import os
from rsc import create_app

print(os.getenv('VANAS_PROJECT_ENV'))
# 创建 flask
app = create_app(os.getenv('VANAS_PROJECT_ENV') or 'default')

app.logger.info("Vanas Resources Cloud create app.")
