# coding:utf-8
__author__ = 'guoling'
import sys
import os
import logging
import logging.config
import config
from flask import jsonify, request, Blueprint
from Common.MessageUtils import standarlize_response
import QueryConsultingCostRules as ConsultingRules


reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('default')

# 蓝图
consulte = Blueprint("consulting",__name__)

@consulte.route('/cost/rules', methods=["GET"])
# @with_internal_journallog
def  query_consulting_cost_rules():
    """
    方法用途: 获取副卡-销售品额外信息
    :param: xspid
    :return: json数据
    网页地址测试: http://localhost:6001/bp/consulting/cost/rules?xspid=00000000E0B00375E86F0D16E043AC1410ACB9E7
    """
    logger.debug(u"[开始]获取副卡-销售品额外信息开始")
    xspid = request.args.get("xspid",None).strip()
    if not xspid:
        logger.debug(u"[失败]没有获取到销售品id")
        return jsonify(standarlize_response(1, u"[失败]没有获取到手机号", None))
    logger.debug(u"返回结果集")
    result = ConsultingRules.query_consulting_cost_ruless(xspid)
    return result