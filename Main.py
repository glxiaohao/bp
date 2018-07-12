# coding:utf-8
__author__ = 'guoling'
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import argparse
import platform
import signal
import gevent
from tornado.ioloop import IOLoop
from gevent.wsgi import WSGIServer
from gevent.monkey import patch_all
from flask import Flask
import logging
import logging.config
import config2
logging.config.dictConfig(config2.LOGGING_CONFIG)
logger = logging.getLogger('default')

misc_service = Flask(__name__)

@misc_service.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'OK MiscServiceBp'


@misc_service.route('/', methods=['GET'])
def root():
    return 'MiscServiceBp OK'

def sig_handler(sig, frame):
    logger.warn('Caught signal: %s', sig)
    IOLoop.instance().add_callback(shutdown)


if __name__ == '__main__':
    # 增加指定端口启动功能
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=6001, help='port providing service')

    args = parser.parse_args()
    thread = 1 if platform.system() == 'Windows' else 0

    # 增加信号
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    # 优雅的关闭
    def shutdown():
        logger.debug('Shutting down ...')
        http_server.stop(timeout=5)
        exit(signal.SIGTERM)

    gevent.signal(signal.SIGTERM, shutdown)
    http_server = WSGIServer(('', args.port), misc_service)
    http_server.serve_forever()