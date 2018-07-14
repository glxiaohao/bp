# coding:utf-8
__author__ = 'guoling'
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import sys
import os
import platform

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

PROD,  RC = range(2)
CURRENT_PROFILE = RC

# PREFIX = 'C:\BllLogs' if platform.system() == 'Windows' else '/opt/logs/python-apps-logs/MiscServiceBp/6001' # window
PREFIX = '/Users/gl/python_logs' if platform.system() == 'Darwin' else '/opt/logs/python-apps-logs/MiscServiceBp/6001'   # mac

# TODO: 日志文件路径
LOG_PATH_DEBUG = r'%s\debug.log' % PREFIX if platform.system() == 'Windows' else '%s/debug.%s.log' % (
    PREFIX, os.getpid())
LOG_PATH_INFO = r'%s\info.log' % PREFIX if platform.system() == 'Windows' else '%s/info.%s.log' % (
    PREFIX, os.getpid())
LOG_PATH_WARN = r'%s\warn.log' % PREFIX if platform.system() == 'Windows' else '%s/warn.%s.log' % (
    PREFIX, os.getpid())
LOG_PATH_ERROR = r'%s\error.log' % PREFIX if platform.system() == 'Windows' else '%s/error.%s.log' % (
    PREFIX, os.getpid())


# 判断目录是否存在，若不存在则创建
if not os.path.exists(PREFIX):
    os.makedirs(PREFIX)

# TODO: 日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s::(%(process)d %(thread)d)::%(module)s[line:%(lineno)d] - %(message)s'
        },
    },
    'handlers': {
        'error': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'standard',
            'filename': LOG_PATH_ERROR + '_file',
            'when': 'D',
            'interval': 1
        },
        'warn': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'WARN',
            'formatter': 'standard',
            'filename': LOG_PATH_WARN + '_file',
            'when': 'D',
            'interval': 1
        },
        'info': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': LOG_PATH_INFO + '_file',
            'when': 'D',
            'interval': 1
        },
        'debug': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': LOG_PATH_DEBUG + '_file',
            'when': 'D',
            'interval': 1
        }
    },
    'loggers': {
        'default': {
            'handlers': ['debug', 'info', 'warn', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'flask.request': {
            'handlers': ['debug', 'info', 'warn', 'error'],
            'level': 'WARN',
            'propagate': False
        },
        'tornado.application': {
            'handlers': ['debug', 'info', 'warn', 'error'],
            'level': 'WARN',
            'propagate': False
        },
        'tornado.general': {
            'handlers': ['debug', 'info', 'warn', 'error'],
            'level': 'WARN',
            'propagate': False
        }
    }
}

# TODO: 调用外部地址配置

CURRENT_CONFIG = [
    dict(
        # prod 数据库配置(业务)
        # 数据库配置
        DB_CONFIG_BIZ=dict(
            DSN='172.16.20.176/wtdb',
            PORT=1521,
            USER_NAME='e_channel',
            PASSWORD='e_channel',
            MIN=0,
            MAX=50,
            INCREMENT=1,
            THREADED=True
        ),
        PROCEDURE_QUERY_URL="http://10.128.89.11:8001/p/pq",  # 存储过程批量调用接口 仅供查询

        # # rabbit队列
        # QUEUE_SERVER_HOST='10.128.89.4',
        # QUEUE_SERVER_VHOST='journal',
        # QUEUE_SERVER_PORT=5673,
        # QUEUE_SERVER_USERNAME='rabbit_journal',
        # QUEUE_SERVER_PASSWORD='8WmphsulfF',

    ),

        dict(
        # rc数据库配置（业务）
        # 数据库配置
        DB_CONFIG_BIZ=dict(
            DSN='172.16.50.67/orcl',
            PORT=1521,
            USER_NAME='e_channel',
            PASSWORD='e_channel_test',
            MIN=0,
            MAX=50,
            INCREMENT=1,
            THREADED=True
        ),
        PROCEDURE_QUERY_URL="http://172.16.20.46:8001/p/pq",  # 存储过程批量调用接口 仅供查询

        # # rabbit队列
        # QUEUE_SERVER_HOST='172.16.20.47',
        # QUEUE_SERVER_VHOST='journal',
        # QUEUE_SERVER_PORT=5673,
        # QUEUE_SERVER_USERNAME='smallrabbit',
        # QUEUE_SERVER_PASSWORD='123456',

        ),
][CURRENT_PROFILE]
