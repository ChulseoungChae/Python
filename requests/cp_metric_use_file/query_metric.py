# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import time
import datetime

#import math
import requests
import json
import copy
#from collections import OrderedDict
#import numpy as np
#import pandas as pd
from multiprocessing import Pool, current_process

import HTTP_POST_request
#import DataFrameInfo
#import multi_make_process as m_proc

# 아래부터는 keti 모듈 import
import ketidatetime

""" 실제 작업에 필요한 query parameter 예 - 초기값 """
query_parameter = {
    "start" : "2014-06-01 00:00:00",
    "end": "2014-06-02 00:00:00",
    "aggregator" : "none",
    "metric" : "____test____"
}

""" 쿼리 하려는 tag """
query_tags = {
}


def brush_args():
    usage = "\n usage : python %s {IP address} {port} " %sys.argv[0]
    usage += "{in_metric_name} {out_ip}"
    usage += "\n usage : python %s {IP address} {port} " %sys.argv[0]
    usage += "{in_metric_name} {out_ip} {port} {out_metric} {start_day} {end_day}"
    print ( usage + '\n'  )

    _len = len(sys.argv)

    if _len < 8:
        print (" 추가 정보를 입력해 주세요. 위 usage 설명을 참고해 주십시오")
        print (" python 이후, 아규먼트 갯수 8개 필요 ")
        print (" 현재 아규먼트 %s 개가 입력되었습니다." %(_len) )
        print (" check *run.sh* file ")
        exit (" You need to input more arguments, please try again \n")

    _ip = sys.argv[1]
    _port = sys.argv[2]
    _in_met = sys.argv[3]
    _out_ip = sys.argv[4]
    _out_port = sys.argv[5]
    _out_met = sys.argv[6]
    _start = None
    _end = None

    if _len > 5:
        _start = sys.argv[7]
        _end = sys.argv[8]

    if ( len(_start) < 15 or len(_end) < 15 ):
        _start = ketidatetime._check_time_len(_start)
        _end = ketidatetime._check_time_len(_end)

    return _ip, _port, _in_met, _out_ip, _out_port, _out_met, _start, _end



def processingResponse(in_data):
    '''openTSDB에서 전송받은, string 들을 dictionary로 변경하여
       dict 를 회신함. 형태를 변경하고, dict의 갯수를 알려줌'''

    _d = in_data
    _r = eval(_d.content)
    # queryData.content is string, thus convert this to list
    _l = len(_r)

    if g_debug_off:
        print ("... debugging print ... filename: %s" %__file__)
        print (type(_d.content), len(_d.content))
        print (type(_r), _l)

        if g_debug_off:
            print (_r[0]['metric'])
            print (_r[0]['tags'])
            print (_r[0]['dps'])

    return _r, _l
    # dict 와 length (딕셔너리 갯수) 리턴


def main_run(_date, dy=None, hrs=None, mins=None):

    if dy == 1: _t_scale = 24
    elif hrs == 1 : _t_scale = 1
    elif mins == 1 : _t_scale = 0.1
    if g_debug_off : print (_t_scale)

    query_parameter['start'] = _date
    query_parameter['end'] = ketidatetime.strday_delta(_date, _t_scale)
    query_parameter['aggregator'] = 'none'
    query_parameter['metric'] = in_metric

    # TSDB에서 데이터를 읽어오기 위한, 패러미터 세팅

    # url = "http://tinyos.asuscomm.com:44242/api/query"
    # for example url
    # new_url = "http://125.140.110.217:4242/api/put"
    # for exmaple write url
    # 참조 : 125.140.110.217 : 4242, tinyos.asuscomm.com : 44242
    # 원본 데이터 : none:rc04_simple_data_v3
    # 테스트 = 데이터 있는 구간 : 2016/07/29 , 2016/07/30

    _q_para = query_parameter
    _url = 'http://' + ip + ':' + port + '/api/query'
    if g_debug_on : print (_url, _q_para, query_tags)
    queryData = HTTP_POST_request.QueryData(_url, _q_para, query_tags)
    # 데이터 reading from DB, 스트링 데이터임
    print("quertData OK...")

    print(queryData)

    _dictbuf, _dictlen = processingResponse(queryData)
    # 스트링 데이터를 리스트 형태로 변환

    print("processingResponse OK...")

    if _dictlen == 0 :
        print ("length is 0, please check it later, it is strange dps is empty")
        return None

    print("start make txt file...")
    mk_file(_date, _dictbuf, _dictlen)

    return None

def mk_file(_date, _d_b, _d_l):

    for _dict in _d_b:
        _dict['metric'] = str(out_metric)


    _file = str(_date)+".json"
    _filename = _file[:4] + _file[5:7] + _file[8:13] + _file[14:16] + _file[17:]
    print(_filename)

    _f = open(_filename, 'w')
    json.dump(_d_b, _f, indent=2)
    _f.close()

    return None

if __name__ == "__main__":

#'python cp_metric.py 125.140.110.217 54242 HanuriTN_00 125.140.110.217 44242 2016/06/01 2014/06/02 '

    g_debug_on = 1
    g_debug_off = 0
    _send_buf = []

    start_time = time.time()
    start_datetime = datetime.datetime.now()

    ip, port, in_metric, out_url, out_port, out_metric, q_start, q_end = brush_args()
    g_w_url = "http://" + out_url + ":" + out_port + "/api/put"
    headers = {'content-type': 'application/json'}

    _date_on  = q_start
    _date_off = q_end

    while(_date_on != None):
        main_run(_date_on, mins=1)
        _date_on = ketidatetime.daydelta(_date_on, _date_off, mins=1)
        #_date_on = ketidatetime.daydelta(_date_on, _date_off)

        run_time = time.time() - start_time
        print ( "\n\n [Main] Query time: %s ~ %s" % (q_start,q_end) )
        print ( " Run time: %.4f (sec)" % (run_time) )
        print('----------------------------------------------------------')
