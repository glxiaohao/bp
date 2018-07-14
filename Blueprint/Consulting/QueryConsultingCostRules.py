# coding:utf-8
__author__ = 'guoling'
import sys
import os

from flask import jsonify
from Common.MessageUtils import standarlize_response
import logging
reload(sys)
sys.setdefaultencoding("utf-8")
logger = logging.getLogger('default')

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import config
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('default')

from Tool.AsyncQueryTools import AsyncQueryTools
async_query_tool = AsyncQueryTools()

def query_consulting_cost_ruless(xspid):
    """
    :param xspid: 0000000055C09D6B9A376E98E053433210AC47CA
    :return:
    """
    in_param_list = [["V_SELLID", xspid]]
    out_param_type_list = ["CURSOR"]
    results = async_query_tool.async_query("P_IF_GET_GOODS_INFO_EXT",
                                                in_param_list=in_param_list,
                                                out_param_type_list=out_param_type_list)
    logger.debug(u"[信息]返回P_IF_GET_GOODS_INFO_EXT的结果集")
    if results:
        result_list = []
        for tc in results:
            imgUrl = tc['WAP_MAIN_FIGURE']  # WAP主图
            tariffRules = tc['WAP_RULE']  # WAP资费规则
            businessRules = tc['WEB_RULE']  # 网厅业务规则
            result_list.append(imgUrl)
            result_list.append(tariffRules)
            result_list.append(businessRules)
            logger.debug(u"result_list=%s, [信息]记录前台传来的数据开始",result_list)
            result_list = {"imgUrl":imgUrl,"tariffRules":tariffRules,"businessRules":businessRules}
            return jsonify(standarlize_response(0, "查询销售品id成功获取相应的数据", result_list))
    # 无返回值
    else:
        logger.debug(u"[信息]副卡-销售品额外信息无查询结果results=%s", results)
        return jsonify(standarlize_response(1, "副卡-销售品额外信息无查询结果", results))



