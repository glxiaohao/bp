# coding:utf-8
__author__ = 'guoling'
import sys
import os
import time

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#返回请求json
def standarlize_response(code, err, biz):
    return {
        'code': code,
        'Description': err,          # 供客户端使用
        'errorDescription': err,     # 供后台使用
        'dataObject': biz,
    }


def head_response(transaction_id, code, err, attach, biz):
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    now_time = time.localtime(now)
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", now_time)
    return {
        "head": {
            "transactionId": transaction_id,
            "reqTime": format_time,
            "code": code,
            "err": err,
            "attach": attach
        },
        "biz": biz
    }