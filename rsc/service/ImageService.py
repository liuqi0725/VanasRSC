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
from vanaspyhelper.util.crypto import AESTool
from ..core.exception import UnKonwImageAccessCode

mdict = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp'
}

class ImageService():

    def __init__(self):
        aes_key = "Alexliu-Vanas-Resources-Cloud-0725-0627-0819"
        self.aes = AESTool(key=aes_key)

    def get_image(self,access_code):
        """
        获取图片
        :param access_code: 访问码
        :return: (image_data,mime)
        """

        try:
            imgPath = self.aes.decrypt(access_code)
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


