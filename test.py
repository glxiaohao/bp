# coding:utf-8
__author__ = 'guoling'
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import platform
print platform.system()