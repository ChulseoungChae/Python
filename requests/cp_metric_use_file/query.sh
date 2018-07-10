#!/bin/bash
#실행스크립트
export cmd='python query_metric.py 125.140.110.217 54242 HanuriTN_00 125.140.110.217 44242 HanuriTN_00 2014/07/17-01:00:00 2014/08/17-00:00:00 '
echo ""
echo $cmd
exec $cmd

