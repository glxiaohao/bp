# coding:utf-8
__author__ = 'guoling'
import sys
import os
from flask import jsonify, request, Blueprint


reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import logging
import config
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('default')

import SubscribeFlowPackageOrder as Subscribe   # 订阅流程包订单

order = Blueprint('order', __name__)


@order.route('/create/book/order', methods=['GET'])
# @with_internal_journallog
def generate_order():
    """
    请求地址: /order/create/book/order?
    salesProdId=[销售品ID]&salesProdName=[销售品名称]&phoneNumber=[预定号码]&appointmentDate=[预定时间]&userId=[用户ID]
    salesProdID 销售品ID
    salesProdName 销售品名称
    phoneNumber 用户号码
    appointmentDate 预定时间
    userId 用户ID
    :return:    json
    """
    logger.debug('流量包预约订单生成开始')
    result = Subscribe.create_book_order()
    logger.debug('流量包预约订单生成结束')
    return jsonify(result)