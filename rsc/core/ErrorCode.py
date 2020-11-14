# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : ErrorCode.py
# @Created  : 2020/11/12 9:00 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

from enum import Enum

from flask import current_app

class AppErrorCode(Enum):

    DOWNLOAD_ERROR = int(current_app.config['ERROR_CODE_REX'].format("01"))
    CREATE_CALLBACK_DATA_ERROR = int(current_app.config['ERROR_CODE_REX'].format("02"))

    UNKNOW_ERROR = int(current_app.config['ERROR_CODE_REX'].format("99"))