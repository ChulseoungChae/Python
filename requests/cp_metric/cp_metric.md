# ◎ cp_metric.py


----
    # -*- coding: utf-8 -*-

    # Author : jeonghoonkang , https://github.com/jeonghoonkang
    # Comment : ChulseoungChai , https://github.com/ChulseoungChai


    """ metric copy for openTSDB
        목적: OpenTSDB의 메트릭 데이터를 복사
        기능 : metric -> new metric 복사
               metric -> 다른 IP 서버로 복사
    """
    from __future__ import print_function  #파이썬2에서 파이썬3 문법을 사용하기 위해 임포트
    import sys
    import time
    import datetime
    # sys,time, datetime 모듈 임포트

    #import math
    import requests
    import json
    import copy
    #from collections import OrderedDict
    #import numpy as np
    #import pandas as pd
    from multiprocessing import Pool, current_process

    import HTTP_POST_request
    #외부모듈 임포트

    #import DataFrameInfo
    #import multi_make_process as m_proc

    # 아래부터는 keti 함수 import

    import ketitime
    #외부모듈 임포트
    
----    

    """ 실제 작업에 필요한 query parameter 예 - 초기값 """
    query_parameter = {
        "start" : "2014-06-01 00:00:00",
        "end": "2014-06-02 00:00:00",
        "aggregator" : "none",
        #aggregator : 여러회사 상품이나 서비스에 대한 정보를 모아 제공하는 웹사이트
        "metric" : "____test____"
    }


    """ 쿼리 하려는 tag """
    query_tags = {
    }
    # 빈 딕셔너리 생성
    
----
#### ● 사용자의 파이썬 파일명, IP주소, 포트, 입력 메트릭, 출력 메트릭, 시작날짜, 끝날짜를 입력받아서 반환해주는 함수

    def brush_args():
        usage = "\n usage : python %s {IP address} {port} " %sys.argv[0]
        usage += "{in_metric_name} {out_metric_name}"
        usage += "\n usage : python %s {IP address} {port} " %sys.argv[0]
        usage += "{in_metric_name} {out_metric_name} {start_day} {end_day}"
        print ( usage + '\n'  )
        # 사용자가 입력해야할 정보들 메시지 출력

        _len = len(sys.argv)
        # 사용자가 입력한 인자의 갯수를 _len 변수에 저장

        if _len < 7:
            print (" 추가 정보를 입력해 주세요. 위 usage 설명을 참고해 주십시오")
            print (" python 이후, 아규먼트 갯수 7개 필요 ")
            print (" 현재 아규먼트 %s 개가 입력되었습니다." %(_len) )
            print (" check *run.sh* file ")
            exit (" You need to input more arguments, please try again \n")
        # 파이썬 파일명, IP주소, 포트, 입력 메트릭, 출력 메트릭, 시작날짜, 끝날짜 전부 입력이 되지 않으면 아래 메시지 출력후 종료

        _ip = sys.argv[1]
        _port = sys.argv[2]
        _in_met = sys.argv[3]
        _out_met = sys.argv[4]
        _start = None
        _end = None
        #각 변수에 입력 인자 저장(ip = IP주소, port = 포트번호, in_met = 입력메트릭, out_met = 출력 메트릭, 시작날짜,끝날짜 값 None)

        if _len > 4:
            _start = sys.argv[5]
            _end = sys.argv[6]
        #입력 인자가 5개 이상( 파일명, IP주소, 포트, 입력 메트릭, 출력 메트릭)이면 시작날짜와 끝날짜를 추가해준다

        if ( len(_start) < 15 ):
            _start = ketitime._check_time_len(_start)
            _end = ketitime._check_time_len(_end)
        # 시작날짜의 길이가 15 미만이면(시간, 분, 초가 입력이 되지 않으면) 외장모듈 ketitime의 check_time_len()함수 동작

        return _ip, _port, _in_met, _out_met, _start, _end
        # 각 인자값이 저장된 변수들을 반환

