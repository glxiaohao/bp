# coding:utf-8
__author__ = 'guoling'
import sys
import os
import json

import logging
import logging.config
import config
from Common.MessageUtils import head_response
from flask import jsonify, request, Blueprint
from Common.MessageUtils import standarlize_response
from Blueprint.OrderSearch import OrderInfoSearch

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('default')

# 蓝图
ordersearch = Blueprint("orderinfosearch",__name__)

@ordersearch.route('/ordersearch', methods=['POST'])
def get_ordersearch_info():
    try:
        data = request.data
        json_data = json.loads(data)

        if data != '':
            logger.debug("1. 请求到的报文data=%s ： \n" % data)
            result = OrderInfoSearch.get_ordersearch_info(json_data)
            # print json_data
            # print result
        else:
            logger.debug('(无)请求的信息是：data=%s', data)
    except Exception as e:
        # print e
        logger.error('数据json 转换错误 msg = %s', e.message)
        # head_response(transaction_id, code, err, attach, biz):
        return jsonify(head_response(None,2, '数据格式有误', None, None))
    # print jsonify(result)
    return jsonify(result)
