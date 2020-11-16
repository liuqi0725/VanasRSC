# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : ImageService.py
# @Created  : 2020/11/12 10:48 上午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------
import os
from flask import current_app
from vanaspyhelper.LoggerManager import log
from rsc.core.exception import UnKonwImageAccessCode, AttributeNotFoundInJsonError
from rsc.handler.DownloadHandler import DownloadTaskType
from rsc.celery_task import download_file

mdict = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp'
}

class ImageService():

    def process_download_request(self,json_data):
        """
        下载文件
        :param json_data: 参看api.image#download_image 参数说明
        :return:
        """
        try:
            id = self._get_json_param(json_data, "id")
            url = self._get_json_param(json_data, "url")
            priority = self._get_json_param(json_data, "priority",nullable=True, default=5)
            client_name = self._get_json_param(json_data, "client_name")
            source_name = self._get_json_param(json_data, "source_name")
            filename = self._get_json_param(json_data, "filename", nullable=True)
            callback = self._get_json_param(json_data, "callback")
            log.info("处理下载图像数据请求: 参数解析完成. client_name: %s , id: %s ", client_name, id)
        except:
            raise

        # 添加到下载任务
        log.info("处理下载图像数据请求: 添加【下载图像】任务到队列. client_name: %s , id: %s ", client_name, id)
        download_file.delay(DownloadTaskType.IMAGE.value, id, url, client_name, source_name, callback, filename)

    def _get_json_param(self,json_data:dict, attr_name:str ,default=None, nullable:bool=False):
        """
        获取 json 入参的属性
        :param json_data:   json 数据
        :param attr_name:   属性名称
        :param default:     默认值，仅当 nullable 为True 时生效
        :param nullable:    是否允许为空.
        :return:
        """

        val = None
        if attr_name in json_data:
            val = json_data[attr_name]
        else:
            if not nullable:
                raise AttributeNotFoundInJsonError(json_data,attr_name)
        return val




    def get_image(self,access_code):
        """
        获取图片
        :param access_code: 访问码
        :return: (image_data,mime)
        """
        from rsc.config import aes
        try:
            imgPath = aes.decrypt(access_code)
        except:
            raise UnKonwImageAccessCode(access_code)

        if not os.path.exists(imgPath):
            imgPath = current_app.config['DEFAULT']['IMAGE']

        mime = mdict[((imgPath.split('/')[-1]).split('.')[1])]

        image_data = None
        try:
            with open(imgPath, 'rb') as f:
                image_data = f.read()
        finally:
            f.close()

        return (image_data,mime)


