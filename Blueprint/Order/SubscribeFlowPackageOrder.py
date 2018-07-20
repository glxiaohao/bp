# coding:utf-8
__author__ = 'guoling'
import sys
import os
from flask import jsonify, request
from Common.MessageUtils import standarlize_response
import datetime
from Dao.flowPackageDao import save_book_order
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import config
import logging
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('default')


def create_book_order():
    """
    [KF_20160920_2144 ]流量包预约需求
        预约流量包订单生成
    """
    sales_prod_id = request.args.get('salesProdID', "")
    sales_prod_name = request.args.get('salesProdName', "")
    phone_number = request.args.get('phoneNumber', "")
    appointment_phone = request.args.get('appointmentPhone', '')
    appointment_date = request.args.get('appointmentDate', "")
    user_id = request.args.get('userId', "")
    shop_id = request.args.get('shopId', "")

    if "" in (sales_prod_id, sales_prod_name, phone_number, appointment_date, user_id, shop_id, appointment_phone):
        logger.debug(u"""流量包预约创建订单请求参数不正确sales_prod_id=%s, sales_prod_name=%s, phone_number=%s,
                     appointment_date=%s, user_id=%s, shop_id=%s""",
                     sales_prod_id, sales_prod_name, phone_number, appointment_date, user_id, shop_id)
        return standarlize_response(2, u'请求参数不正确, 请检查参数', None)

    # 转换预约日期时间为YYYYMMDD格式
    try:
        app_date = datetime.datetime.strptime(appointment_date, '%Y%m%d').strftime("%Y%m%d")
    except ValueError, e:
        logger.debug(u'预约时间参数不正确appointment_date=%s,错误原因=%s', appointment_date, e.message)
        return standarlize_response(2, u'预约时间参数不正确=%s, 错误原因=%s' % (appointment_date, e.message), None)

    # 验证创建时间是否符合要求    要求预约时间至少大于当前时间1天
    today = datetime.datetime.now().strftime('%Y%m%d')
    if today >= app_date:
        logger.debug(u'预约时间不符合校验规则, 请确保当前时间至少小大预约日期一天, appointment_date=%s', appointment_date)
        return standarlize_response(672, u'[失败]预约时间不符合校验规则, 请确保当前时间至少提前预约日期一天', appointment_date)

    # 查看是否有在途订单  非业务要求, 暂时注掉, 后期与业务沟通是否加此功能  具体功能由'存储过程'实现
    # has_order_today = get_book_on_order(phone_number, appointment_date)
    #
    # if has_order_today:
    #     logger.debug(u'user_id=%s, 订单于%s包含在途订单, 无法办理', user_id, appointment_date)
    #     return standarlize_response(1, u'user_id=%s, 订单于%s包含在途订单, 无法办理' % (user_id, appointment_date), None)

    # 创建订单
    order_status = save_book_order(sales_prod_id, sales_prod_name, phone_number,
                                   app_date, user_id, shop_id, appointment_phone)

    if not order_status['status']:
        logger.debug(u'[失败]user_id=%s, [失败]创建预约订单失败, 失败原因=%s', user_id, order_status['status'])
        return standarlize_response(1, u'[失败]创建预约订单失败', order_status)

    logger.debug(u'user_id=%s, [成功]创建预约订单成功')
    return standarlize_response(0, u'操作成功', None)

