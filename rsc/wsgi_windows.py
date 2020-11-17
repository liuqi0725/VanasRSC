# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : manager.py
# @Created  : 2020/11/9 3:49 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : flask框架项目启动运行文件, 在 windows 下使用 Tornado 启动
#
# -------------------------------------------------------------------------------
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
print("curPath >>",curPath)

parentPath = os.path.split(curPath)[0]
print("parentPath >>",parentPath)

# rootPath = os.path.split(parentPath)[0]
# print("rootPath >>",rootPath)

sys.path.append(parentPath)
# print("添加项目路径 >>",parentPath)

from rsc import create_app
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

# 创建 flask
app = create_app(os.getenv('VANAS_PROJECT_ENV') or 'default')
s = HTTPServer(WSGIContainer(app))
s.listen(9900) # 监听 9900 端口
print("Server Run at 9900.")
IOLoop.current().start()
