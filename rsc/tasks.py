# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : tasks.py
# @Created  : 2020/11/12 11:12 上午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------

from rsc import make_celery
from rsc.handler.DownloadHandler import DownloadHandler, DownloadTaskType

celery = make_celery(app=None)

@celery.task()
def download_file(type:DownloadTaskType, id, url:str, client_name:str, resource_type:str, callback:str):
    """
    下载文件任务
    :param type: DownloadTaskType 枚举类型
    :param id: task_id 客户端传递的
    :param url: 文件 url
    :param client_name: 客户端传递的 client_name 用于区分不同客户端的文件 .
            比如 client_name = "vanas" , resource_type = "study"  服务器会生成将下载的文件存放在 vanas/study 目录下
    :param resource_type: 客户端传递的 resource_type 用于区分文件目录
    :param callback: 回调地址
    :return:
    """

    handler = DownloadHandler()
    # 下载
    result = handler.download(type, id, url, client_name, resource_type, callback)
    return result

@celery.task()
def retry_callback():
    """
    回调重试
    :return:
    """
    pass