----

    def sendBuf(buf_dict_list):
        _data = buf_dict_list
        #함수 호출시 데이터값을 _data 변수에 저장
        _write_url = g_w_url
        #사용자가 입력한 ip값을 _write_url에 저장
        
        with requests.Session() as s:
            #This module provides a Session object to manage and persist settings across
            decode_data = json.dumps(buf_dict_list, indent=2)
            if g_debug_off:
                print (decode_data)
                print (type(decode_data))
                print (type(_data))
                _deco_data_cnt_ = len(decode_data)
                print (_deco_data_cnt_)
            try:
                _r = s.post("http://125.140.110.217:44242/api/put?", decode_data)
            except requests.exceptions.ConnectionError as e :
                 time.sleep(5)
                _r = s.post("http://125.140.110.217:44242/api/put?", decode_data)

            while _r.status_code > 204:
                print ("error!")
                print (_r)
                try :
                    _r = s.post("http://125.140.110.217:44242/api/put?", decode_data)
                except requests.exceptions.ConnectionError as e :
                    pass
            # _r의 서버 응답코드가 204이상이면 에러문장과 _r값을 출력후 try except문 실행        
                    
            # with as문 : 보통 파일을 열면 작업후 항상 close를 해줘야 하지만 with as문을 사용하면 파일 열고 작업후 인터프리터가 자동으로 닫게 처리해준다
            # try except : try 블록 수행 중 오류가 발생하면 except 블록이 수행된다. 하지만 try블록에서 오류가 발생하지 않는다면 except 블록은 수행되지 않는다.

----

    def postDp(dict_buf):
        # make multiple list of 50 chunk dict
        # send every chunk which has 50 dp in it
        _tot_len = len(dict_buf)
        _solid = _tot_len/50
        _pos_end = 0

        if _solid > 0 :
            for _idx in xrange(_solid):
                _pos_start = 50 * _idx
                _pos_end   = _pos_start + 50
                _send_buf  = dict_buf[_pos_start:_pos_end]
                sendBuf(_send_buf)
                # send : post dp, 실제 전송
                if g_debug_off:
                    print ("send solid chunk", _idx)
                    print (_send_buf)

        _send_buf = dict_buf[_pos_end:]
        sendBuf(_send_buf)
        # send : post dp, 실제 전송

        if g_debug_off :
            print ("send last chunk")
            print (_send_buf)

        return True

----
#### 

    def putIteration(_dict_list, _len):
        putDict = dict()
        putDict['metric'] = None
        putDict['tags'] = None
        dict_array=[]
        _current_cnt = 0
        #

        for one_dict in _dict_list:
            _current_cnt += 1
            putDict['metric'] = one_dict['metric']
            putDict['tags'] = one_dict['tags']
            for k, v in one_dict.iteritems():
            # iteritems() 메소드는 딕셔너리의 key와 그에 상응하는 값에 대해 접근하는 메소드이다.
            # ex) d = {'person': 2, 'cat': 4, 'spider': 8}
            # for animal, legs in d.iteritems():
            #    print 'A %s has %d legs' % (animal, legs)
            # 출력 "A person has 2 legs", "A spider has 8 legs", "A cat has 4 legs", 한 줄에 하나씩 출력.
                # key are metric, dps, tags, aggregatorTag
                # we don't need aggregatorTag which len is 0
                if len(v) == 0: continue
                if k == 'dps' and len(v) ==1 :
                    putDict['timestamp'], putDict['value'] in one_dict['dps'].iteritems()
                    dict_array.append(putDict)
                else :
                    for kt, pv in one_dict['dps'].iteritems() :
                        putDict['timestamp'] = kt
                        putDict['value'] = pv
                        dict_array.append(putDict)
                    if g_debug_off:
                        print (dict_array)
                        print ("리스트로 구성된 딕셔너리 갯수", len(dict_array))

                    if True == postDp(dict_array):
                    # 실제 전송은 postDB() 내부에서 실행
                        __display_out = "current progress = %s / %s \r" %(_current_cnt, _len)
                        sys.stdout.write(__display_out)
                        sys.stdout.flush()
                dict_array=[]

        return True

