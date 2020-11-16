# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : RequestHandler.py
# @Created  : 2020/11/2 6:10 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------
import time
from vanaspyhelper.LoggerManager import log
from vanaspyhelper.util.request import build_proxies, do_get, get_user_agent_mobile, get_user_agent_remote, request_json
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


class FileDownloadError(Exception):
    pass

class FileDownloadSaveTimeOutError(FileDownloadError):

    def __init__(self,url):
        self.url = url

    def __str__(self):
        return "下载文件，保存下载数据超时. File URL : {}".format(self.url)

class FileDownloadGetFileStreamError(FileDownloadError):

    def __init__(self,url):
        self.url = url

    def __str__(self):
        return "下载文件，获取文件数据量错误. File URL : {}".format(self.url)



class CallBackRetryMaximumError(Exception):
    def __init__(self,url):
        self.url = url

    def __str__(self):
        return "回调地址不可用,重试次数达到上限. URL:{}".format(self.url)


def get_remote_header():
    """
    获取随机的 header
    :return:
    """

    headers = {
        'User-Agent': get_user_agent_remote(),
        'Connection': 'close'
    }

    return headers

def get_mobile_header():
    """
    获取手机 headers
    :return:
    """
    headers = {
        'User-Agent': get_user_agent_mobile(),
        'Connection': 'close' # 打开后关闭链接，解决: 1. http 链接过多造成的上限问题。 2.解决服务器产生大量close_wait问题
    }

    return headers

def __get_proxy():
    from flask import current_app
    proxy_enable = current_app.config['REQUEST_PROXY']['enable']

    # if sys.spider_conf.proxy_enable:
    if proxy_enable:
        proxy_ip = current_app.config['REQUEST_PROXY']['ip']
        proxy_port = current_app.config['REQUEST_PROXY']['port']
        proxy_type = current_app.config['REQUEST_PROXY']['type']

        proxies = build_proxies(proxy_ip, proxy_port, proxy_type)
        # proxies = build_proxies(sys.spider_conf.proxy_ip, sys.spider_conf.proxy_port, sys.spider_conf.proxy_type)
    else:
        proxies = None

    return proxies

def get_page_info(url, force_mobile:bool=True):
    """
    获取页面信息
    :param url:
    :param force_mobile: 强制使用手机模式访问 默认 True,headers 将替换为手机的
    :return:
    """
    if force_mobile:
        headers = get_mobile_header()
    else:
        headers = get_remote_header()

    rep = do_get(url, headers=headers ,proxies=__get_proxy())

    if rep is not None:
        rep.encoding = rep.apparent_encoding
        return rep.text

    return None

def get_file_stream(url, force_mobile:bool=True, retry:int=3):
    """
    获取文件流
    :param url:
    :param stream:
    :param force_mobile:
    :param retry 重试次数
    :return:
    """

    if force_mobile:
        headers = get_mobile_header()
    else:
        headers = get_remote_header()

    response = do_get(url, proxies=__get_proxy() ,stream=True, headers=headers)

    if response is None:

        # 重试
        if retry > 0:
            retry -= retry
            log.warning("重新下载文件数据流 ! URL:[{}]".format(url))
            response = get_file_stream(url,force_mobile,retry)
        else:
            raise FileDownloadGetFileStreamError(url)

    return (response,url)

def download_file_as_stream(stream_data , filepath:str , filename:str, retry=3, timeout=600):
    """
    下载文件按进度，按流处理
    :param stream_data: request 请求回来的 content 及 下载 url 【元祖】
    :param filepath: 下载路径，包含文件名
    :param retry: 重试次数 默认 3
    :parma timeout: 超时时间 默认 60 秒
    :return:
    """
    from vanaspyhelper.util.file import removeFile

    stream,url = stream_data

    chunk_size = 1024  # 单次请求最大值
    total_size = int(stream.headers['Content-Length'])  # 内容体总大小
    processed = 0

    start_time = time.time()

    with open(filepath, 'wb') as file:
        try:
            for data in stream.iter_content(chunk_size):
                # 设置 300 秒超时
                if time.time() - start_time > timeout:
                    # 设置为超时
                    raise FileDownloadSaveTimeOutError(url)

                processed += chunk_size
                file.write(data)
                file.flush()

            end_time = time.time() - start_time
            log.info("下载文件 {} 完成，大小:[{}] kb, 耗时:[{}] s".format(filename,str(total_size/1024), str(end_time)))

        except FileDownloadSaveTimeOutError:
            # 超时异常，到需要重新下载
            # 删除文件
            removeFile(filepath)

            if retry > 0:
                retry -= retry
                log.warning("重新根据文件流下载文件到本地 ! URL:[{}] , Local_save:[{}]".format(url,filepath))
                download_file_as_stream(stream_data, filepath , filename, retry, timeout)
            else:
                # 3次重试失败
                raise FileDownloadSaveTimeOutError(url)
        finally:
            # 关闭文件流
            file.close()


def callback(url, data:dict, retry:int=1):
    """
    成功回调
    :param url: 回调地址
    :param data: 回调 json_data
    :param retry: 当前执行的重试次数 默认 1 , 失败后会重新进入队列，并作为入参回传回来
    :return: 回调的 json 字符串
    """
    # 如果重试次数 > 20 ，视为该地址已经无法连接
    if retry > 20:
        raise CallBackRetryMaximumError(url)

    from rsc.celery_task import retry_callback

    try:
        rep = request_json(url,data)
        if(rep['success'] == int(False)):
            retry = retry + 1
            log.error("调用 Callback 失败! 重试次数:{} , URL: {}, RESULT: {} ".format(str(retry),url, rep))
            # 添加到 task 重试
            retry_callback(url,data,retry)
    except CallBackRetryMaximumError as e:
        # 超过最大重试次数
        log.error(str(e))
    except :
        # 异常，添加到 task 重试
        retry_callback(url,data,(retry+1))
