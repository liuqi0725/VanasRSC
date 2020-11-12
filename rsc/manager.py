# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : manager.py
# @Created  : 2020/11/9 3:49 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : flask框架项目启动运行文件
# -------------------------------------------------------------------------------

import os

from rsc import create_app

app = create_app(os.getenv('VANAS_RSC_ENV') or 'default')

if __name__ == '__main__':
    app.run()