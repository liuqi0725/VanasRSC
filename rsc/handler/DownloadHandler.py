# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : DownloadHandler.py
# @Created  : 2020/11/12 11:27 上午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

import enum as Enum

class DownloadTaskType(Enum):

    IMAGE = "download_image"
    VIDEO = "download_kindle_video"
    AUDIO = "download_kindle_audio"
    PDF = "download_pdf"
    txt = "download_txt"
    KINDLE = "download_kindle_file"

class DownloadHandler():

    def download(self, type:DownloadTaskType, id, url:str, client_name:str, resource_type:str, callback:str):
        """
        参数参考 各下载文件 api
        :param type:
        :param id:
        :param url:
        :param client_name:
        :param resource_type:
        :param callback:
        :return:
        """

        # 查询文件是否存在

        # 存在就立即回调

        # 下载

        # 回调

        return True

    def callback(self):

        # 如果重试次数 > 20 ，视为该地址已经死亡

        # 组装回调数据

        # 回调地址

        # 错误,添加回调到任务

        pass
