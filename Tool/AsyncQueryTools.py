# coding:utf-8
__author__ = 'guoling'
import sys
import os
import logging
import json

import unirest

import config
unirest.timeout(45)

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class AsyncQueryTools:
    def __init__(self):
        self._logger = logging.getLogger('default')

    # 不懂 此方法
    def get_db_data(self, zzj_raw, pro_name, out_param_type_list):
        """
        获取调用存储过程返回的结果集
        :param zzj_raw:
        :param pro_name:
        :return:
        """
        local_data = None
        if zzj_raw["code"] == 0:
            zzj_result = zzj_raw["dataObject"]["results"][0]
            if zzj_result["name"] == pro_name:
                if len(zzj_result["values"]) > 1:
                    rese = list()
                    for value in zzj_result["values"]:
                        rese.append(value.get("value"))
                    return rese
                else:
                    local_data = zzj_result["values"][0]["value"]
        return local_data

    def async_query(self, sp_name, time_out=15, cache_expires=60, readonly_transaction_required=1,
                    in_param_list=list(), out_param_type_list=list(), db_flag=0):
        '''
        暂时不适合多个存储过程同时调用
        通用查询接口封装
        :param sp_name: 存储过程名称
        :param time_out: 接口超时时间
        :param cache_expires: 缓存失效时间
        :param readonly_transaction_required: 是否支持只读事物
        :param in_param_list: 入参列表（必须按顺序）[['orderid','123456'],['id','123']]
        :param out_param_list: 出参列表
        :param out_param_type_list:出参类型列表
        :return:
        '''

        result_data = None
        prov_result = None
        in_param = list()
        in_param_order = 1
        for i in in_param_list:
            name = i[0]
            value = i[1]
            in_param_dict = dict(name=name,
                                 value=value,
                                 order=in_param_order)
            in_param.append(in_param_dict)
            in_param_order += 1
        out_param = list()
        out_param_order = 1
        for l in out_param_type_list:
            out_param.append(dict(type=l,
                                  order=out_param_order))
            out_param_order += 1

        params = dict(interface_name=sp_name,
                      timeout=time_out,
                      cache_expires=cache_expires,
                      readonly_transaction_required=readonly_transaction_required,
                      db_flag=db_flag,
                      attach="www.189.cn",
                      sps=[dict(
                          in_params=in_param,
                          out_params=out_param,
                          name=sp_name,
                          id='1'
                      )])
        params_str = json.dumps(params)
        print "params_str:",params_str
        try:
            prov_result = unirest.post(config.CURRENT_CONFIG['PROCEDURE_QUERY_URL'], params=params_str,
                                       headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
            self._logger.debug('调用通用查询接口返回=%s', prov_result.body)
            if prov_result is not None:
                if prov_result.code != 200:
                    self._logger.error('[调用接口接口FAIL] HTTP Status=%d,url = %s' % (
                    prov_result.code, config.CURRENT_CONFIG['PROCEDURE_QUERY_URL']))
                body = json.loads(prov_result.raw_body)
                result_data = self.get_db_data(body, sp_name, out_param_type_list)
        except Exception, e:
            error_desc = '调用通用查询接口异常=%s' % e.message
            self._logger.exception(error_desc)
            self._logger.debug(u"Exception=%s:" % error_desc)
        return result_data
