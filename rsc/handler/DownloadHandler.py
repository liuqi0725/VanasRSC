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

from enum import Enum
import os
import time

from flask import current_app
from vanaspyhelper.LoggerManager import log

from rsc.core.ErrorCode import AppErrorCode
from rsc.handler.RequestHandler import download_file_as_stream, get_file_stream, callback
from vanaspyhelper.util.file import fileExist,makeDir
from vanaspyhelper.util.request import json_res_failure,json_res_success

class DownloadTaskType(Enum):

    IMAGE = "download_image"
    VIDEO = "download_kindle_video"
    AUDIO = "download_kindle_audio"
    PDF = "download_pdf"
    txt = "download_txt"
    KINDLE = "download_kindle_file"


class CreateCallbackDataError(Exception):
    pass

class DownloadHandler():

    def download(self, type:DownloadTaskType, id, url:str, filename:str, client_name:str, resource_type:str, callback_url:str):
        """
        参数参考 各下载文件 api
        :param type:
        :param id:
        :param url:
        :param filename:
        :param client_name:
        :param resource_type:
        :param callback_url:
        :return:
        """

        try:
            # 获取本地保存路径
            local_save = self._get_local_save_path(client_name, resource_type, filename)
            # 查询文件是否存在
            if fileExist(local_save):
                log.warning("下载文件： 文件已存在。请勿重复下载! URL: %s , LOCAL: %s", url, local_save)
                # 存在就立即触发 成功回调
                callback_data = self._create_success_callback_data(id, local_save, type)
            else:
                # 发送下载请求
                try:
                    download_file_as_stream(get_file_stream(url), local_save, filename)
                    callback_data = self._create_success_callback_data(id, local_save, type)
                except Exception as e:
                    log.exception("下载文件: 失败! URL:{}".format(url), exc_info=True)
                    callback_data = json_res_failure("下载文件: 失败! ID:{} , URL:{}".format(id, url),AppErrorCode.DOWNLOAD_ERROR.value, str(e))
        except CreateCallbackDataError as e:
            log.exception("下载文件: ID: {} 创建 callback Data 错误！！".format(url), exc_info=True)
            callback_data = json_res_failure("下载文件: ID: {} 创建 callback Data 错误！！".format(id),AppErrorCode.CREATE_CALLBACK_DATA_ERROR.value, str(e))
        except Exception as e:
            log.exception("下载文件: ID: {} 未知错误！！".format(id), exc_info=True)
            callback_data = json_res_failure("下载文件: ID: {} 未知错误！！".format(id),AppErrorCode.UNKNOW_ERROR.value, str(e))

        callback(callback_url, callback_data)
        # 返回 callback data 作为 task 返回值
        return callback_data

    def _get_local_save_path(self,client_name:str, resource_type:str , filename:str=None):
        """
        :param client_name:
        :param resource_type:
        :param filename:
        :return:
        """
        from vanaspyhelper.util.common import md5

        download_path = current_app.config['DATA_DOWNLOAD_PATH']
        # 获取当前日期 作为第三层目录
        timedir = time.strftime("%Y%m%d", time.localtime())
        local_save_dir = os.path.join(download_path,client_name,resource_type,timedir)

        makeDir(local_save_dir,True)

        if filename is None:
            # 用时间戳 + md5 作为文件名
            filename = md5(str(time.time())) + ".jpg"

        local_save_path = os.path.join(local_save_dir, filename)

        return local_save_path

    def _create_access_code(self,local_save):
        """
        创建访问 code
        :param local_save:
        :return:
        """
        from rsc.config import aes
        return aes.encrypt(local_save)

    def _create_success_callback_data(self,id, local_save, type:DownloadTaskType):

        try:
            # 创建 access_code
            access_code = self._create_access_code(local_save)

            res = {
                "id": id,
                "access_code": access_code,
                "task": type.value,
            }
            # 组装成功回调数据
            return json_res_success(res)
        except Exception as e:
            raise CreateCallbackDataError(e)



def get_token_handler():
    """
    获取新 token
    :return:
    """

    from vanaspyhelper.util.request import vanas_get_token

    try:
        client_id = current_app.conifg['CLIENT_ID']
        secrect_key = current_app.conifg['CLIENT_SECRET_KEY']

        try:
            res = vanas_get_token(client_id, secrect_key)
            if res['success']:
                current_app.config['access_token'] = res['data']['access_token']
                log.info("获取 token。 access_token: %s",current_app.config['access_token'])
            else:
                log.error("获取 token。 失败! result : %s",res)
        except:
            log.exception("获取 token，获取 vanas_get_token 错误！", exc_info=True)
    except:
        log.exception("获取 token，获取 Client_id, secrect_key 错误！",exc_info=True)




