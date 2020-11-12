# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : exception.py
# @Created  : 2020/11/12 10:58 上午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

class UnKonwImageAccessCode(Exception):

    def __init__(self , access_code):
        self.access_code = access_code

    def __str__(self):
        return "未知的 access_code : {}".format(self.access_code)