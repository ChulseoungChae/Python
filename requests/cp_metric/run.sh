#/bin/bash
#실행스크립트
# 참조 : 125.140.110.217 : 4242
# 원본 데이터 : none:rc04_simple_data_v3
# 테스트 = 데이터 있는 구간 : 2016/07/16 , 2016/07/18
export cmd='python cp_metric.py 125.140.110.217 4242 rc04_simple_data_v3 125.140.110.217 54242 2016/07/16 2016/07/18 '
echo ""
echo $cmd
exec $cmd
