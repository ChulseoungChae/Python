#/bin/bash
#실행스크립트
export cmd='python cp_metric_with_file.py 125.140.110.217 54242 HanuriTN_00 125.140.110.217 44242 2014/08/01-00:00:00 2014/08/02-00:00:00 '
echo ""
echo $cmd
exec $cmd
