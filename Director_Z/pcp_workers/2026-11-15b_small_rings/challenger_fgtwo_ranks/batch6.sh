#!/bin/bash
# batch6.sh RUNDIR : fgtwo_beam.py W=2, 2 in parallel, timeout 600 s, ulimit -v 3000000
RD=$1; mkdir -p $RD; cp "$(dirname $0)/fgtwo_beam.py" $RD/; cd $RD
ulimit -v 3000000
printf "%s\n" "Z2Z2_keven 7 13 9 2000000 -2" "Z4_kodd_c1 7 13 9 2000000 -2" "Z8_M6_kodd 12 12 8 2000000 -2" "Z4Z2_M6_keven 12 12 8 2000000 -2" | xargs -P 2 -L 1 bash -c 's=$(date +%s.%N); timeout 600 python3 fgtwo_beam.py $0 $1 $2 $3 $4 $5 res_$0_N$1_L$2_L0$3_B$5.json > log_$0_N$1_L$2_L0$3_B$5.txt 2>&1; e=$?; echo "python3 fgtwo_beam.py $0 $1 $2 $3 $4 $5 res_$0_N$1_L$2_L0$3_B$5.json exit=$e sec=$(echo "$(date +%s.%N)-$s"|bc)" >> cmdlog.txt'
