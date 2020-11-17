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

from rsc.celerymanager import celery

@celery.task()
def download_file(task_type:str, id, url:str, client_name:str, source_name:str, callback:str,filename:str=None):
    """
    下载文件任务
    :param task_type: DownloadTaskType 枚举类型的值
    :param id: task_id 客户端传递的
    :param url: 文件 url
    :param filename: 客户端传递 filename 可以为空
    :param source_name: 客户端传递的 client_name 用于区分不同客户端的文件 .
            比如 client_name = "vanas" , resource_type = "study"  服务器会生成将下载的文件存放在 vanas/study 目录下
    :param resource_type: 客户端传递的 resource_type 用于区分文件目录
    :param callback: 回调地址
    :return:
    """
    from rsc.handler.DownloadHandler import DownloadHandler

    handler = DownloadHandler()
    # 下载
    result = handler.download(task_type, id, url, filename , client_name, source_name, callback)
    return result

@celery.task()
def retry_callback(url:str, data:dict, retry:int):
    """
    回调重试
    :return:
    """
    from rsc.handler.RequestHandler import callback

    callback(url, data , retry)
    return None

@celery.task()
def get_token():
    """
    每 12 小时获取一次新 token
    :return:
    """
    from rsc.handler.DownloadHandler import get_token_handler

    get_token_handler()