#!/bin/bash
#실행스크립트
# 원본 json파일 : 20140624.json
# 만들어진 excel파일 : 20140624.json.xlsx
export cmd='python JsonToExcel.py 20140624.json '
echo ""
echo $cmd
exec $cmd
