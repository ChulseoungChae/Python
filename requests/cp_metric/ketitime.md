# ketitime.py 설명
### ◎ ketitime.py
> ● cp_metric.py 에서 사용하기 위해 만든 모듈

> ● 사용자가 데이터를 추출할 날짜를 입력하면 날짜,시간정보를 형식에 맞게 변환, 처리 및 입력오류 판별하는 모듈 

----
#### ◎ 필요 모듈 임포트

    # -*- coding:utf:8 -*-
    from __future__ import print_function
    # 파이썬2에서 파이썬3 프린트 문법을 사용하기 위해 임포트
    import datetime
    # 날짜,시간 사용 모듈 datetime 모듈 임포트

----
#### ◎ 입력오류 판별 및 문장출력 함수

    def _check_time_len( time ):

        print ( " ### warning, using %s which is under development " %__file__ )
        _debug_print = 1
        _ret_time = time
        # "### warning, using (파일의 path) which is under development" 문장출력
        # _debug_print 에 1 대입



        _year = time[:4]
        #_year 변수에 time(0) ~ time(3) 값을 저장
        if int(_year) < 1900 :
            print (_year)
            exit(" Error @ %s : please check time string " %__file__)
        # 년도가 1900 보다 작으면 _year 를 출력하고 " Error @ (현재파일경로) : please check time string " 출력후 종료

        _year_month = time[4:5]
        # _year_month 변수에 time(4) 값을 저장
        if _year_month != "/":
            print (_year_month, 'It should be /')
            exit(" Error @ %s : please check time string " %__file__)
        # _year_month가 '/'가 아니면 현재 _year_month에 저장된 스트링을 출력하고 문장 출력후 종료

        _month = time[5:7]
        # _month 변수에 time(5), time(6) 값을 저장
        if int(_month) > 12:
            print (_month)
            exit(" Error @ %s : please check time string " %__file__)
        # month 값이 12보다 크면 현재 _month에 저장된 값 과 문장 출력후 종료

        _month_day = time[7:8]
        _day = time[8:10]
        # _month_day, _day 변수에 각각 time(7), time(8)~time(9) 값 저장

        _ret_time += '-00:00:00'
        # _ret_time 변수에 시간정보를 저장

        if _debug_print :
            print (" debug_option ", _year, _year_month, _month, _month_day, _day )
        # _debug_print 가 1이므로 참이되어 하단의 문장 출력

        #exit(" Error @ %s : please check time string" %__file__)

        return _ret_time
        # 날짜와 시간정보가 더해진 값을 리턴
        
----
#### ◎ 시작날짜와 입력날짜 차이 판별해 해당값 리턴 함수

    def daydelta(_date_on, _date_off):

        _on    = str2datetime(_date_on)
        _off   = str2datetime(_date_off)
        # 각각 날짜와 시간정보 리스트를 각각의 변수에 저장한다.

        _delta = _on + datetime.timedelta(days = 1)
        # datetime.timedelta() : datetime.datetime 클래스 객체의 차이를 구하고 그결과가 datetime.timedelta 클래스 객체로 반환된다
        # ex) _on = datetime.datetime(2018, 5, 30, 14)
        #     _delta = _on + datetime.timedelta(day = 1)
        #     _delta = datetime.datetime(2018, 5, 31, 14)

        if _delta == _off :
            return None
        # 시작날짜와 끝날짜가 하루차이 나면 None 리턴
        # cp metric.py 에서는 날짜까지만 입력하고 시간은 자동적으로 00:00:00으로 되기때문에 정확히 24시간 차이가 나게됌
        # ex) 입력 2018/05/01 입력하면 2018/05/01-00:00:00 으로 변환되어 사용됌
        # 만약 다른 코드에서 이 모듈을 사용하려면 24시간 미만일 때에도 처리를 해줘야함

        else :
            return datetime2str(_delta)
        # 시작날짜와 끝날짜가 이틀이상 차이나면 datetime2str() 함수를 리턴

----
#### ◎ 요일 하루 추가 함수

    def strday_delta(_s, delta=1):
        _dt  = str2datetime(_s)
        # _s 의 시간정보를 datetime.datetime 클래스 객체로 변환해서 _dt에 저장 
        _dt += datetime.timedelta(days = delta)
        # delta 만큼의 요일 차이를 추가(하루 추가)
        _str = datetime2str(_dt)
        # 요일을 추가한 시간정보를 문자열로 바꿈
        return _str
        # _str 리턴

----
#### ◎ 연월일시 형식 변경 함수

    def str2datetime(dt_str):
        return datetime.datetime.strptime(dt_str, "%Y/%m/%d-%H:%M:%S")
        # datetime.datetime.strptime() : 문자열로부터 날짜와 시간정보를 읽어서 datime.datetime 클래스 객체를 만든다.

----
#### ◎ 연월일시 형식 변경 함수

    def datetime2str(dt):
        return dt.strftime('%Y/%m/%d-%H:%M:%S')
        # 변수.strftime() : 지정 변수의 시간정보를 문자열로 바꿔주는 함수이다
        # ex) dt = datetime.datetime(2018, 5, 1, 0, 00, 00)
        #     print(dt.strftime('%Y/%m/%d-%H:%M:%S')) = dt.strftime('2018/05/01-00:00:00')
        # %Y - 앞의 빈자리를 0으로 채우는 4자리 연도 숫자
        # %m - 앞의 빈자리를 0으로 채우는 2자리 월 숫자
        # %d - 앞의 빈자리를 0으로 채우는 2자리 일 숫자
        # %H - 앞의 빈자리를 0으로 채우는 24시간 형식 2자리 시간 숫자
        # %M - 앞의 빈자리를 0으로 채우는 2자리 분 숫자
        # %S - 앞의 빈자리를 0으로 채우는 2자리 초 숫자
        # %A – 영어로 된 요일 문자열
        # %B – 영어로 된 월 문자열
        # 다른 날짜 시간 지정 문자열 참조 : https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
