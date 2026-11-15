#!/bin/bash
# batch.sh RUNDIR : runs fgtwo_ranks.py on every qualifying (carrier, N) with the L, L0 below; 3 in parallel
RD=$1; mkdir -p $RD; cp "$(dirname $0)/fgtwo_ranks.py" $RD/; cd $RD
ulimit -v 3000000
jobs_list() {
for spec in "3 7 4" "6 7 4" "5 8 5" "10 8 5" "7 9 7" "14 9 7"; do set -- $spec
  for C in Z2Z3_rodd Z2Z2_keven Z4_kodd_c1 Z4_kodd_c3 Z8_r4_kodd Z4Z2_r4_keven Z2Z3_rodd2; do echo "$C $1 $2 $3"; done; done
for C in Z4Z2_M6_keven Z4Z3_M6_rodd Z8_M6_kodd Z2Z3_rodd2; do echo "$C 12 8 6"; done
echo "Z16Z2_M8_keven 16 10 8"
}
jobs_list | xargs -P 3 -L 1 bash -c 's=$(date +%s.%N); timeout 400 python3 fgtwo_ranks.py $0 $1 $2 $3 40000 res_$0_N$1_L$2_L0$3.json > log_$0_N$1_L$2_L0$3.txt 2>&1; e=$?; echo "python3 fgtwo_ranks.py $0 $1 $2 $3 40000 res_$0_N$1_L$2_L0$3.json exit=$e sec=$(echo "$(date +%s.%N)-$s"|bc)" >> cmdlog.txt'
