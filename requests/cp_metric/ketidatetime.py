# -*- coding:utf:8 -*-
# 사용자가 데이터를 추출할 날짜를 입력하면 날짜,시간정보를 형식에 맞게 변환, 처리 및 입력오류 판별하는 모듈
from __future__ import print_function
# 파이썬2에서 파이썬3 프린트 문법을 사용하기 위해 임포트
import datetime
# 날짜,시간 사용 모듈 datetime 모듈 임포트

g_debug_on = 1
g_debug_off = 0

# 입력된 날짜형식을 체크하고 시간정보를 더하여 
def _check_time_len( time ):

    print ( " ### warning, using %s which is under development " %__file__ )
    _debug_print = 1
    _ret_time = time
    # "### warning, using (파일의 path) which is under development" 문장출력
    # _debug_print 에 1 대입

    _year = time[:4]
    #_year 변수에 time(0) ~ time(3) 값을 저장
    _year_int = int(_year)
    # _year을 정수형으로 변환하여 _year_int에 저장
    if _year_int < 1900 or _year_int > 2100 :
        print (_year)
        exit(" Error @ %s : please check time string " %__file__)
    # 년도가 1900 보다 작거나 2100보다 크면 _year 를 출력하고 " Error @ (현재파일경로) : please check time string " 출력후 종료


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

def daydelta(_date_on, _date_off, dys=None, hrs=None, mins=None):

    _on    = str2datetime(_date_on)
    _off   = str2datetime(_date_off)
    # 각각 날짜와 시간정보 리스트를 각각의 변수에 저장한다.
    if dys != None : _delta = _on + datetime.timedelta(days = 1)
    # dys가 None이 아니면 시작날짜에 하루를더함
    elif hrs !=None : _delta = _on + datetime.timedelta(hours = 1)
    # hrs가 None이 아니면 시작날짜에 한시간을 더함    
    elif mins !=None : _delta = _on + datetime.timedelta(minutes = 20)
    # mins가 None이 아니면 시작날짜에 20분을 더함    
    if _delta == _off :
        return None
    # _delta와 off가 같으면 None 반환
    else :
        return datetime2str(_delta)
    # 다르면 datetime2str(_delta)함수 실행

# 요일+1/시간+1/분+20 조건에 맞는것을 추가
def strday_delta(_s, _h_scale):
    _dt  = str2datetime(_s)
    if _h_scale == 24 : _dt += datetime.timedelta(days = 1)
    elif _h_scale == 1 : _dt += datetime.timedelta(hours = 1)
    elif _h_scale == 0.1 : _dt += datetime.timedelta(minutes = 20)
    _str = datetime2str(_dt)
    if g_debug_off :
        print (_str)
        iin = raw_input("go on? otherwise press [n]")
        if iin == 'n' : exit()
    return _str

def ts2datetime(ts_str):
    return datetime.datetime.fromtimestamp(int(ts_str)).strftime('%Y/%m/%d-%H:%M:%S')

def datetime2ts(dt_str):
    dt = datetime.datetime.strptime(dt_str, "%Y/%m/%d-%H:%M:%S")
    return time.mktime(dt.timetuple())

def ts2str(ts):
    return str(int(ts))

def str2datetime(dt_str):
    return datetime.datetime.strptime(dt_str, "%Y/%m/%d-%H:%M:%S")
     # datetime.datetime.strptime() : 문자열로부터 날짜와 시간정보를 읽어서 datime.datetime 클래스 객체를 만든다.

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

def add_time(dt_str, days=0, hours=0, minutes=0, seconds=0):
    return datetime2str(str2datetime(dt_str) + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))

def is_past(dt_str1, dt_str2):
    return datetime2ts(dt_str1) < datetime2ts(dt_str2)

def is_weekend(dt_str):
    if self.str2datetime(dt_str).weekday() >= 5: return '1'
    else: return '0'
