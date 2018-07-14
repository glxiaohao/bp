# coding:utf-8
__author__ = 'guoling'
import sys
import os
import functools
from DBUtils.PooledDB import PooledDB

import config
import cx_Oracle
from Common.MessageUtils import head_response
from Dao.OrderDao import db_pool
import logging
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('default')

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# 获取存储过程的值
def get_stored_procedure(ORDER_ID, PARTNER_ORDER_ID):
    """
    获取存储过程的值
    :param ：
    :return:
    """
    conn, cur = None, None
    try:
        conn = db_pool.connection() # 数据库连接异常
        cur = conn.cursor()
        result = cur.var(cx_Oracle.CURSOR)
        cur.callproc("SP_DEAL_SEARCHBROADBANDINFO", [ORDER_ID, PARTNER_ORDER_ID, result])
        for item in result.getvalue():
            return item
    except Exception as error:
        print error
        logger.debug("获取数据库信息异常:%s" % error.message)
        return False
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def deal(biz, queryInfo):
    ok = True
    ORDERID_INVAILD = (1023004, "通过电渠订单号未查到订单信息")
    PARTNERORDERID_INVAILD = (1023005, "通过合作商订单号未查到订单信息")
    INVAILD = (1023001, "缺少必要的入参")

    orderId = biz.get("orderId", None)
    # print(orderId)
    # print len(orderId)
    partnerOrderId = biz.get("partnerOrderId", None)

    if orderId:
        result = queryInfo(orderId=orderId)  # 根据订单号查询信息
        if result is not None:
            return result
        else:
            if not partnerOrderId:
                return ORDERID_INVAILD  # 1023004
            else:
                ok = False

    # 能够继续往下执行,OK值的含义
    # ok = True表示订单号不存在
    # ok = False表示订单号存在但是有误

    if partnerOrderId:
        result = queryInfo(partnerOrderId=partnerOrderId)  # 根据合作商订单号查询信息
        if result is not None:
            return result
        else:
            return PARTNERORDERID_INVAILD
            # if ok:
            #     return PARTNERORDERID_INVAILD
            # else:
            #     return ORDERID_INVAILD

    return INVAILD

def kdxy_common(result_list, transactionId, attach, orderId=None, partnerOrderId=None):
    out_param_type_list = ["CURSOR"]

    results = get_stored_procedure(orderId, partnerOrderId)
    # print "入参%s"%in_param_list
    # print "出参%s"%out_param_type_list
    print results
    if results:
        logger.debug("SP_DEAL_SEARCHBROADBANDINFO返回count:%s" % len(results))
        for tc in results:
            order_price = 0
            partner_order_id = results[0]  # 合作商订单号

            order_id = results[1]  # 订单号
            prov_code = results[2]  # 省编号
            city_code = results[3]  # 市编号
            broadband_account = results[4]  # 宽带账号
            prod_nbr = results[5]  # NBR

            idcardno = results[6]  # 身份证号码
            contact_num = results[7]  # 联系电话

            create_date = results[8]  # 订单生成时间
            print create_date
            order_price = results[9]  # 订单金额
            order_price = int(order_price) * 100
            order_status = results[10]  # 订单状态

            partnerPaymentId = results[11]  # 合作商支付订单号  扩展属性编码：800031
            comboPrice = results[12]  # 套餐金额（单位：分） 扩展属性编码：800032
            paymentAmount = results[13]  # 实际支付金额（单位：分） 扩展属性编码：800033

            result_list = {"partnerOrderId": partner_order_id,
                           "orderId": order_id,
                           "provinceCode": prov_code,
                           "cityCode": city_code,
                           "broadbandAccount": broadband_account,
                           "prodNbr": prod_nbr,
                           "custInfo": {"certNumber": idcardno},
                           "contactInfo": {"contactNbr": contact_num},
                           "createTime": create_date,
                           "price": order_price,
                           "orderStatus": order_status,
                           "partnerPaymentId": partnerPaymentId,
                           "comboPrice": comboPrice,
                           "paymentAmount": paymentAmount}
            return head_response(transactionId, 0, "操作成功", attach, result_list)



def get_ordersearch_info(data):
    try:
        head = data["head"]
        biz = data['biz']

        transactionId = head['transactionId']
        attach = head["attach"]
        sysCode = head["sysCode"]

        orderId = biz.get("orderId", None)
        partnerOrderId = biz.get("partnerOrderId", None)

        if isinstance(biz, dict):  # 判断biz是否是dict类型，返回true或者false
            result_list = dict()
            queryInfo = functools.partial(kdxy_common, result_list, transactionId, attach)
            r = deal(biz, queryInfo)
            if isinstance(r, tuple):
                # 下面传递的5个参数分别为： transaction_id, code, err, attach, biz
                return head_response(transactionId, r[0], r[1], attach, None)
            else:
                return r
    except Exception, e:
        print e
        logger.error(e.message)
        return head_response(transactionId, 1, "服务器异常", attach, None)
