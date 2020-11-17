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


class AppErrorCode(Enum):
    DOWNLOAD_ERROR = 5001
    CREATE_CALLBACK_DATA_ERROR = 5002

    UNKNOW_ERROR = 5099