----
#### ● 스트링 데이터를 딕셔너리 형태로 변환

    def processingResponse(in_data):
        '''openTSDB에서 전송받은, string 들을 dictionary로 변경하여
           dict 를 회신함. 형태를 변경하고, dict의 갯수를 알려줌'''

        _d = in_data
        _r = eval(_d.content)
        # eval(expression)은 실행 가능한 문자열(1+2, 'hi' + 'a' 같은 것)을 입력으로 받아 문자열을 실행한 결과값을 리턴하는 함수이다.
        # queryData.content is string, thus convert this to list

        if g_debug_on :
        # g_debug_on 이 1이므로 참이되어 밑에 문장들을 실행한다
            print ("... debugging print ... filename: %s" %__file__)
            print (type(_d.content), len(_d.content))
            _l = len(_r)
            # _r의 길이를 _l에 저장
            print (type(_r), _l)
            # _r의 타입과 _l을 출력
            if g_debug_off:
            # g_debug_off 가 0이므로 거짓이 된다 따라서 아래문장들은 출력이 되지않는다
                print (_r[0]['metric'])
                print (_r[0]['tags'])
                print (_r[0]['dps'])

        return _r, _l
        # dict 와 length (딕셔너리 갯수) 리턴

----
#### ● TSDB에서 데이터를 읽어와서 데이터를 딕셔너리 형태로 변환하고 

    def main_run(_date):
        query_parameter['start'] = _date
        query_parameter['end'] = ketitime.strday_delta(_date, 1)
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
        # _url변수에 http://ip:port/api/query 형식으로 저장
        if g_debug_on : print (_url, _q_para, query_tags)
        # g_debug_on 이 1이라 참이되기 때문에 _url, _q_para, query_tags 출력
        queryData = HTTP_POST_request.QueryData(_url, _q_para, query_tags)
        # 데이터 reading from DB, 스트링 데이터임

        _dictbuf, _dictlen = processingResponse(queryData)
        # 스트링 데이터를 딕셔너리 형태로 변환

        putIteration(_dictbuf, _dictlen)
        # 데이터 입력 to DB

        return None
        # 반환값 None

----
#### ● 프로그램 동작 실행

    if __name__ == "__main__":     #메인 동작

        g_debug_on = 1
        g_debug_off = 0
        # 변수 g_debug_on, g_debug_off에 각각 1,0 대입

        _send_buf = []
        # postDp(dict_buf)함수에서 쓰이는 변수, 비어있는 리스트형태로 만듦

        start_time = time.time()
        #time.time() : 컴퓨터의 현재 시각을 구하는 함수, 반환 값 기준 시각에서 몇 초가 지났는지를 나타내주는 실수(float). 한번 호출한 뒤 다시 호출할 때까지의 시간을 측정한다
        start_datetime = datetime.datetime.now()
        #datetime.datetime.now() : 컴퓨터의 현재 시간을 datetime.datetime 클래스 객체로 만들어 반환. -> datetime.datetime(년, 월, 일, 시, 분. 초, 마이크로초(.000001)) ->(2018, 5, 1, 2, 34, 56, 196637)

        ip, port, in_metric, out_metric, q_start, q_end = brush_args()
        # brush_args() 함수를 실행하여 사용자가 입력한 인자값들을 변수에 대입

        g_w_url = ip
        # ip를  g_w_url변수에 대입하고 sendBuf(buf_dict_list)함수에서 사용

        _date_on  = q_start
        # 사용자가 데이터 추출할 시작날짜를 _date_on 변수에 저장

        _date_off = q_end
        # 사용자가 데이터 추출할 끝날짜를 _date_off 변수에 저장

        while(_date_on != None):
            main_run(_date_on)
            _date_on = ketitime.daydelta(_date_on, _date_off)
        #데이터 추출 시작날짜가 None이면 main_run(_date_on) 함수를 실행하고

        run_time = time.time() - start_time
        # 현재시각에서 처음 시작한 시간을 빼서 런타임 시간을 구한다.

        print ( "\n\n [Main] Query time: %s ~ %s" % (q_start,q_end) )
        # 쿼리 시간을 출력함
        print ( " Run time: %.4f (sec)" % (run_time) )
        # 런타임 시간을 소수점 이하 4자리까지의 실수형태로 표현한다
