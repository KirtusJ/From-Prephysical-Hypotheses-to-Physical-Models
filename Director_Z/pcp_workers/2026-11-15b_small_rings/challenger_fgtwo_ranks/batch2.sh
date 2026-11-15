#!/bin/bash
# batch2.sh RUNDIR : fgtwo_beam.py runs, 3 in parallel, timeout 500 s, ulimit -v 3000000
RD=$1; mkdir -p $RD; cp "$(dirname $0)/fgtwo_beam.py" $RD/; cd $RD
ulimit -v 3000000
jobs_list() {
for C in Z2Z3_rodd Z2Z2_keven Z4_kodd_c1 Z8_r4_kodd Z4Z2_r4_keven; do echo "$C 3 9 6 600000 0"; done
for C in Z2Z3_rodd Z2Z2_keven Z4_kodd_c3 Z8_r4_kodd Z4Z2_r4_keven; do echo "$C 5 11 7 400000 20000"; done
for C in Z2Z3_rodd Z2Z2_keven Z4_kodd_c1 Z8_r4_kodd Z4Z2_r4_keven; do echo "$C 7 13 9 400000 15000"; done
for C in Z4Z2_M6_keven Z4Z3_M6_rodd Z8_M6_kodd; do echo "$C 12 12 8 400000 15000"; done
echo "Z16Z2_M8_keven 16 14 10 400000 15000"
}
jobs_list | xargs -P 3 -L 1 bash -c 's=$(date +%s.%N); timeout 500 python3 fgtwo_beam.py $0 $1 $2 $3 $4 $5 res_$0_N$1_L$2_L0$3_B$5.json > log_$0_N$1_L$2_L0$3_B$5.txt 2>&1; e=$?; echo "python3 fgtwo_beam.py $0 $1 $2 $3 $4 $5 res_$0_N$1_L$2_L0$3_B$5.json exit=$e sec=$(echo "$(date +%s.%N)-$s"|bc)" >> cmdlog.txt'
