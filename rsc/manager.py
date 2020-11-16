# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : manager.py
# @Created  : 2020/11/9 3:49 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : flask框架项目启动运行文件
# -------------------------------------------------------------------------------
import sys,signal,argparse,os

def _quit(signal, frame):
    print("Bye!")
    sys.exit(0)


def main(args=sys.argv[1:]):
    """
    入库
    :param args: 去掉第一个 第一个 -h help
    :return:
    """

    from rsc import create_app
    from chaussette.server import make_server

    parser = argparse.ArgumentParser(description="Vanas Token Manager")

    # 添加参数
    parser.add_argument("--fd", type=int, default=None)
    # parser.add_argument("--config-file", type=str,default=None, help="Config file path")

    # 解析参数
    args = parser.parse_args(args)

    # 创建 flask
    app = create_app(os.getenv('VANAS_PROJECT_ENV') or 'default')

    app.logger.info("Vanas Resources Cloud create app.")

    # 默认值
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)

    signal.signal(signal.SIGINT, _quit)
    signal.signal(signal.SIGTERM, _quit)

    # app.logger.info("args.fd >> {}".format(args.fd))
    # app.logger.info("args.config_file >> {}".format(args.config_file))

    def runner():

        if args.fd is not None:
            # use chaussette
            httpd = make_server(app, host='fd://%d' % args.fd)
            httpd.serve_forever()
        else:
            app.run(debug=debug, host=host, port=port)

    app.logger.info("Web Runner.")
    runner()

if __name__ == '__main__':
    main()