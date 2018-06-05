# -*- coding: utf-8 -*-
import requests
import json

if __name__ == '__main__':

    #GET
    #payload = {'key1': 'value1', 'key2': 'value2'}
    # re = requests.get('http://httpbin.org/get', params=payload)

    r = requests.get('http://httpbin.org/get')
    print(r.request)  # 내가 보낸 request 객체에 접근 가능
    print(r.status_code)  # 서버 응답 코드를 반환, 200 이 출력된다면 정상
    print(r.raise_for_status())  # 200 OK 코드가 아닌 경우 에러 발동
    print(r.text)  # =print(re.content), 실제 웹페이지에 사용되는 html 소스값 출력
    print(r.json())  # json response일 경우 딕셔너리 타입으로 바로 변환
    print(r.headers)  # 헤더를 반환
    print(r.url)  # 주소를 반환

    '''
    #POST
    dic = {'key1': 'value1', 'key2': 'value2'}
    URL = 'http://httpbin.org/post'
    r = requests.post(URL)
    r = requests.post('http://httpbin.org/post', data=dic)
    res = requests.post(URL, data=json.dumps(dic))

    print(r.status_code)
    print(r.text)
    print(res.text)
    
    r = requests.put('http://httpbin.org/put')
    r = requests.delete('http://httpbin.org/delete')
    r = requests.head("http://httpbin.org/get")
    r = requests.options("http://httpbin.org/get")
    '''