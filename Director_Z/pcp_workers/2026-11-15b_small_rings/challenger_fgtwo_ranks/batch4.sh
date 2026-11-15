#!/bin/bash
# batch4.sh RUNDIR : fgtwo_beam.py width cap W=2 (BEAM=-2), 4 in parallel, timeout 600 s, ulimit -v 3000000
RD=$1; mkdir -p $RD; cp "$(dirname $0)/fgtwo_beam.py" $RD/; cd $RD
ulimit -v 3000000
jobs_list() {
for C in Z8_r4_kodd Z4Z2_r4_keven Z4_kodd_c1 Z2Z3_rodd; do echo "$C 3 12 7 2000000 -2"; done
for C in Z2Z3_rodd Z4_kodd_c3 Z8_r4_kodd Z4Z2_r4_keven; do echo "$C 5 12 8 2000000 -2"; done
for C in Z2Z3_rodd Z2Z2_keven Z4_kodd_c1 Z8_r4_kodd; do echo "$C 7 13 9 2000000 -2"; done
for C in Z4Z2_M6_keven Z4Z3_M6_rodd Z8_M6_kodd; do echo "$C 12 12 8 2000000 -2"; done
echo "Z16Z2_M8_keven 16 13 9 2000000 -2"
}
jobs_list | xargs -P 4 -L 1 bash -c 's=$(date +%s.%N); timeout 600 python3 fgtwo_beam.py $0 $1 $2 $3 $4 $5 res_$0_N$1_L$2_L0$3_B$5.json > log_$0_N$1_L$2_L0$3_B$5.txt 2>&1; e=$?; echo "python3 fgtwo_beam.py $0 $1 $2 $3 $4 $5 res_$0_N$1_L$2_L0$3_B$5.json exit=$e sec=$(echo "$(date +%s.%N)-$s"|bc)" >> cmdlog.txt'
