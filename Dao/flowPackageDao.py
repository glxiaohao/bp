# coding:utf-8
__author__ = 'guoling'
import sys
import os
from Dao.BaseDao import db_pool
import cx_Oracle
import config
import logging
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('default')


reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def save_book_order(sales_prod_id, sales_prod_name, phone_number, appointment_date, user_id, shop_id, appointment_phone):
    """
    生成流量包预约订单
    :param sales_prod_id: 销售品ID  | STRING
    :param sales_prod_name: 销售品类型  | STRING
    :param phone_number: 预约手机号  | STRING
    :param appointment_date: 预约时间  | STRING
    :param user_id: 用户ID  | STRING
    :param shop_id: 店铺ID  | STRING
    :param appointment_phone: 预约人手机号  |  STRING
    :return: response
    """

    response = {'status': 0, 'msg': u'记录失败, 未插入数据库'}
    logger.debug(u'user_id=%s, [信息]流量包预约生成订单开始', user_id)
    conn, cur = None, None
    try:
        conn = db_pool.acquire(cclass="Misc", purity=cx_Oracle.ATTR_PURITY_SELF)
        cur = conn.cursor()
        output_type = cur.var(cx_Oracle.STRING)
        in_params = [user_id, sales_prod_id, sales_prod_name, phone_number, appointment_date,
                     shop_id, appointment_phone, output_type]
        save_db = cur.callproc('SP_DEAL_SAVESUBSCRIBEORDER', in_params)

        if save_db is None or save_db == "0":
            logger.debug(u'user_id=%s, [失败]流量包预约数据库生成订单失败', user_id)
            response['msg'] = u'流量包预约数据库生成订单失败'
        else:
            logger.debug(u'user_id=%s, [成功]流量包预约数据库生成订单成功', user_id)
            response['status'] = 1
            response['msg'] = u'[成功]流量包预约数据库生成订单成功'
            conn.commit()
    except Exception, e:
        logger.debug(u'user_id=%s, [失败]流量包预约数据库生成订单异常=%s', user_id, e.message)
        response['msg'] = u'[失败]流量包预约数据库生成订单异常=%s' % e.message
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            db_pool.release(conn)
    logger.debug(u'[信息]流量包预约生成订单结束')
    return response
