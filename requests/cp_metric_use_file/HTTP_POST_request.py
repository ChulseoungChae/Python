#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Mon Mar  5 14:41:11 2018

    @author : Taewoo
    @author : https://github.com/jeonghoonkang
"""

import time
import requests
import json
#import pandas as pd
from collections import OrderedDict
from multiprocessing import current_process

MAX_BUFFER = 1000000
#requests.adapters.DEFAULT_RETRIES = 8

def convertTimeToEpoch(_time):
    _f_time_sym_ = ''

    if _time.find('/') != -1:
        _f_time_sym_ = '/'
    if _time.find('-') != -1:
        _f_time_sym_ = '-'

    date_time = "%s.%s.%s %s:%s:%s" \
                %(_time[8:10], _time[5:7], _time[:4], _time[-8:-6], _time[-5:-3], _time[-2:])
        #print date_time
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int (time.mktime(time.strptime(date_time, pattern)))
    #if _f_time_sym_ == '-':
    #elif _f_time_sym_ == '-'

    return epoch

''' OpenTSDB에 HTTP POST방식으로 쿼리하는 함수 '''
def QueryData(_url, _required, _tags=None):
    headers = {'content-type': 'application/json'}

    dp = OrderedDict()    # dp (Data Point)
    dp["start"] = convertTimeToEpoch(_required["start"])
    dp["end"] = convertTimeToEpoch(_required["end"])    # not exactly required

    temp = OrderedDict()
    temp["aggregator"] = _required["aggregator"]
    temp["metric"] = _required["metric"]
    if _tags != None:
        temp["tags"] = _tags

    dp["queries"] = []
    dp["queries"].append(temp)

    #print " [Querying]" + json.dumps(dp, ensure_ascii=False, indent=4)
    response = requests.post(_url, data=json.dumps(dp), headers= headers)

    while response.status_code > 204:
        print " [Bad Request] Query status: %s" % (response.status_code)
        print " [Bad Request] We got bad request, Query will be restarted after 3 sec!\n"
        time.sleep(3)

        print " [Querying]" + json.dumps(dp, ensure_ascii=False, indent=4)
        response = requests.post(_url, data=json.dumps(dp), headers= headers)

    pout = " [Query is done, got reponse from server]"
    pout += " : now starting processing, writing and more "
    print pout
    return response

''' 실질적으로 OpenTSDB에 HTTP POST 방식으로 PUT Request를 보내는 함수
    50개로 multiple data 를 put 하는게 가장 좋으며, 늘어날 때는 테스트 필요함
    http://opentsdb.net/docs/build/html/api_http/put.html '''
def putRequest(_session, _url, _buffer):
    ''' put sends json packs to opentsdb, since opentsdb runs on a multi-thread mode
        putRequest runs efficiently parallelized , _buffer is array of dict'''

    headers = {'content-type': 'application/json'}

    for i in xrange(0, len(_buffer), 50):
        #print json.dumps(_buffer[i:i+50], ensure_ascii=False, indent=4)
        response = _session.post(_url, data=json.dumps(_buffer[i:i+50]), headers= headers)
        while response.status_code > 204:
            print "error!"
            print response
            response = _session.post(_url, data=json.dumps(_buffer[i:i+50]), headers= headers)

        if i+1 % 10000 == 0:
            print "\tputData: %s / %s finished" % (i+1, len(_buffer))

def guaranteePutRetry(_session, _url, _buf, _time):
    ''' Prevent sending too many requests from same ip address in short period of time '''
    while(True):
        try:
            putRequest(_session, _url, _buf)
        except requests.exceptions.ConnectionError:
            print "<%s> -> RETRY after %ssec" % (current_process().name, str(_time))
            time.sleep(_time)
            continue
        break


''' 데이터를 받아와서 JSON 형태로 만들어 buf에 담고 putRequest 함수로 전달 '''
def PutData(_session, _url, _metric, _content, _carid, _data):
    buf = []
    keys = _data.keys()

    for k in keys:
        dp = OrderedDict()    # dp (Data Point)

        dp["metric"] = _metric
        dp["timestamp"] = int(k)
        dp["value"] = int(_data[k])
        #print dp["value"]

        dp["tags"] = OrderedDict()
        dp["tags"]["content"] = _content
        dp["tags"]["carid"] = _carid

        buf.append(dp)

        if len(buf) >= MAX_BUFFER:
            guaranteePutRetry(_session, _url, buf, 3)
            buf = []

    guaranteePutRetry(_session, _url, buf ,3)
