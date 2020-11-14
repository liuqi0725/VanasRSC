# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : comic.py
# @Created  : 2020/11/2 7:41 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 图像api
# -------------------------------------------------------------------------------

from flask import Blueprint,request
from vanaspyhelper.util.request import E400,render_json,json_res_success
from vanaspyhelper.wraps.token import token_required

image = Blueprint("image" , __name__)

@image.route("/image/download" , methods=['POST'])
@token_required
def download_image():
    """
    下载图像
    post header : {
        Content-Type: application/json,
        access_token: access_token from vans-token-manager
        client_id:    client_id from vans-token-manager conf. create by developers.
    }

    post data :{
        id          : [Not Null] Identifies the ID of the task. when download file over, it will send to client, client will use the ID that save the task status.
        url         : [Not Null] download image url.
        priority    : [Null Enable] download priority . 1~10 , 10 > 9 > ... 1,  DEFAULT: 5.
        client_name : [Not Null] name of client . server will create dir with the name.
        source_name : [Not Null] resources name . server will create dir with the name in `client_name` dir.
        filename    : [Null Enable] Filename for Download file. If None ,that will create by server timestamp and suffix use `.jpg`. DEFAULT: None
        callback    : [Not Null] callback url. when file download over will call client by callback_url. call data example: {
            # only post data
            success : 1,            # success 1 failure 0
            code:      ,            # only failure have code
            msg:       ,            # only failure have code
            data: {
                id :       ,                # Use the post param id.
                task: "download_image",     # A fixed value
                url:       ,                # download file url
                access_code:     ,          # Access code
                time:      ,                # Time consuming
            }
        }
    }

    :return:
    """

    try:
        from rsc.service.ImageService import ImageService

        # 头部必须是 Content-Type: application/json
        json_data = request.get_json()

        # id = request.args.get("id")                 # id 客户端可以用该 id 是什么。 callback 时回调
        # url = request.args.get("url")               # 下载 url
        # type = request.args.get("type")             # 类型 JPG|GIF|BMP|JPEG|PNG 选一个
        # priority = request.args.get("priority")     # 优先级
        # save_path = request.args.get("save_path")   # 保存路径
        # callback = request.args.get("callback")     # 回调地址

        service = ImageService()
        service.process_download_request(json_data)
        return render_json(json_res_success())
    except Exception as e:
        return E400(str(e))


@image.route("/image/access/<access_code>", methods=['POST'])
@token_required
def access_image(access_code:str):
    """
    下载图像
    post header : {
        Content-Type: application/json,
        access_token: access_token from vans-token-manager
        client_id:    client_id from vans-token-manager conf. create by developers.
    }

    :return:
    """
    try:
        from rsc.service.ImageService import ImageService

        # 获取图片
        service = ImageService()
        image_data, mime = service.get_image(access_code)
        data = json_res_success({"image":image_data, "mime":mime})
        return render_json(data)
    except Exception as e:
        return E400(str(e))