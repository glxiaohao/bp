# coding:utf-8
__author__ = 'guoling'
import sys
import os
import config
import cx_Oracle


reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

db_pool = cx_Oracle.SessionPool(user=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['USER_NAME'],
                                password=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['PASSWORD'],
                                dsn=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['DSN'],
                                min=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['MIN'],
                                max=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['MAX'],
                                increment=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['INCREMENT'],
                                threaded=config.CURRENT_CONFIG['DB_CONFIG_BIZ']['THREADED'])