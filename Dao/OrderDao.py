# coding:utf-8
__author__ = 'guoling'
import sys
import os
import config
import cx_Oracle
from DBUtils.PooledDB import PooledDB

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# db_pool = PooledDB(cx_Oracle, user=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['USER_NAME'],
#                    password=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['PASSWORD'],
#                    dsn=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['DSN'],
#                    mincached=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['MIN'],
#                    maxcached=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['MAX'],
#                    maxconnections=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['INCREMENT'],
#                    threaded=True)