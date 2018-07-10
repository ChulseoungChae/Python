# -*- coding: utf-8 -*-

# Author : jeonghoonkang , https://github.com/jeonghoonkang

""" metric copy for openTSDB

    목적: OpenTSDB의 메트릭 데이터를 복사
    기능 : metric -> new metric 복사
           metric -> 다른 IP 서버로 복사
"""
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


def resendBuf(decode_data, s):
    time.sleep(5)

    try :
        r = s.post(g_w_url, decode_data, timeout = 10, headers=headers)
        if r.status_code > 204: return 'FAIL'
        else : return 'SUCCESS'

    except requests.exceptions.ReadTimeout as e :
        print ("\n [Exception]", e)
        if 'FAIL' == resendBuf(decode_data, s) : resendBuf(decode_data, s)

    except requests.exceptions.ConnectionError as e :
        print ("\n [Exception]", e)
        time.sleep(10)
        if 'FAIL' == resendBuf(decode_data, s) : resendBuf(decode_data, s)

def sendBuf(buf_dict_list, s):
    _data = buf_dict_list
    _write_url = g_w_url

    if len(buf_dict_list) == 0 :
        #print (" no data in buffer, it tried to send EMPTY buf")
        return

    decode_data = json.dumps(buf_dict_list, indent=2)

    if g_debug_off:
        print (decode_data)
        print (type(decode_data))
        print (type(_data))
        _deco_data_cnt_ = len(decode_data)
        print (_deco_data_cnt_)

    try:
        _r = s.post(g_w_url, decode_data, headers=headers)
        while _r.status_code > 204:
            print (" Write error!")
            print (_r.content)
            if 'FAIL' == resendBuf(decode_data, s) : resendBuf(decode_data, s)

    except requests.exceptions.ReadTimeout as e :
        print ("\n [Exception]", e)
        if 'FAIL' == resendBuf(decode_data, s) : resendBuf(decode_data, s)

    except requests.exceptions.ConnectionError as e :
        print ("\n [Exception]", e)
        time.sleep(10)
        if 'FAIL' == resendBuf(decode_data, s) : resendBuf(decode_data, s)

def postDp(dict_buf):
    # make multiple list of 50 chunk dict
    # send every chunk which has 50 dp in it
    _tot_len = len(dict_buf)
    _solid = _tot_len / 50
    _rest = _tot_len % 50
    if _tot_len == 0 : return

    if _rest > 0 : _loop = _solid + 1
    else : _loop = _solid

    if g_debug_off: print ('n', _tot_len, _solid)
    _pos_end = 0

    with requests.Session() as s:
        for _idx in xrange(_loop):
            _pos_start = 50 * _idx
            _pos_end   = _pos_start + 49
            if _pos_end > _tot_len : _pos_end =_tot_len
            _send_buf = dict_buf[_pos_start:_pos_end]
            sendBuf(_send_buf, s)
            # send : post dp, 실제 전송
            if g_debug_off:  print ("\n send solid chunk", _idx, _pos_start, _pos_end )
            if g_debug_off: print (_send_buf)
        _send_buf = dict_buf
        if len(_send_buf) == 0 :
            print( _solid, _rest, _solid)
            exit()
        sendBuf(_send_buf, s)
        # send : post dp, 실제 전송

        if g_debug_off : exit()

        if g_debug_off :
            print ("send last chunk")
            print (_send_buf)

    return True


def putIteration(_dt):

    _file = str(_dt)+".json"
    _filename = _file[:4] + _file[5:7] + _file[8:13] + _file[14:16] + _file[17:]

    _f = open(_filename, 'r')
    fd = _f.read()
    decoding_json = json.loads(fd)

    print("put start : %s" %_dt)

    _len = len(decoding_json)

    putDict = {}
    dict_array=[]
    _current_cnt = 0

    for one_dict in decoding_json:
        _current_cnt += 1
        # tags 를 그대로 사용한다. write 하는 메트릭에 tag 변경없이 사용
        for k, v in one_dict.iteritems():
            if g_debug_off : print (k, v)
            # key are metric, dps, tags, aggregatorTag
            # we don't need aggregatorTag which len is 0

            if k == 'dps' :
                for kt, pv in v.iteritems() :
                    putDict['metric'] = one_dict['metric']
                    putDict['tags'] = one_dict['tags']
                    putDict['timestamp'] = kt
                    putDict['value'] = pv
                    if g_debug_off : print (kt, pv)
                    if g_debug_off : print (putDict)
                    dict_array.append(putDict)
                    putDict = {}

        if g_debug_off:
            if len(dict_array) == 0 : print (one_dict)
            print ("리스트로 구성된 딕셔너리 갯수", len(dict_array))

        if True == postDp(dict_array):
            # 실제 전송은 postDB() 내부에서 실행
            __display_out = '*' * 30 + " current progress / tot dict = %s / %s \r" %(_current_cnt, _len)
            sys.stdout.write(__display_out)
            sys.stdout.flush()

            dict_array=[]

        if g_debug_off : exit()

    _f.close()


    return True

def processingResponse(in_data):
    '''openTSDB에서 전송받은, string 들을 dictionary로 변경하여
       dict 를 회신함. 형태를 변경하고, dict의 갯수를 알려줌'''

    _d = in_data
    _r = eval(_d.content)
    # queryData.content is string, thus convert this to list
    _l = len(_r)
    print("eval 길이 : %s" %_l)

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

    putIteration(_date)
    # 데이터 입력 to DB

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
